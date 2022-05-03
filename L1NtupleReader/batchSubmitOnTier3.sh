source /opt/exp_soft/cms/t3/t3setup

python batchSubmitOnTier3.py --doEG0_200 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doEG0_200 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doEG0_200 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNewECALcalib

python batchSubmitOnTier3.py --doEG200_500 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doEG200_500 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doEG200_500 --jetcut 60 --etacut 24 --ecalcut True --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNewECALcalib

python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "50To80" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "50To80" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "50To80" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNewECALcalib

python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "80To120" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "80To120" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "80To120" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNewECALcalib

python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "120To170" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "120To170" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doQCDnoPU --qcdPtBin "120To170" --etacut 37 --indir 2022_04_30_NtuplesV7 --applyHCALpfa1p --applyNewECALcalib


python batchSubmitOnTier3.py --doQCDpu --indir 2022_04_30_NtuplesV7 --odir --applyHCALpfa1p --applyNoCalib
python batchSubmitOnTier3.py --doQCDpu --indir 2022_04_30_NtuplesV7 --odir --applyHCALpfa1p --applyOldCalib
python batchSubmitOnTier3.py --doQCDpu --indir 2022_04_30_NtuplesV7 --odir --applyHCALpfa1p --applyNewECALcalib