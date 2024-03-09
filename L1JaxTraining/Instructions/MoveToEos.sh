#!/usr/bin/bash
# seteos

# source Instructions/MoveToEos.sh JAX_HCAL_17 HCAL
# source Instructions/MoveToEos.sh JAX_HCAL_20 HCAL
# source Instructions/MoveToEos.sh JAX_ECAL_11 ECAL
# source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_17 HCAL
# source Instructions/MoveToEos.sh JAX_ECAL_11_HCAL_17 ECAL

number="$1"
version="$2"
if [ -n "$3" ]; then
    suffix=$3
else
    suffix="L1ptNoSatu"
fi

www='/eos/home-e/evernazz/www/L1Trigger/PerformancePlots/JAXV1/'

mkdir -p "${www}"/"${number}"
cp /eos/home-e/evernazz/www/L1Trigger/PerformancePlots/JAXV1/index.php "${www}"/"${number}"

if [ "$version" == "HCAL" ]; then

    cp Trainings_2023/"${number}"/Calib_vs_Eta_HCAL* "${www}"/"${number}"
    cp Trainings_2023/"${number}"/SFs_2D_HCAL* "${www}"/"${number}"
    cp Trainings_2023/"${number}"/ScaleFactors_HCAL.csv "${www}"/"${number}"
    cp Trainings_2023/"${number}"/ScaleFactors_HCAL_Phys.csv "${www}"/"${number}"

    mkdir -p "${www}"/"${number}"/PerformanceJet
    cp /eos/home-e/evernazz/www/L1Trigger/PerformancePlots/JAXV1/index.php "${www}"/"${number}"/PerformanceJet
    cp /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/"${number}"/NtuplesVnew/PerformancePlots"${suffix}"/PNGs/comparisons__jet/* "${www}"/"${number}"/PerformanceJet
    cp /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/"${number}"/NtuplesVnew/PerformancePlots"${suffix}"/PDFs/comparisons__jet/* "${www}"/"${number}"/PerformanceJet

else

    cp Trainings_2023/"${number}"/Calib_vs_Eta_ECAL* "${www}"/"${number}"
    cp Trainings_2023/"${number}"/SFs_2D_ECAL* "${www}"/"${number}"
    cp Trainings_2023/"${number}"/ScaleFactors_ECAL.csv "${www}"/"${number}"
    cp Trainings_2023/"${number}"/ScaleFactors_ECAL_Phys.csv "${www}"/"${number}"

    mkdir -p "${www}"/"${number}"/PerformanceEle
    cp /eos/home-e/evernazz/www/L1Trigger/PerformancePlots/JAXV1/index.php "${www}"/"${number}"/PerformanceEle
    cp /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/"${number}"/NtuplesVnew/PerformancePlotsL1pt/PNGs/comparisons__ele/* "${www}"/"${number}"/PerformanceEle
    cp /data_CMS/cms/motta/CaloL1calibraton/2024_03_05_NtuplesV59/"${number}"/NtuplesVnew/PerformancePlotsL1pt/PDFs/comparisons__ele/* "${www}"/"${number}"/PerformanceEle

fi