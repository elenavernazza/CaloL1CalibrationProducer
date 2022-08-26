python NNModelTraining_FlooringInTTP.py --indir 2022_07_20_NtuplesV23 --v ECAL --tag _0pt500
sleep 5
python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --maxeta 28 --v ECAL --tag _0pt500 --padZeros
sleep 5

python NNModelTraining_FlooringInTTP.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _30pt1000
sleep 5
python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --v HCAL --tag _30pt1000 --padZeros
sleep 5

# python NNModelTraining_FlooringInTTP.py --indir 2022_07_20_NtuplesV23 --v ECAL --tag _0pt200
# sleep 5
# python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --maxeta 28 --v ECAL --tag _0pt200 --padZeros
# sleep 5

# python NNModelTraining_FlooringInTTP.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _30pt500
# sleep 5
# python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --v HCAL --tag _30pt500 --padZeros
# sleep 5

# python NNModelTraining_FlooringInTTP.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _20pt1000
# sleep 5
# python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --v HCAL --tag _20pt1000 --padZeros
# sleep 5



# python3 ModelPlots.py --indir 2022_07_20_NtuplesV23 --v ECAL --tag _0pt500
# python3 ModelPlots.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _30pt1000
# python3 ModelPlots.py --indir 2022_07_20_NtuplesV23 --v ECAL --tag _0pt200
# python3 ModelPlots.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _30pt500
# python3 ModelPlots.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _20pt1000

# python3 ModelPlots.py --indir 2022_06_14_NtupleV21 --v HCAL --tag _30pt1000_eta41_Lbound0p95

# python3 ModelPlots.py --indir 2022_07_12_NtupleV22 --v HCAL --tag _30pt1000_eta41_nTT





# python NNModelTraining_FlooringInTTP_SoftSaturationInTTP.py --indir 2022_07_20_NtuplesV23 --v HCAL --tag _30pt1000_softSaturInTTP --proxyMinEta 16 --proxyMaxEta 28 --proxyMinE 3 --proxyMaxE 6
# sleep 5
# python CalibrationFactor.py --indir 2022_07_20_NtuplesV23 --start 1 --stop 200 --v HCAL --tag _30pt1000_softSaturInTTP --padZeros
# sleep 5