########################################################################################################################
# HCAL TRAININGS
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_1 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.75 --scaleHF 0.75 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_1
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_1

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_2 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.8 --scaleHF 0.8 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_2
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_2

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_3 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --scaleHF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_3
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_3

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_4 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --scaleHF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_4
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_4

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_5 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.75 --scaleHF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_5
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_5

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_6 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.75 --scaleHF 1.5 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_6
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_6

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_7 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.82 --scaleHF 1 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_7
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_7

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/JetMET_Run2023B_PuppiJet_Pt30_HoTot70/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_HCAL_8 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 0.82 --scaleHF 1.5 --v HCAL
source Instructions/TestsTrainingHCAL.sh JAX_HCAL_8
source Instructions/TestsPerformanceHCAL.sh JAX_HCAL_8

########################################################################################################################
# ECAL TRAININGS (full stats 5353702)
########################################################################################################################

python3 JaxOptimizer.py --indir 2024_02_15_NtuplesV58/EGamma_Run2023*_LooseEle_EoTot80/GoodNtuples/tensors \
    --odir Trainings_2023/JAX_ECAL_1 --jetsLim 1000000 --lr 0.5 --bs 4096 --ep 100 --scale 1 --v ECAL
source Instructions/TestsTrainingECAL.sh JAX_ECAL_1
source Instructions/TestsPerformanceECAL.sh JAX_ECAL_1

########################################################################################################################
# ECAL TRAININGS
########################################################################################################################

source Instructions/TestsTrainingHCAL.sh ECALv33_HCALv51_HFv52_Best
source Instructions/TestsPerformanceHCAL.sh ECALv33_HCALv51_HFv52_Best

source Instructions/TestsTrainingECAL.sh ECALv33_HCALv51_HFv52_Best
source Instructions/TestsPerformanceECAL.sh ECALv33_HCALv51_HFv52_Best

