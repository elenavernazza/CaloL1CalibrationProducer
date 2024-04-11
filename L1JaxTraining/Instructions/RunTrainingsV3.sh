########################################################################################################################
# TEST ECAL 
########################################################################################################################

# first line to 1 to fix nTT probelm
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_24 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v ECAL --maskLE 2
source Instructions/TestsTrainingECAL.sh JAX_ECAL_24
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_24 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_24
source Instructions/MoveToEos.sh JAX_ECAL_24 ECAL

# first two lines to 1 (to reproduce Olivier's results)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/EGamma_Run2023D_LooseEle_EoTot80_Cluster/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_25 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v ECAL --maskLE 4
source Instructions/TestsTrainingECAL.sh JAX_ECAL_25
python3 PlotHistory.py --indir Trainings_2023/JAX_ECAL_25 --v ECAL --loss
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_25
source Instructions/MoveToEos.sh JAX_ECAL_25 ECAL

########################################################################################################################
# TEST HCAL 
########################################################################################################################

# try to reproduce Olivier's results with lower scale
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_61 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_25/ScaleFactors_ECAL_Phys.csv --maskHF --scaleB 0.75 scaleE 0.7 --maskLE 10
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_61
source Instructions/TestTrainingCombination.sh ECAL_25 HCAL_61
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_61 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_61
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_25_HCAL_61
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_25_HCAL_61
source Instructions/MoveToEos.sh JAX_HCAL_61 HCAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_61 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_61 HCAL

# same configuration as V51 (no HF masking) + ECAL 25 (first 2 lines to 1)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_62 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_25/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_62
source Instructions/TestTrainingCombination.sh ECAL_25 HCAL_62
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_62 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_62
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_25_HCAL_62
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_25_HCAL_62
source Instructions/MoveToEos.sh JAX_HCAL_62 HCAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_62 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_62 HCAL

# same configuration as V51 (no HF masking) + ECAL 24 (first line to 1)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_63 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL \
    --ECALCalib Trainings_2023/JAX_ECAL_24/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_63
source Instructions/TestTrainingCombination.sh ECAL_24 HCAL_63
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_63 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_63
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_24_HCAL_63
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_24_HCAL_63
source Instructions/MoveToEos.sh JAX_HCAL_63 HCAL
source Instructions/MoveToEos.sh JAX_ECAL_24_HCAL_63 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_24_HCAL_63 HCAL

# same configuration as V57 (HF masking 3.5) + ECAL 25 (first 2 lines to 1)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_64 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_25/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_64
source Instructions/TestTrainingCombination.sh ECAL_25 HCAL_64
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_64 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_64
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_25_HCAL_64
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_25_HCAL_64
source Instructions/MoveToEos.sh JAX_HCAL_64 HCAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_64 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_25_HCAL_64 HCAL

# same configuration as V57 (HF masking 3.5) + ECAL 24 (first line to 1)
python3 JaxOptimizer.py --indir 2024_03_05_NtuplesV59/JetMET_Run2023D_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_65 --jetsLim 1000000 --lr 1 --bs 4096 --ep 50 --v HCAL --maskHF \
    --ECALCalib Trainings_2023/JAX_ECAL_24/ScaleFactors_ECAL_Phys.csv
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_65
source Instructions/TestTrainingCombination.sh ECAL_24 HCAL_65
python3 PlotHistory.py --indir Trainings_2023/JAX_HCAL_65 --v HCAL --loss
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_65
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_24_HCAL_65
source Instructions/TestsPerformanceHCAL.sh JAX_ECAL_24_HCAL_65
source Instructions/MoveToEos.sh JAX_HCAL_65 HCAL
source Instructions/MoveToEos.sh JAX_ECAL_24_HCAL_65 ECAL
source Instructions/MoveToEos.sh JAX_ECAL_24_HCAL_65 HCAL