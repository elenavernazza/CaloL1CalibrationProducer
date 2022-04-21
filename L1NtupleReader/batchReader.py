from itertools import chain
from TowerGeometry import *
import pandas as pd
import numpy as np
import argparse
import uproot3
import glob
import sys
import csv
import os


def deltarSelect( df, dRcut ):
    deta = np.abs(df['jetEta'] - df['jetEta_joined'])
    dphi = np.abs(df['jetPhi'] - df['jetPhi_joined'])
    sel = dphi > np.pi
    dphi = np.abs(sel*(2*np.pi) - dphi)
    return (np.sqrt(dphi*dphi+deta*deta) > dRcut) | ((deta == 0) & (dphi == 0))


# returns an array with 81 entries, for each entry we have [eta,phi] number of the tower belonging to the chunky donut
def ChunkyDonutTowers(jetIeta, jetIphi):

    ieta_start = jetIeta
    iphi_start = jetIphi

    # define the top left position of the chunky donut
    for i in range(0,4):
        ieta_start = PrevEtaTower(ieta_start)
    for i in range(0,4):
        iphi_start = PrevPhiTower(iphi_start)

    ieta = ieta_start
    iphi = iphi_start

    CD = []
    for i in range(0,9): # scan eta direction
        if i > 0:
            ieta = NextEtaTower(ieta)
        iphi = iphi_start # for every row in eta we restart from the iphi on the left
        for j in range(0,9): # scan phi direction
            if j > 0:
                iphi = NextPhiTower(iphi)
            CD.append([ieta,iphi])
    return CD


def padDataFrame( dfFlatEJT ):
    padded = dfFlatEJT
    for uniqueIdx in dfFlatEJT.index.unique():
        #print(uniqueIdx)
        try:
            len(dfFlatEJT['jetIeta'][uniqueIdx])
            jetIeta = dfFlatEJT['jetIeta'][uniqueIdx].unique()[0]
            jetIphi = dfFlatEJT['jetIphi'][uniqueIdx].unique()[0]
            jetPt = dfFlatEJT['jetPt'][uniqueIdx].unique()[0]
        except TypeError:
            jetIeta = dfFlatEJT['jetIeta'][uniqueIdx]
            jetIphi = dfFlatEJT['jetIphi'][uniqueIdx]
            jetPt = dfFlatEJT['jetPt'][uniqueIdx]

        padder = pd.DataFrame(columns=dfFlatEJT.columns, index=range(0,81))
        padder['uniqueId'] = uniqueIdx
        padder['jetPt'] = jetPt
        padder['jetIeta'] = jetIeta
        padder['jetIphi'] = jetIphi
        padder['iem'] = 0
        padder['ihad'] = 0
        padder['iet'] = 0
        padder[['ieta','iphi']] = ChunkyDonutTowers(jetIeta,jetIphi)

        padded = padded.append(padder)
        del padder
        
    return padded


def mainReader( dfET, dfEJ, saveToDFs, saveToTensors ):
    if len(dfET) == 0 or len(dfEJ) == 0:
        print(' ** WARNING: Zero data here --> EXITING!\n')
        return
    
    # flatten out the dataframes so that ech entry of the dataframe is a number and not a vector
    dfFlatET = pd.DataFrame({
        'event': np.repeat(dfET[b'event'].values, dfET[b'ieta'].str.len()), # event IDs are copied to keep proper track of what is what
        'ieta': list(chain.from_iterable(dfET[b'ieta'])),
        'iphi': list(chain.from_iterable(dfET[b'iphi'])),
        'iem' : list(chain.from_iterable(dfET[b'iem'])),
        'ihad': list(chain.from_iterable(dfET[b'ihad'])),
        'iet' : list(chain.from_iterable(dfET[b'iet']))
        })

    dfFlatEJ = pd.DataFrame({
        'event': np.repeat(dfEJ[b'event'].values, dfEJ[b'jetEta'].str.len()), # event IDs are copied to keep proper track of what is what
        'jetEta': list(chain.from_iterable(dfEJ[b'jetEta'])),
        'jetPhi': list(chain.from_iterable(dfEJ[b'jetPhi'])),
        'jetPt' : list(chain.from_iterable(dfEJ[b'jetPt']))
        })
    dfFlatEJ['jetId'] = dfFlatEJ.index # each jet gets an identifier based on a progressive value independent of event -> this allows further flexibility of ID on top of event

    # reset indeces to be the event number to be able to join the DFs later
    dfFlatET.set_index('event', inplace=True)
    dfFlatEJ.set_index('event', inplace=True)

    ## DEBUG
    # print(dfET.shape[0])
    # print(dfEJ.shape[0])
    # dfFlatET = dfFlatET.head(100).copy(deep=True)
    # dfFlatEJ = dfFlatEJ.head(100).copy(deep=True)

    # cerate all the possible combinations of jets per each event
    dfFlatEJ  = dfFlatEJ.join(dfFlatEJ, on='event', how='left', rsuffix='_joined', sort=False)
    # select only those jets that are at least dRcut away from each other
    dRcut = 0.5
    dfFlatEJ['dRsafe'] = deltarSelect(dfFlatEJ, dRcut)
    notSafe = list(dfFlatEJ[(dfFlatEJ['dRsafe']==False)]['jetId'])
    dfFlatEJ = dfFlatEJ[dfFlatEJ.jetId.isin(notSafe) == False]
    dfFlatEJ.drop(['jetEta_joined', 'jetPhi_joined', 'jetPt_joined', 'jetId_joined', 'dRsafe'], axis=1, inplace=True) # drop columns not needed anymore
    dfFlatEJ.drop_duplicates('jetId', keep='first', inplace=True) # drop duplicates of teh jets

    # find ieta/iphi values for the jets
    FindIeta_vctd = np.vectorize(FindIeta)
    FindIphi_vctd = np.vectorize(FindIphi)
    dfFlatEJ['jetIeta'] = FindIeta_vctd(dfFlatEJ['jetEta'])
    dfFlatEJ['jetIphi'] = FindIphi_vctd(dfFlatEJ['jetPhi'])
    dfFlatEJ.drop(['jetEta', 'jetPhi'], axis=1, inplace=True) # drop columns not needed anymore

    # join the jet and the towers datasets -> this creates all the possible combination of towers and jets for each event
    dfFlatEJT = dfFlatEJ.join(dfFlatET, on='event', how='left', rsuffix='_joined', sort=False)

    # select only towers that are inside the +-4 range from jetIphi
    # since on phi the range is wrapped around 72 we need to take into account the cases with |deltaIphi|>68
    dfFlatEJT['deltaIphi'] = dfFlatEJT['iphi'] - dfFlatEJT['jetIphi']
    dfFlatEJT = dfFlatEJT[((dfFlatEJT['deltaIphi']<=4)&(dfFlatEJT['deltaIphi']>=-4))|(dfFlatEJT['deltaIphi']<=-68)|(dfFlatEJT['deltaIphi']>=68)]

    # select only towers that are inside the +-5 range from jetIphi
    # since towers 0/29 do not exist we need to take a range larger by 1 tower on each side compared to the actual chunky donut
    dfFlatEJT['deltaIeta'] = dfFlatEJT['ieta'] - dfFlatEJT['jetIeta']
    dfFlatEJT = dfFlatEJT[(dfFlatEJT['deltaIeta']<=5)&(dfFlatEJT['deltaIeta']>=-5)]

    # compute the distances from towers +-29 and +-1
    # this gives us the possibility to define some specific conditions to select the correct towers of a cunky donut
    dfFlatEJT['deltaI29'] = 29 - dfFlatEJT['jetIeta']
    dfFlatEJT['deltaIm29'] = -29 - dfFlatEJT['jetIeta']
    dfFlatEJT['deltaI1'] = 1 - dfFlatEJT['jetIeta']
    dfFlatEJT['deltaIm1'] = -1 - dfFlatEJT['jetIeta']
    # define full OR condition in order to select the correct towers for each jet
    # the onditions (in coordinates wrt the jetIeta) are summarized in teh file bigORtowers.txt
    dfFlatEJT = dfFlatEJT[( ((dfFlatEJT['deltaI29']<5)&(dfFlatEJT['deltaI29']>0)&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=5)) | ((dfFlatEJT['deltaI29']>-5)&(dfFlatEJT['deltaI29']<0)&(dfFlatEJT['deltaIeta']>=-5)&(dfFlatEJT['deltaIeta']<=4)) | (((dfFlatEJT['deltaI29']<-5)|(dfFlatEJT['deltaI29']>5))&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=4)) | ((dfFlatEJT['deltaIm29']<5)&(dfFlatEJT['deltaIm29']>0)&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=5)) | ((dfFlatEJT['deltaIm29']>-5)&(dfFlatEJT['deltaIm29']<0)&(dfFlatEJT['deltaIeta']>=-5)&(dfFlatEJT['deltaIeta']<=4)) | (((dfFlatEJT['deltaIm29']<-5)|(dfFlatEJT['deltaIm29']>5))&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=4)) )]
    dfFlatEJT = dfFlatEJT[( ((dfFlatEJT['deltaI1']<5)&(dfFlatEJT['deltaI1']>0)&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=5)) | ((dfFlatEJT['deltaI1']>-5)&(dfFlatEJT['deltaI1']<0)&(dfFlatEJT['deltaIeta']>=-5)&(dfFlatEJT['deltaIeta']<=4)) | (((dfFlatEJT['deltaI1']<-5)|(dfFlatEJT['deltaI1']>5))&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=4)) | ((dfFlatEJT['deltaIm1']<5)&(dfFlatEJT['deltaIm1']>0)&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=5)) | ((dfFlatEJT['deltaIm1']>-5)&(dfFlatEJT['deltaIm1']<0)&(dfFlatEJT['deltaIeta']>=-5)&(dfFlatEJT['deltaIeta']<=4)) | (((dfFlatEJT['deltaIm1']<-5)|(dfFlatEJT['deltaIm1']>5))&(dfFlatEJT['deltaIeta']>=-4)&(dfFlatEJT['deltaIeta']<=4)) )]

    # drop what is no longer needed
    dfFlatEJT.drop(['deltaI29', 'deltaIm29', 'deltaI1', 'deltaIm1', 'deltaIphi', 'deltaIeta'], axis=1, inplace=True)

    # make the unique ID for each jet across all the files
    dfFlatEJT.reset_index(inplace=True)
    dfFlatEJT['uniqueId'] = dfFlatEJT['event'].astype(str)+'_'+dfFlatEJT['jetId'].astype(str)
    dfFlatEJT['uniqueIdx'] = dfFlatEJT['uniqueId'].copy(deep=True)
    dfFlatEJT.set_index('uniqueIdx', inplace=True)

    # drop what is no longer needed
    dfFlatEJT.drop(['event', 'jetId'], axis=1, inplace=True)

    # do the padding of the dataframe to have 81 rows for each jet        
    paddedEJT = padDataFrame(dfFlatEJT)
    paddedEJT.drop_duplicates(['uniqueId', 'ieta', 'iphi'], keep='first', inplace=True)
    paddedEJT.reset_index(inplace=True)

    # append the DFs from the different files to one single big DF
    dfTowers = paddedEJT[['uniqueId','ieta','iem','ihad','iet']]
    dfJets = paddedEJT[['uniqueId','jetPt']]

    ## DEBUG
    # print(dfFlatEJT)
    # print(dfTowers)

    ## DEBUG
    # print(dfTowers)
    # print(len(dfTowers.event.unique()), 'events')
    # print(len(dfTowers.uniqueId.unique()), 'jets')
    # print(len(dfTowers), 'rows')

    # save hdf5 files with dataframe formatted datasets
    storeT = pd.HDFStore(saveToDFs['towers']+'.hdf5', mode='w')
    storeT['towers'] = dfTowers
    storeT.close()

    storeJ = pd.HDFStore(saveToDFs['jets']+'.hdf5', mode='w')
    storeJ['jets'] = dfJets
    storeJ.close()

    # make the produced files accessible to the other people otherwise we cannot work together
    os.system('chmod 774 '+saveToDFs['towers']+'.hdf5')
    os.system('chmod 774 '+saveToDFs['jets']+'.hdf5')

    # define some variables on top
    dfTowers['ieta'] = abs(dfTowers['ieta'])
    dfTowers['iesum'] = dfTowers['iem'] + dfTowers['ihad']
    dfE = dfTowers[['uniqueId', 'ieta','iesum']]

    # set the uniqueId indexing
    dfE.set_index('uniqueId',inplace=True)
    dfJets.drop_duplicates('uniqueId', keep='first', inplace=True)
    dfJets.set_index('uniqueId', inplace=True)

    # do the one hot encoding of ieta
    dfEOneHotEncoded = pd.get_dummies(dfE, columns=['ieta'])
    for i in range(35,42):
        dfEOneHotEncoded['ieta_'+str(i)] = 0

    # convert to tensor input for the NN
    Y = np.array([dfJets.loc[i].values[0] for i in dfJets.index]).reshape(-1,1)
    X = np.array([dfEOneHotEncoded.loc[i].to_numpy() for i in dfE.index.drop_duplicates(keep='first')])

    # save .npz files with tensor formatted datasets
    np.savez_compressed(saveToTensors['towers']+'.npz', X)
    np.savez_compressed(saveToTensors['jets']+'.npz', Y)

    # make the produced files accessible to the other people otherwise we cannot work together
    os.system('chmod 774 '+saveToTensors['towers']+'.npz')
    os.system('chmod 774 '+saveToTensors['jets']+'.npz')




#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

### To run:
### python3 batchReader.py --fin <fileIN_path> --tag <batch_tag> --fout <fileOUT_path>
### OR
### python batchSubmitOnTier3.py (after appropriate modifications)

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--fin", dest="fin", default='')
    parser.add_option("--tag", dest="tag", default='')
    parser.add_option("--fout", dest="fout", default='')
    (options, args) = parser.parse_args()

    if (options.fin=='' or options.tag=='' or options.fout==''): print('** ERROR: wonrg input options --> EXITING!!'); exit()

    # define the two paths where to read the hdf5 files
    readfrom = {
        'towers'  : options.fin+'/towers/towers'+options.tag,
        'jets'    : options.fin+'/jets/jets'+options.tag
    }

    # define the paths where to save the hdf5 files
    saveToDFs = {
        'towers'  : options.fout+'/dataframes/towers'+options.tag,
        'jets'    : options.fout+'/dataframes/jets'+options.tag
    }
    # define the two paths where to save the hdf5 files
    saveToTensors = {
        'towers'  : options.fout+'/tensors/towers'+options.tag,
        'jets'    : options.fout+'/tensors/jets'+options.tag
    }

    print(readfrom['towers']+'.hdf5')

    # read hdf5 files
    readT = pd.HDFStore(readfrom['towers']+'.hdf5', mode='r')
    dfET = readT['towers']
    readT.close()

    readJ = pd.HDFStore(readfrom['jets']+'.hdf5', mode='r')
    dfEJ = readJ['jets']
    readJ.close()

    mainReader(dfET, dfEJ, saveToDFs, saveToTensors)
    print("DONE!")
