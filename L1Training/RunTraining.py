import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 RunTraining.py --addtag _A

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--addtag",           dest="addtag",                                                                 default=''                           )
parser.add_option("--epochs",           dest="epochs",           help="Number of epochs for the training",             default='20',    type=str            )
parser.add_option("--MaxLR",            dest="MaxLR",            help="Maximum learning rate",                         default='1E-3'                       )
parser.add_option("--batch_size",       dest="batch_size",       help="Batch size for the training",                   default='256',   type=str            )
parser.add_option("--ThrRate",          dest="ThrRate",          help="Threshold for rate proxy",                      default='40'                         )
parser.add_option("--weight_loss",      dest="weight_loss",      help="Type of weight loss [abs,sqr]",                 default='abs'                        )
parser.add_option("--add_iem",          dest="add_iem",          help="Add iem to the training loss",                  default=False,    action='store_true')
parser.add_option("--eventLim",         dest="eventLim",         help="Maximum number of events to use",               default='20000'                      )
(options, args) = parser.parse_args()

if not options.add_iem:
    NNModel = 'NNModel_RegAndRate.py'
else:
    NNModel = 'NNModel_RegAndRate_AddEt.py'

run = True
indir1 = '2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95'
indir2 = '2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70'
indir3 = '2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70'
indir4 = '2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70'

for i, indir in enumerate([indir1, indir2, indir3, indir4]):
    log_file = os.getcwd() + '/RunInstructions/Training_Input' + str(i+1) + options.addtag + '.sh'

    cmd = []
    cmd.append('loadGPUtf \n')

    cmd.append('python3 ' + NNModel + ' --indir ' + indir + ' \\')
    cmd.append(' --v HCAL --tag DataReco' + ' --addtag ' + options.addtag + ' --epochs ' + options.epochs + ' \\')
    cmd.append(' --MaxLR ' + options.MaxLR + ' --batch_size ' + options.batch_size + ' --ThrRate ' + options.ThrRate + '\n')

    cmd.append('python3 CalibrationFactor.py --indir ' + indir1 + ' --v HCAL --tag DataReco --reg HCAL --energystep 2 --addtag ' + options.addtag + '\n')
    cmd.append('python3 CalibrationFactor.py --indir ' + indir1 + ' --v HCAL --tag DataReco --reg HF --energystep 2 --addtag ' + options.addtag + '\n')

    cmd.append('python3 ProduceCaloParams.py --name caloParams_2023_v56' + options.addtag + '_Input' + str(i+1) + '_cfi \\')
    cmd.append(' --base caloParams_2023_v0_2_noL1Calib_cfi.py \\')
    cmd.append(' --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \\')
    cmd.append(' --HCAL /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HCAL_energystep2iEt.csv \\')
    cmd.append(' --HF   /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HF_energystep2iEt.csv \n')
    
    file = open (log_file, 'w')
    for line in cmd:
        file.write(line + '\n')
    file.close()