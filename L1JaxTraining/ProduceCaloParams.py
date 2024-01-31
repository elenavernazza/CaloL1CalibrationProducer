import os,sys

#######################################################################
######################### SCRIPT BODY #################################
#######################################################################

'''
python3 ProduceCaloParams.py --name caloParams_2023_v51A_newCalib_cfi \
    --ECAL /data_CMS/cms/motta/CaloL1calibraton/2023_06_21_NtuplesV51/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/data_A/ScaleFactors_HCAL_energystep2iEt.csv \
    --HF /data_CMS/cms/motta/CaloL1calibraton/2023_06_21_NtuplesV51/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco/data_A/ScaleFactors_HF_energystep2iEt.csv \
    --HCAL /data_CMS/cms/motta/CaloL1calibraton/2023_06_21_NtuplesV51/JetMET_PuppiJet_BarrelEndcap_Pt30_HoTot95/HCALtrainingDataReco_A/ScaleFactors_HCAL_energystep2iEt.csv \

python3 ProduceCaloParams.py --name caloParams_2023_JAX4_newCalib_cfi \
    --HCAL /data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/L1JaxTraining/4/ScaleFactors_HCAL.csv \
'''

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--name",      dest="name",       default='caloParams_2023_vX_newCalib_cfi')
parser.add_option("--base",      dest="base",       default='caloParams_2023_v0_2_noL1Calib_cfi.py')
parser.add_option("--ECAL",      dest="ECAL",       default=None)
parser.add_option("--HCAL",      dest="HCAL",       default=None)
parser.add_option("--HF",        dest="HF",         default=None)
parser.add_option("--cureSFs",   dest="cureSFs",    default=False,      action='store_true')
(options, args) = parser.parse_args()

# prepare caloParams file
base_dir = os.getcwd().split('/L1JaxTraining')[0] + '/caloParams/'

base_file = base_dir + options.base
new_file = base_dir + options.name + '.py'

print('\n### INFO: Producing new calo params file : {}'.format(new_file))
print('### INFO: Reference calo params file : {}\n'.format(base_file))

if os.path.exists(new_file):
    print("This file already exists: {}".format(new_file))
    write = input("Do you want to over-write it? (y/n)\n")
    if write != 'y':
        sys.exit()

print('### INFO: Adding first part')
f_base = open(base_file)
Old_Lines = f_base.readlines()
New_Lines = []

start_ECAL = [index for index, value in enumerate(Old_Lines) if 'layer1ECalScaleETBins = cms.' in value][0]
start_HCAL = [index for index, value in enumerate(Old_Lines) if 'layer1HCalScaleETBins = cms.' in value][0]
start_HF   = [index for index, value in enumerate(Old_Lines) if 'layer1HFScaleETBins = cms.' in value][0]
end_ECAL = [index for index, value in enumerate(Old_Lines) if '    ]),' in value][0]
end_HCAL = [index for index, value in enumerate(Old_Lines) if '    ]),' in value][1]
end_HF   = [index for index, value in enumerate(Old_Lines) if '    ]),' in value][2]

for line in Old_Lines[:start_ECAL]:
    New_Lines.append(line)

print('### INFO: Adding ECAL')
if options.ECAL:
    f_ECAL = options.ECAL
    with open(f_ECAL) as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                et_binning = line.split("[0 ,")[1].split("]")[0]
                first_part = "    layer1ECalScaleETBins = cms.vint32([ "
                last_part = "]),\n"
                New_Lines.append(first_part + et_binning + last_part)
                New_Lines.append("    layer1ECalScaleFactors = cms.vdouble([\n")
            if '#' in line: continue
            New_Lines.append('        ' + line)
else:
    for line in Old_Lines[start_ECAL:end_ECAL]:
        New_Lines.append(line)

for line in Old_Lines[end_ECAL:start_HCAL]:
    New_Lines.append(line)

print('### INFO: Adding HCAL')
if options.HCAL:
    f_HCAL = options.HCAL
    with open(f_HCAL) as f:
        first_line = True
        for i, line in enumerate(f.readlines()):
            if i == 0:
                et_binning = line.split("[0 ,")[1].split("]")[0]
                first_part = "    layer1HCalScaleETBins = cms.vint32([ "
                last_part = "]),\n"
                New_Lines.append(first_part + et_binning + last_part)
                New_Lines.append("    layer1HCalScaleFactors = cms.vdouble([\n")
            if '#' in line: continue
            if first_line == True:
                print("### INFO: Apply Zero Suppression\n")
                print(" --> BEFORE: ", line)
                SF_zs = line.split(",")[:28]
                SF_zs[:15] = ["0.0000"] * 15
                if options.cureSFs:
                    print("### INFO: Apply Ones to all iEt = 1\n")
                    SF_zs[15:28] = ["1.0000"] * 13
                line_to_add = ",".join(SF_zs)
                print(" --> AFTER:  ", line_to_add)
                New_Lines.append('        ' + line_to_add + ',\n')
                first_line = False
            else:
                SF = line.split(",")[:28]
                line_to_add = ",".join(SF)
                New_Lines.append('        ' + line_to_add + ',\n')
else:
    for line in Old_Lines[start_HCAL:end_HCAL]:
        New_Lines.append(line)

for line in Old_Lines[end_HCAL:start_HF]:
    New_Lines.append(line)

print('### INFO: Adding HF')
if options.HCAL:
    f_HF = options.HCAL
    with open(f_HF) as f:
        first_line = True
        for i, line in enumerate(f.readlines()):
            if i == 0:
                et_binning = line.split("[0 ,")[1].split("]")[0]
                first_part = "    layer1HFScaleETBins = cms.vint32([ "
                last_part = "]),\n"
                New_Lines.append(first_part + et_binning + last_part)
                New_Lines.append("    layer1HFScaleFactors = cms.vdouble([\n")
            if '#' in line: continue
            if first_line == True:
                SF_zs = line.split(",")[28:40]
                if options.cureSFs:
                    print("### INFO: Apply Ones to all iEt = 1\n")
                    print(" --> BEFORE: ", line)
                    SF_zs = line.split(",")[28:40]
                    SF_zs[28:40] = ["1.0000"] * 12
                line_to_add = ",".join(SF_zs)
                if options.cureSFs: 
                    print(" --> AFTER:  ", line_to_add)
                New_Lines.append('        ' + line_to_add + ',\n')
                first_line = False
            else:
                SF = line.split(",")[28:40]
                line_to_add = ",".join(SF)
                New_Lines.append('        ' + line_to_add + ',\n')
else:
    for line in Old_Lines[start_HF:end_HF]:
        New_Lines.append(line)

for line in Old_Lines[end_HF:]:
    New_Lines.append(line)

print('### INFO: Writing')
with open(new_file, 'w') as file:
    for line in New_Lines:
        file.write(line)

cmd = 'cp '+new_file+' ../../L1Trigger/L1TCalorimeter/python/'
print('cp '+new_file+' ../../L1Trigger/L1TCalorimeter/python/')
# os.system(cmd)
print('### INFO: DONE!')