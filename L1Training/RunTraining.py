import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

# python3 RunTraining.py --addtag _A --indir 1
# python3 RunTraining.py --addtag _B --indir 2,3,4 --add_iem
# python3 RunTraining.py --addtag _C --indir 2 --model_py NNModel_RegAndRate_AddEt_1.py
# python3 RunTraining.py --addtag _D --indir 2 --model_py NNModel_RegAndRate_AddEt_2.py
# python3 RunTraining.py --addtag _D1 --indir 2 --model_py NNModel_RegAndRate_AddEt_2.py --regr_w 0.01
# python3 RunTraining.py --addtag _D2 --indir 2 --model_py NNModel_RegAndRate_AddEt_2.py --regr_w 0.1

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--indir",            dest="indir",                                                                  default='1,2,3,4'                    )
parser.add_option("--addtag",           dest="addtag",                                                                 default=''                           )
parser.add_option("--epochs",           dest="epochs",           help="Number of epochs for the training",             default='20',    type=str            )
parser.add_option("--MaxLR",            dest="MaxLR",            help="Maximum learning rate",                         default='1E-3'                       )
parser.add_option("--batch_size",       dest="batch_size",       help="Batch size for the training",                   default='256',   type=str            )
parser.add_option("--ThrRate",          dest="ThrRate",          help="Threshold for rate proxy",                      default='40'                         )
# parser.add_option("--weight_loss",      dest="weight_loss",      help="Type of weight loss [abs,sqr]",                 default='abs'                        )
parser.add_option("--add_iem",          dest="add_iem",          help="Add iem to the training loss",                  default=False,    action='store_true')
parser.add_option("--model_py",         dest="model_py",         help="Python script to be used for the training",     default=None)
parser.add_option("--regr_w",           dest="regr_w",           help="Multiplicative parameter for regression",       default=500,     type=float          )
parser.add_option("--weig_w",           dest="weig_w",           help="Multiplicative parameter for regularization",   default=1,       type=float          )
parser.add_option("--rate_w",           dest="rate_w",           help="Multiplicative parameter for rate",             default=1,       type=float          )
(options, args) = parser.parse_args()

if not options.model_py:
    if not options.add_iem:
        NNModel = 'NNModel_RegAndRate.py'
    else:
        NNModel = 'NNModel_RegAndRate_AddEt.py'
else:
    NNModel = options.model_py

run = True
indir1 = '2023_12_13_NtuplesV56/Input1/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95'
indir2 = '2023_12_13_NtuplesV56/Input2/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot70'
indir3 = '2023_12_13_NtuplesV56/Input3/JetMET_PuppiJet_BarrelEndcap_Pt60_HoTot70'
indir4 = '2023_12_13_NtuplesV56/Input4/JetMET_PuppiJet_BarrelEndcap_PtRaw60_HoTot70'

indirs = [indir1, indir2, indir3, indir4]

for i in options.indir.split(','):

    indir = indirs[int(i)-1]
    log_file = os.getcwd() + '/RunInstructions/Training_Input' + i + options.addtag + '.sh'

    cmd = []
    cmd.append('loadGPUtf \n')

    cmd.append('python3 ' + NNModel + ' --indir ' + indir + ' \\')
    cmd.append(' --v HCAL --tag DataReco' + ' --addtag ' + options.addtag + ' --epochs ' + options.epochs + ' \\')
    cmd.append(' --MaxLR ' + options.MaxLR + ' --batch_size ' + options.batch_size + ' --ThrRate ' + options.ThrRate + ' \\')
    cmd.append(' --regr_w ' + str(options.regr_w) + ' --weig_w ' + str(options.weig_w) + ' --rate_w ' + str(options.rate_w) + '\n')

    cmd.append('python3 CalibrationFactor.py --indir ' + indir + ' --v HCAL --tag DataReco --reg HCAL --energystep 2 --addtag ' + options.addtag + '\n')
    cmd.append('python3 CalibrationFactor.py --indir ' + indir + ' --v HCAL --tag DataReco --reg HF --energystep 2 --addtag ' + options.addtag + '\n')

    cmd.append('python3 ModelPlots.py --indir ' + indir + ' --v HCAL --tag DataReco --energystep 2 --addtag ' + options.addtag + '\n')

    cmd.append('python3 ProduceCaloParams.py --name caloParams_2023_v56' + options.addtag + '_Input' + i + '_cfi \\')
    cmd.append(' --base caloParams_2023_v0_2_noL1Calib_cfi.py \\')
    cmd.append(' --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_03_06_NtuplesV33/ECALtrainingDataReco_normalOrder/data/ScaleFactors_ECAL_energystep2iEt.csv \\')
    cmd.append(' --HCAL /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HCAL_energystep2iEt.csv \\')
    cmd.append(' --HF   /data_CMS/cms/motta/CaloL1calibraton/' + indir + '/HCALtrainingDataReco/model_HCAL' + options.addtag + '/SFs_2iEt/ScaleFactors_HF_energystep2iEt.csv \n')
    
    # Re-emulation NEW of jets
    cmd.append('cd ../L1NtupleLauncher \n')
    run = '' # or '# '
    cmd.append(run + 'python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \\')
    cmd.append(run + ' --outTag GT130XdataRun3Promptv3_CaloParams2023v56' + options.addtag + '_Input' + i + '_data_reco_json \\')
    cmd.append(run + ' --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \\')
    cmd.append(run + ' --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \\')
    cmd.append(run + ' --caloParams caloParams_2023_v56' + options.addtag + '_Input' + i + '_cfi \n')

    # Re-emulation NEW of zero-bias
    run = '' # or '# '
    cmd.append(run + 'python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \\')
    cmd.append(run + ' --outTag GT130XdataRun3Promptv3_CaloParams2023v56' + options.addtag + '_Input' + i + '_data \\')
    cmd.append(run + ' --nJobs 31 --queue short --maxEvts 5000 \\')
    cmd.append(run + ' --globalTag 130X_dataRun3_Prompt_v3 --data \\')
    cmd.append(run + ' --caloParams caloParams_2023_v56' + options.addtag + '_Input' + i + '_cfi \n')

    # Re-emulation OLD of jets
    run = '# ' # or '# '
    cmd.append(run + 'python3 submitOnTier3.py --inFileList JetMET__Run2022G-PromptReco-v1__Run362617__AOD \\')
    cmd.append(run + ' --outTag GT130XdataRun3Promptv3_CaloParams2023v02_data_reco_json \\')
    cmd.append(run + ' --nJobs 31 --queue short --maxEvts 5000 --inJson Cert_Collisions2022_355100_362760_Golden \\')
    cmd.append(run + ' --globalTag 130X_dataRun3_Prompt_v3 --data --recoFromAOD \\')
    cmd.append(run + ' --caloParams caloParams_2023_v0_2_cfi \n')

    # Re-emulation OLD of zero-bias
    run = '# ' # or '# '
    cmd.append(run + 'python3 submitOnTier3.py --inFileList EphemeralZeroBias0__Run2022G-v1__Run362617__RAW \\')
    cmd.append(run + ' --outTag GT130XdataRun3Promptv3_CaloParams2023v02_data \\')
    cmd.append(run + ' --nJobs 31 --queue short --maxEvts 5000 \\')
    cmd.append(run + ' --globalTag 130X_dataRun3_Prompt_v3 --data \\')
    cmd.append(run + ' --caloParams caloParams_2023_v0_2_cfi \n')

    cmd.append('cd - \n')

    file = open (log_file, 'w')
    for line in cmd:
        file.write(line + '\n')
    file.close()
