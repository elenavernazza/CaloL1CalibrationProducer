#librairies utiles
import numpy as np
import os
import sys
import copy
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

sys.path.insert(0,'..')
from Utils.TowerGeometry import *
from L1Training.NNModel_RegAndRate import *

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

def ExtractSFs(TTP, reg, min_energy, max_energy, energy_step, odir, i_epoch = None):

    if i_epoch: epoch = '_{}'.format(i_epoch)
    else: epoch = ''

    if reg == "HCAL" or reg == "ECAL":
        eta_towers = [i for i in range(1,28+1)]
        input_towers = []

        # always comput all the scale factors
        min_energy_tower = 1
        max_energy_tower = 256
        input_towers = []
        for i_energy in np.array(range(min_energy_tower, max_energy_tower+1, 1)):
            for i_eta in eta_towers:
                one_hot_tower = np.array([i_energy] + [0 if j != i_eta else 1 for j in range(1,40+1)])
                if reg == "ECAL":    
                    # apply 3/6/9 zero-suppression by inputing energy = 0.0
                    if i_eta == 26 and i_energy <=  6: one_hot_tower = np.array([0.0] + [0 if j != i_eta else 1 for j in range(1,40+1)])
                    if i_eta == 27 and i_energy <= 12: one_hot_tower = np.array([0.0] + [0 if j != i_eta else 1 for j in range(1,40+1)])
                    if i_eta == 28 and i_energy <= 18: one_hot_tower = np.array([0.0] + [0 if j != i_eta else 1 for j in range(1,40+1)])
                input_towers.append(one_hot_tower)
        input_towers = np.array(input_towers)
        Einput = input_towers[:,0].reshape(-1,1)
        Epredicted = TTP.predict(input_towers)

        vec_SFs_rounded = np.round(Epredicted/Einput, 4)
        newEpredicted = Einput * vec_SFs_rounded
        vec_SFs_rounded += 0.0001 * ((Epredicted - newEpredicted) > 0)

        SFs = (vec_SFs_rounded).reshape(int(max_energy_tower-min_energy_tower)+1,28)
        SFs[np.isinf(SFs)] = 0.0000 # replace the infs form the 3/6/9 zero suppression trick with zeros
        SFs[np.isnan(SFs)] = 0.0000 # replace the infs form the 3/6/9 zero suppression trick with zeros

        # change binning of Scale Factors a posteriori

        SFs_new = []
        SFs_new.append(SFs[0])
        for i in range(1,max_energy):
            if (i%energy_step == 0):
                SFs_new.append(SFs[i])

        head_text = 'energy bins iEt       = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(i)
        head_text = head_text + " , 256]\n"

        head_text = head_text + 'energy bins GeV       = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(i/2)
        head_text = head_text + " , 256]\n"

        head_text = head_text + 'energy bins GeV (int) = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(int(i/2))
        head_text = head_text + " , 256]\n"

        SFOutFile = odir + '/ScaleFactors_' + reg + '_energystep'+str(energy_step)+'iEt'+epoch+'.csv'
        np.savetxt(SFOutFile, SFs_new, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*28))
        print('\nScale Factors saved to: {}'.format(SFOutFile))

    if reg == "HF":
        eta_towers = [i for i in range(29,40+1)]
        input_towers = []

        # always comput all the scale factors
        min_energy_tower = 1
        max_energy_tower = 256
        input_towers = []
        for i_energy in np.array(range(min_energy_tower, max_energy_tower+1, 1)):
            for i_eta in eta_towers:
                one_hot_tower = np.array([i_energy] + [0 if j != i_eta else 1 for j in range(1,40+1)])
                input_towers.append(one_hot_tower)
        input_towers = np.array(input_towers)
        Einput = input_towers[:,0].reshape(-1,1)
        Epredicted = TTP.predict(input_towers)

        vec_SFs_rounded = np.round(Epredicted/Einput, 4)
        newEpredicted = Einput * vec_SFs_rounded
        vec_SFs_rounded += 0.0001 * ((Epredicted - newEpredicted) > 0)

        SFs = (vec_SFs_rounded).reshape(int(max_energy_tower-min_energy_tower)+1,12)
        SFs[np.isinf(SFs)] = 0.0000 # replace the infs form the 3/6/9 zero suppression trick with zeros
        SFs[np.isnan(SFs)] = 0.0000 # replace the infs form the 3/6/9 zero suppression trick with zeros

        SFs_new = []
        SFs_new.append(SFs[0])
        for i in range(1,max_energy):
            if (i%energy_step == 0):
                SFs_new.append(SFs[i])

        head_text = 'energy bins iEt       = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(i)
        head_text = head_text + " , 256]\n"
        
        head_text = head_text + 'energy bins GeV       = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(i/2)
        head_text = head_text + " , 256]\n"

        head_text = head_text + 'energy bins GeV (int) = [0'
        for i in range(min_energy, max_energy, energy_step):
            head_text = head_text + ' ,{}'.format(int(i/2))
        head_text = head_text + " , 256]\n"

        SFOutFile = odir + '/ScaleFactors_' + reg + '_energystep'+str(energy_step)+'iEt'+epoch+'.csv'
        np.savetxt(SFOutFile, SFs_new, delimiter=",", newline=',\n', header=head_text, fmt=','.join(['%1.4f']*12))
        print('\nScale Factors saved to: {}'.format(SFOutFile))

    return SFOutFile

### To run:
### python3 CalibrationFactor.py --in 2022_04_21_NtuplesV1 --v ECAL 

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",      dest="indir",      help="Input folder with trained model",             default=None                       )
    parser.add_option("--tag",        dest="tag",        help="tag of the training folder",                  default=""                         )
    parser.add_option("--out",        dest="odir",       help="Output folder",                               default=None                       )
    parser.add_option("--v",          dest="v",          help="Ntuple type ('ECAL' or 'HCAL')",              default='ECAL'                     )
    parser.add_option("--reg",        dest="reg",        help="Ntuple type ('ECAL' or 'HCAL' or 'HF'')",     default='ECAL'                     )
    parser.add_option("--maxenergy",  dest="maxenergy",  help="Energy tower max",                type=int,   default=200                        )
    parser.add_option("--energystep", dest="energystep", help="Energy steps",                    type=int,   default=1                          )
    parser.add_option("--addtag",     dest="addtag",     help="Add tag to distinguish different trainings",  default="",                        )
    (options, args) = parser.parse_args()
    print(options)

    # Definition of the trained model
    indir = '/data_CMS/cms/motta/CaloL1calibraton/' + options.indir + '/' + options.v + 'training' + options.tag
    modeldir = indir + '/model_' + options.v + options.addtag
    print('\nModel dir = {}\n'.format(modeldir))

    TTP = keras.models.load_model(modeldir + '/TTP', compile=False, custom_objects={'Fgrad': Fgrad})

    # Definition of the output folder
    if options.odir:
        odir = options.odir
    else:
        odir = modeldir + '/SFs_' + str(options.energystep) + 'iEt'
    os.system('mkdir -p '+ odir)
    print('\nOutput dir = {}\n'.format(odir))

    reg = options.reg
    min_energy = 1
    max_energy = options.maxenergy
    energy_step = options.energystep
    
    ExtractSFs(TTP, reg, min_energy, max_energy, energy_step, odir, i_epoch = None)

