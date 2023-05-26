import FWCore.ParameterSet.Config as cms

from L1Trigger.L1TCalorimeter.caloParams_cfi import caloParamsSource
import L1Trigger.L1TCalorimeter.caloParams_cfi
caloStage2Params = L1Trigger.L1TCalorimeter.caloParams_cfi.caloParams.clone(

    # EG
    egHcalThreshold            = 0.,
    egTrimmingLUTFile          = "L1Trigger/L1TCalorimeter/data/egTrimmingLUT_10_v16.01.19.txt",
    egHOverEcutBarrel          = 3,
    egHOverEcutEndcap          = 4,
    egBypassExtHOverE          = 0,
    egMaxHOverELUTFile         = "L1Trigger/L1TCalorimeter/data/HoverEIdentification_0.995_v15.12.23.txt",
    egCompressShapesLUTFile    = "L1Trigger/L1TCalorimeter/data/egCompressLUT_v4.txt",
    egShapeIdType              = "compressed",
    egShapeIdLUTFile           = "L1Trigger/L1TCalorimeter/data/shapeIdentification_adapt0.99_compressedieta_compressedE_compressedshape_v15.12.08.txt", #Not used any more in the current emulator version, merged with calibration LUT

    egIsolationType            = "compressed",
    egIsoLUTFile               = "L1Trigger/L1TCalorimeter/data/EG_Iso_LUT_Flat_WP_v2_Tight1358_20p0_0p7_40p0_v1_APR23.txt",
    egIsoLUTFile2              = "L1Trigger/L1TCalorimeter/data/EG_Iso_LUT_Flat_WP_v2_Loose610_10p0_0p7_40p0_v1_APR23.txt",

    egIsoVetoNrTowersPhi       = 2,
    egPUSParams                = cms.vdouble(1,4,32), #Isolation window in firmware goes up to abs(ieta)=32 for now
    egCalibrationType          = "compressed",
    egCalibrationVersion       = 0,
    egCalibrationLUTFile       = "L1Trigger/L1TCalorimeter/data/EG_Calibration_LUT_correctedEtCalibLUT_v1_APR2023.txt",

    # Tau
    isoTauEtaMax               = 25,
    tauSeedThreshold           = 0.,
    tauIsoLUTFile              = "L1Trigger/L1TCalorimeter/data/Tau_Iso_LUT_2023_calibThr1p7_V2gs_effMin0p9_eMin16_eMax60.txt",
    tauIsoLUTFile2             = "L1Trigger/L1TCalorimeter/data/Tau_Iso_LUT_2023_calibThr1p7_V2gs_effMin0p9_eMin16_eMax60.txt",
    tauCalibrationLUTFile      = "L1Trigger/L1TCalorimeter/data/Tau_Cal_LUT_2023_calibThr1p7_V2.txt",
    tauCompressLUTFile         = "L1Trigger/L1TCalorimeter/data/tauCompressAllLUT_12bit_v3.txt",
    tauPUSParams               = [1,4,32],

    # jets
    jetSeedThreshold           = 4.0,
    jetPUSType                 = "ChunkyDonut",

    # Calibration options
    jetCalibrationType         = "LUT",
    jetCompressPtLUTFile       = "L1Trigger/L1TCalorimeter/data/lut_pt_compress_2017v1.txt",
    jetCompressEtaLUTFile      = "L1Trigger/L1TCalorimeter/data/lut_eta_compress_2017v1.txt",
    jetCalibrationLUTFile      = "L1Trigger/L1TCalorimeter/data/lut_calib_2022v5_ECALZS_noHFJEC.txt",


    # sums: 0=ET, 1=HT, 2=MET, 3=MHT
    etSumEtaMin             = [1, 1, 1, 1, 1],
    etSumEtaMax             = [28,  26, 28,  26, 28],
    etSumEtThreshold        = [0.,  30.,  0.,  30., 0.], # only 2nd (HT) and 4th (MHT) values applied
    etSumMetPUSType         = "LUT", # et threshold from this LUT supercedes et threshold in line above
    etSumBypassEttPUS       = 1,
    etSumBypassEcalSumPUS   = 1,

    etSumMetPUSLUTFile               = "L1Trigger/L1TCalorimeter/data/metPumLUT_2022_HCALOff_p5.txt",


    # Layer 1 SF
    layer1ECalScaleETBins = cms.vint32([3, 6, 9, 12, 15, 20, 25, 30, 35, 40, 45, 55, 70, 256]),
    layer1ECalScaleFactors = cms.vdouble([
        1.12, 1.13, 1.13, 1.12, 1.12, 1.12, 1.13, 1.12, 1.13, 1.12, 1.13, 1.13, 1.14, 1.13, 1.13, 1.13, 1.14, 1.26, 1.11, 1.20, 1.21, 1.22, 1.19, 1.20, 1.19, 0.00, 0.00, 0.00,
        1.12, 1.13, 1.13, 1.12, 1.12, 1.12, 1.13, 1.12, 1.13, 1.12, 1.13, 1.13, 1.14, 1.13, 1.13, 1.13, 1.14, 1.26, 1.11, 1.20, 1.21, 1.22, 1.19, 1.20, 1.19, 1.22, 0.00, 0.00,
        1.08, 1.09, 1.08, 1.08, 1.11, 1.08, 1.09, 1.09, 1.09, 1.09, 1.15, 1.09, 1.10, 1.10, 1.10, 1.10, 1.10, 1.23, 1.07, 1.15, 1.14, 1.16, 1.14, 1.14, 1.15, 1.14, 1.14, 0.00, 
        1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.06, 1.07, 1.07, 1.07, 1.07, 1.07, 1.08, 1.07, 1.09, 1.08, 1.17, 1.06, 1.11, 1.10, 1.13, 1.10, 1.10, 1.11, 1.11, 1.11, 1.09, 
        1.04, 1.05, 1.04, 1.05, 1.04, 1.05, 1.06, 1.06, 1.05, 1.05, 1.05, 1.06, 1.06, 1.06, 1.06, 1.06, 1.07, 1.15, 1.04, 1.09, 1.09, 1.10, 1.09, 1.09, 1.10, 1.10, 1.10, 1.08, 
        1.04, 1.03, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.05, 1.06, 1.04, 1.05, 1.05, 1.13, 1.03, 1.07, 1.08, 1.08, 1.08, 1.07, 1.07, 1.09, 1.08, 1.07, 
        1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.04, 1.04, 1.05, 1.05, 1.05, 1.05, 1.05, 1.12, 1.03, 1.06, 1.06, 1.08, 1.07, 1.07, 1.06, 1.08, 1.07, 1.06, 
        1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.04, 1.03, 1.10, 1.02, 1.05, 1.06, 1.06, 1.06, 1.06, 1.05, 1.06, 1.06, 1.06, 
        1.02, 1.02, 1.02, 1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.04, 1.03, 1.03, 1.02, 1.07, 1.02, 1.04, 1.04, 1.05, 1.06, 1.05, 1.05, 1.06, 1.06, 1.05, 
        1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.09, 1.02, 1.04, 1.05, 1.05, 1.05, 1.05, 1.04, 1.05, 1.06, 1.05, 
        1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.03, 1.08, 1.01, 1.04, 1.04, 1.05, 1.05, 1.04, 1.04, 1.05, 1.06, 1.05, 
        1.01, 1.01, 1.01, 1.01, 1.01, 1.01, 1.02, 1.01, 1.02, 1.02, 1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.03, 1.06, 1.01, 1.04, 1.04, 1.05, 1.04, 1.03, 1.03, 1.04, 1.05, 1.04, 
        1.01, 1.00, 1.01, 1.01, 1.01, 1.01, 1.01, 1.00, 1.01, 1.02, 1.01, 1.01, 1.02, 1.02, 1.02, 1.02, 1.03, 1.04, 1.01, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.03, 1.00, 1.01, 
        1.02, 1.00, 1.00, 1.02, 1.00, 1.01, 1.01, 1.00, 1.00, 1.02, 1.01, 1.01, 1.02, 1.02, 1.02, 1.02, 1.02, 1.04, 1.01, 1.03, 1.03, 1.03, 1.03, 1.02, 1.02, 1.02, 1.00, 1.01
    ]),

    layer1HCalScaleETBins = cms.vint32([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 256]),
    layer1HCalScaleFactors = cms.vdouble([
        2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,3.0000,3.0000,3.0000,3.0000,3.0000,3.0000,3.0000,3.0000,2.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.3334,1.3334,1.6667,1.6667,1.3334,1.3334,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.6667,1.0000,1.0000,1.0000,1.0000,1.0000,1.3334,1.0000,1.0000,1.0000,
        1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.4000,1.6000,1.6000,1.4000,1.4000,1.4000,1.6000,1.4000,1.2000,1.2000,1.2000,1.2000,1.0000,1.2000,1.2000,1.2000,1.2000,
        1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.4286,1.2858,1.2858,1.4286,1.4286,1.4286,1.4286,1.4286,1.4286,1.4286,1.4286,1.4286,1.4286,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,
        1.2223,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.4445,1.4445,1.3334,1.3334,1.3334,1.3334,1.3334,1.1112,1.2223,1.2223,1.2223,1.1112,1.2223,1.2223,1.1112,1.2223,
        1.2728,1.2728,1.2728,1.2728,1.2728,1.2728,1.2728,1.2728,1.2728,1.2728,1.3637,1.3637,1.3637,1.3637,1.3637,1.3637,1.3637,1.3637,1.2728,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,
        1.2308,1.3077,1.3077,1.3077,1.2308,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.3077,1.1539,1.1539,1.1539,1.1539,1.1539,1.2308,1.1539,1.1539,1.1539,
        1.2667,1.2667,1.2667,1.2667,1.2667,1.2667,1.2667,1.2667,1.2667,1.2667,1.3334,1.3334,1.3334,1.3334,1.3334,1.3334,1.2667,1.3334,1.2667,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,
        1.2353,1.2942,1.2942,1.2942,1.2353,1.2353,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.2942,1.1765,1.1765,1.1765,1.1765,1.1765,1.2353,1.1765,1.1765,1.1765,
        1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.2632,1.3158,1.3158,1.3158,1.2632,1.2632,1.2632,1.3158,1.2632,1.2106,1.2106,1.2106,1.2106,1.1579,1.2106,1.2106,1.2106,1.2106,
        1.2381,1.2381,1.2381,1.2858,1.2381,1.2381,1.2858,1.2381,1.2381,1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.2858,1.1905,1.1905,1.1905,1.1905,1.1905,1.2381,1.1905,1.1905,1.1905,
        1.2174,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.2609,1.3044,1.3044,1.2609,1.2609,1.2609,1.2609,1.2609,1.2174,1.2174,1.2174,1.2174,1.1740,1.2174,1.2174,1.2174,1.2174,
        1.2400,1.2400,1.2400,1.2400,1.2400,1.2400,1.2800,1.2400,1.2400,1.2800,1.2800,1.2800,1.2800,1.2800,1.2800,1.2800,1.2800,1.2800,1.2400,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,
        1.2223,1.2593,1.2593,1.2593,1.2223,1.2593,1.2593,1.2593,1.2593,1.2593,1.2593,1.2593,1.2963,1.2593,1.2593,1.2593,1.2593,1.2593,1.2593,1.1852,1.2223,1.1852,1.1852,1.1852,1.2223,1.2223,1.1852,1.2223,
        1.2414,1.2414,1.2414,1.2414,1.2414,1.2414,1.2414,1.2414,1.2414,1.2414,1.2759,1.2759,1.2759,1.2759,1.2759,1.2759,1.2759,1.2759,1.2414,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,
        1.2259,1.2581,1.2581,1.2581,1.2259,1.2259,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.2581,1.1936,1.1936,1.1936,1.1936,1.1936,1.2259,1.1936,1.1936,1.1936,
        1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2425,1.2728,1.2728,1.2728,1.2728,1.2425,1.2425,1.2728,1.2425,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,
        1.2286,1.2286,1.2286,1.2572,1.2286,1.2286,1.2572,1.2286,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2572,1.2000,1.2000,1.2000,1.2000,1.2000,1.2286,1.2000,1.2000,1.2000,
        1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2433,1.2703,1.2703,1.2433,1.2433,1.2433,1.2433,1.2433,1.2163,1.2163,1.2163,1.2163,1.1892,1.2163,1.2163,1.2163,1.2163,
        1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2565,1.2308,1.2308,1.2565,1.2565,1.2565,1.2565,1.2565,1.2565,1.2565,1.2565,1.2565,1.2308,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,
        1.2196,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2440,1.2683,1.2683,1.2440,1.2440,1.2440,1.2440,1.2440,1.1952,1.2196,1.2196,1.1952,1.1952,1.2196,1.2196,1.1952,1.2196,
        1.2326,1.2326,1.2326,1.2326,1.2326,1.2326,1.2326,1.2326,1.2326,1.2326,1.2559,1.2559,1.2559,1.2559,1.2559,1.2559,1.2559,1.2559,1.2326,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,
        1.2223,1.2445,1.2445,1.2445,1.2223,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2445,1.2000,1.2000,1.2000,1.2000,1.2000,1.2223,1.2000,1.2000,1.2000,
        1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2341,1.2554,1.2554,1.2554,1.2554,1.2554,1.2341,1.2554,1.2341,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,
        1.2245,1.2245,1.2449,1.2449,1.2245,1.2245,1.2449,1.2245,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2449,1.2041,1.2041,1.2041,1.2041,1.2041,1.2245,1.2041,1.2041,1.2041,
        1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2550,1.2550,1.2353,1.2353,1.2353,1.2550,1.2353,1.2157,1.2157,1.2157,1.2157,1.1961,1.2157,1.2157,1.2157,1.2157,
        1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2453,1.2265,1.2265,1.2453,1.2453,1.2453,1.2453,1.2453,1.2453,1.2453,1.2453,1.2453,1.2453,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,
        1.2182,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2364,1.2546,1.2546,1.2364,1.2364,1.2364,1.2364,1.2364,1.2182,1.2182,1.2182,1.2182,1.2000,1.2182,1.2182,1.2182,1.2182,
        1.2281,1.2281,1.2281,1.2281,1.2281,1.2281,1.2281,1.2281,1.2281,1.2281,1.2457,1.2457,1.2457,1.2457,1.2457,1.2457,1.2457,1.2457,1.2281,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,
        1.2204,1.2373,1.2373,1.2373,1.2204,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2373,1.2034,1.2204,1.2034,1.2034,1.2034,1.2204,1.2204,1.2034,1.2204,
        1.2296,1.2296,1.2296,1.2296,1.2296,1.2296,1.2296,1.2296,1.2296,1.2296,1.2460,1.2460,1.2460,1.2460,1.2460,1.2460,1.2296,1.2460,1.2296,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,
        1.2223,1.2381,1.2381,1.2381,1.2223,1.2223,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2381,1.2064,1.2064,1.2064,1.2064,1.2064,1.2223,1.2064,1.2064,1.2064,
        1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2462,1.2462,1.2462,1.2308,1.2308,1.2308,1.2462,1.2308,1.2154,1.2154,1.2154,1.2154,1.2000,1.2154,1.2154,1.2154,1.2154,
        1.2239,1.2239,1.2239,1.2389,1.2239,1.2239,1.2389,1.2239,1.2239,1.2389,1.2389,1.2389,1.2389,1.2389,1.2389,1.2389,1.2389,1.2389,1.2389,1.2090,1.2090,1.2090,1.2090,1.2090,1.2239,1.2090,1.2090,1.2090,
        1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2319,1.2464,1.2464,1.2319,1.2319,1.2319,1.2319,1.2319,1.2174,1.2174,1.2174,1.2174,1.2029,1.2174,1.2174,1.2174,1.2174,
        1.2254,1.2254,1.2254,1.2254,1.2254,1.2254,1.2395,1.2254,1.2254,1.2254,1.2395,1.2395,1.2395,1.2395,1.2395,1.2395,1.2395,1.2395,1.2254,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,
        1.2192,1.2329,1.2329,1.2329,1.2192,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2329,1.2055,1.2192,1.2055,1.2055,1.2055,1.2192,1.2192,1.2055,1.2192,
        1.2267,1.2267,1.2267,1.2267,1.2267,1.2267,1.2267,1.2267,1.2267,1.2267,1.2400,1.2400,1.2400,1.2400,1.2400,1.2400,1.2400,1.2400,1.2267,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,
        1.2208,1.2338,1.2338,1.2338,1.2208,1.2208,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2338,1.2078,1.2078,1.2078,1.2078,1.2078,1.2208,1.2078,1.2078,1.2078,
        1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2279,1.2406,1.2406,1.2406,1.2406,1.2406,1.2279,1.2406,1.2279,1.2152,1.2152,1.2152,1.2152,1.2152,1.2152,1.2152,1.2152,1.2152,
        1.2223,1.2223,1.2223,1.2346,1.2223,1.2223,1.2346,1.2223,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2346,1.2099,1.2099,1.2099,1.2099,1.2099,1.2223,1.2099,1.2099,1.2099,
        1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2290,1.2410,1.2410,1.2290,1.2290,1.2290,1.2290,1.2290,1.2169,1.2169,1.2169,1.2169,1.2049,1.2169,1.2169,1.2169,1.2169,
        1.2236,1.2236,1.2236,1.2236,1.2236,1.2236,1.2353,1.2236,1.2236,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2353,1.2236,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,
        1.2184,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2299,1.2414,1.2299,1.2299,1.2299,1.2299,1.2299,1.2069,1.2184,1.2184,1.2069,1.2069,1.2184,1.2184,1.2069,1.2184,
        1.2248,1.2248,1.2248,1.2248,1.2248,1.2248,1.2248,1.2248,1.2248,1.2248,1.2360,1.2360,1.2360,1.2360,1.2360,1.2360,1.2360,1.2360,1.2248,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,
        1.2198,1.2308,1.2308,1.2308,1.2198,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2088,1.2088,1.2088,1.2088,1.2088,1.2198,1.2088,1.2088,1.2088,
        1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2366,1.2366,1.2366,1.2366,1.2366,1.2259,1.2366,1.2259,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,
        1.2211,1.2211,1.2316,1.2316,1.2211,1.2211,1.2316,1.2211,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2316,1.2106,1.2106,1.2106,1.2106,1.2106,1.2211,1.2106,1.2106,1.2106,
        1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2372,1.2372,1.2269,1.2269,1.2269,1.2372,1.2269,1.2165,1.2165,1.2165,1.2165,1.2062,1.2165,1.2165,1.2165,1.2165,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2324,1.2223,1.2223,1.2324,1.2324,1.2324,1.2324,1.2324,1.2324,1.2324,1.2324,1.2324,1.2324,1.2122,1.2122,1.2122,1.2122,1.2122,1.2223,1.2122,1.2122,1.2122,
        1.2179,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2278,1.2377,1.2377,1.2278,1.2278,1.2278,1.2278,1.2278,1.2179,1.2179,1.2179,1.2179,1.2080,1.2179,1.2179,1.2179,1.2179,
        1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2331,1.2234,1.2234,1.2234,1.2331,1.2331,1.2331,1.2331,1.2331,1.2331,1.2331,1.2331,1.2234,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,
        1.2191,1.2286,1.2286,1.2286,1.2191,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2286,1.2096,1.2191,1.2096,1.2096,1.2096,1.2191,1.2191,1.2096,1.2191,
        1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2337,1.2337,1.2337,1.2337,1.2337,1.2337,1.2243,1.2337,1.2243,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,
        1.2202,1.2202,1.2294,1.2294,1.2202,1.2202,1.2294,1.2202,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2294,1.2111,1.2111,1.2111,1.2111,1.2111,1.2202,1.2111,1.2111,1.2111,
        1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2253,1.2343,1.2343,1.2343,1.2343,1.2253,1.2253,1.2343,1.2253,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,
        1.2213,1.2213,1.2213,1.2301,1.2213,1.2213,1.2301,1.2213,1.2213,1.2301,1.2301,1.2301,1.2301,1.2301,1.2301,1.2301,1.2301,1.2301,1.2301,1.2124,1.2124,1.2124,1.2124,1.2124,1.2213,1.2124,1.2124,1.2124,
        1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2261,1.2348,1.2348,1.2261,1.2261,1.2261,1.2261,1.2261,1.2174,1.2174,1.2174,1.2174,1.2087,1.2174,1.2174,1.2174,1.2174,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2308,1.2223,1.2223,1.2223,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2308,1.2223,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,
        1.2185,1.2269,1.2269,1.2269,1.2185,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2269,1.2101,1.2185,1.2185,1.2101,1.2101,1.2185,1.2185,1.2101,1.2185,
        1.2232,1.2232,1.2232,1.2232,1.2232,1.2232,1.2232,1.2232,1.2232,1.2232,1.2315,1.2315,1.2315,1.2315,1.2315,1.2315,1.2315,1.2315,1.2232,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,
        1.2196,1.2277,1.2277,1.2277,1.2196,1.2196,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2277,1.2114,1.2114,1.2114,1.2114,1.2114,1.2196,1.2114,1.2114,1.2114,
        1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2240,1.2320,1.2320,1.2320,1.2320,1.2320,1.2240,1.2320,1.2240,1.2160,1.2160,1.2160,1.2160,1.2160,1.2160,1.2160,1.2160,1.2160,
        1.2205,1.2205,1.2205,1.2284,1.2205,1.2205,1.2284,1.2205,1.2205,1.2284,1.2284,1.2284,1.2284,1.2284,1.2284,1.2284,1.2284,1.2284,1.2284,1.2126,1.2126,1.2126,1.2126,1.2126,1.2205,1.2126,1.2126,1.2126,
        1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2326,1.2326,1.2249,1.2249,1.2249,1.2249,1.2249,1.2171,1.2171,1.2171,1.2171,1.2094,1.2171,1.2171,1.2171,1.2171,
        1.2214,1.2214,1.2214,1.2214,1.2214,1.2214,1.2291,1.2214,1.2214,1.2291,1.2291,1.2291,1.2291,1.2291,1.2291,1.2291,1.2291,1.2291,1.2214,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,
        1.2181,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2256,1.2331,1.2256,1.2256,1.2256,1.2256,1.2256,1.2181,1.2181,1.2181,1.2106,1.2106,1.2181,1.2181,1.2181,1.2181,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2297,1.2297,1.2297,1.2297,1.2297,1.2297,1.2297,1.2297,1.2223,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,
        1.2190,1.2263,1.2263,1.2263,1.2190,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2263,1.2117,1.2190,1.2117,1.2117,1.2117,1.2190,1.2190,1.2117,1.2190,
        1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2231,1.2303,1.2303,1.2303,1.2303,1.2303,1.2231,1.2303,1.2231,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,
        1.2199,1.2199,1.2270,1.2270,1.2199,1.2199,1.2270,1.2199,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2128,1.2128,1.2128,1.2128,1.2128,1.2199,1.2128,1.2128,1.2128,
        1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2238,1.2308,1.2308,1.2238,1.2238,1.2238,1.2308,1.2238,1.2168,1.2168,1.2168,1.2168,1.2098,1.2168,1.2168,1.2168,1.2168,
        1.2207,1.2207,1.2207,1.2207,1.2207,1.2207,1.2276,1.2207,1.2207,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2138,1.2138,1.2138,1.2138,1.2138,1.2207,1.2138,1.2138,1.2138,
        1.2177,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2245,1.2313,1.2245,1.2245,1.2245,1.2245,1.2245,1.2177,1.2177,1.2177,1.2177,1.2109,1.2177,1.2177,1.2177,1.2177,
        1.2215,1.2215,1.2215,1.2215,1.2215,1.2215,1.2282,1.2215,1.2215,1.2215,1.2282,1.2282,1.2282,1.2282,1.2282,1.2282,1.2282,1.2282,1.2215,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,
        1.2186,1.2252,1.2252,1.2252,1.2186,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2120,1.2186,1.2186,1.2120,1.2120,1.2186,1.2186,1.2120,1.2186,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2288,1.2288,1.2288,1.2288,1.2288,1.2223,1.2288,1.2223,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,
        1.2194,1.2194,1.2259,1.2259,1.2194,1.2194,1.2259,1.2194,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2259,1.2130,1.2130,1.2130,1.2130,1.2130,1.2194,1.2130,1.2130,1.2130,
        1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2230,1.2293,1.2293,1.2293,1.2293,1.2230,1.2230,1.2293,1.2230,1.2166,1.2166,1.2166,1.2166,1.2166,1.2166,1.2166,1.2166,1.2166,
        1.2202,1.2202,1.2202,1.2265,1.2202,1.2202,1.2265,1.2202,1.2202,1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2265,1.2139,1.2139,1.2139,1.2139,1.2139,1.2202,1.2139,1.2139,1.2139,
        1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2237,1.2299,1.2237,1.2237,1.2237,1.2237,1.2237,1.2174,1.2174,1.2174,1.2174,1.2112,1.2174,1.2174,1.2174,1.2174,
        1.2209,1.2209,1.2209,1.2209,1.2209,1.2209,1.2270,1.2209,1.2209,1.2209,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2270,1.2209,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,
        1.2182,1.2243,1.2243,1.2243,1.2182,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2243,1.2304,1.2243,1.2243,1.2243,1.2243,1.2243,1.2182,1.2182,1.2182,1.2122,1.2122,1.2182,1.2182,1.2182,1.2182,
        1.2216,1.2216,1.2216,1.2216,1.2216,1.2216,1.2216,1.2216,1.2216,1.2216,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2276,1.2216,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,
        1.2190,1.2249,1.2249,1.2249,1.2190,1.2190,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2249,1.2131,1.2190,1.2131,1.2131,1.2131,1.2190,1.2190,1.2131,1.2131,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2281,1.2281,1.2281,1.2281,1.2281,1.2223,1.2281,1.2223,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,
        1.2197,1.2197,1.2255,1.2255,1.2197,1.2197,1.2255,1.2197,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2255,1.2139,1.2139,1.2139,1.2139,1.2139,1.2197,1.2139,1.2139,1.2139,
        1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2229,1.2286,1.2286,1.2229,1.2229,1.2229,1.2229,1.2229,1.2172,1.2172,1.2172,1.2172,1.2115,1.2172,1.2172,1.2172,1.2172,
        1.2204,1.2204,1.2204,1.2204,1.2204,1.2204,1.2260,1.2204,1.2204,1.2260,1.2260,1.2260,1.2260,1.2260,1.2260,1.2260,1.2260,1.2260,1.2204,1.2147,1.2147,1.2147,1.2147,1.2147,1.2204,1.2147,1.2147,1.2147,
        1.2179,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2235,1.2291,1.2235,1.2235,1.2235,1.2235,1.2235,1.2179,1.2179,1.2179,1.2179,1.2123,1.2179,1.2179,1.2179,1.2179,
        1.2210,1.2210,1.2210,1.2210,1.2210,1.2210,1.2266,1.2210,1.2210,1.2210,1.2266,1.2266,1.2266,1.2266,1.2266,1.2266,1.2266,1.2266,1.2210,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,
        1.2186,1.2241,1.2241,1.2241,1.2186,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2241,1.2132,1.2186,1.2132,1.2132,1.2132,1.2186,1.2186,1.2132,1.2186,
        1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2217,1.2271,1.2271,1.2271,1.2271,1.2271,1.2217,1.2271,1.2217,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,
        1.2193,1.2193,1.2246,1.2246,1.2193,1.2193,1.2246,1.2193,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2246,1.2140,1.2140,1.2140,1.2140,1.2140,1.2193,1.2140,1.2140,1.2140,
        1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2276,1.2276,1.2276,1.2223,1.2223,1.2276,1.2223,1.2170,1.2170,1.2170,1.2170,1.2170,1.2170,1.2170,1.2170,1.2170,
        1.2199,1.2199,1.2199,1.2199,1.2199,1.2199,1.2252,1.2199,1.2199,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2252,1.2147,1.2147,1.2147,1.2147,1.2147,1.2199,1.2147,1.2147,1.2147,
        1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2228,1.2280,1.2228,1.2228,1.2228,1.2228,1.2228,1.2177,1.2177,1.2177,1.2177,1.2125,1.2177,1.2177,1.2177,1.2177,
        1.2206,1.2206,1.2206,1.2206,1.2206,1.2206,1.2257,1.2206,1.2206,1.2206,1.2257,1.2257,1.2257,1.2257,1.2257,1.2257,1.2257,1.2257,1.2206,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,
        1.2183,1.2234,1.2234,1.2234,1.2183,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2234,1.2132,1.2183,1.2183,1.2132,1.2132,1.2183,1.2183,1.2132,1.2183,
        1.2212,1.2212,1.2212,1.2212,1.2212,1.2212,1.2212,1.2212,1.2212,1.2212,1.2262,1.2262,1.2262,1.2262,1.2262,1.2262,1.2212,1.2262,1.2212,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,
    ]),

    layer1HFScaleETBins = cms.vint32([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 256]),
    layer1HFScaleFactors = cms.vdouble([
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.2000,1.2000,1.2000,1.2000,1.2000,1.0000,1.2000,1.2000,1.0000,1.2000,1.2000,1.2000,
        1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,1.1429,
        1.2223,1.2223,1.1112,1.2223,1.2223,1.1112,1.1112,1.2223,1.1112,1.1112,1.2223,1.2223,
        1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,1.1819,
        1.1539,1.1539,1.1539,1.1539,1.1539,1.1539,1.1539,1.2308,1.1539,1.1539,1.2308,1.1539,
        1.2000,1.2000,1.2000,1.2000,1.2000,1.1334,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,
        1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,1.1765,
        1.2106,1.2106,1.2106,1.2106,1.2106,1.1579,1.2106,1.2106,1.1579,1.2106,1.2106,1.2106,
        1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,1.1905,
        1.2174,1.2174,1.2174,1.2174,1.2174,1.1740,1.2174,1.2174,1.1740,1.1740,1.2174,1.2174,
        1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,
        1.1852,1.2223,1.1852,1.1852,1.2223,1.1852,1.1852,1.2223,1.1852,1.1852,1.2223,1.1852,
        1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,1.2069,
        1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,1.1936,
        1.2122,1.2122,1.2122,1.2122,1.2122,1.1819,1.2122,1.2122,1.1819,1.2122,1.2122,1.2122,
        1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,
        1.2163,1.2163,1.2163,1.2163,1.2163,1.1892,1.2163,1.2163,1.1892,1.2163,1.2163,1.2163,
        1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,1.2052,
        1.2196,1.2196,1.1952,1.1952,1.2196,1.1952,1.1952,1.2196,1.1952,1.1952,1.2196,1.2196,
        1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,1.2094,
        1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2000,1.2223,1.2000,1.2000,1.2223,1.2000,
        1.2128,1.2128,1.2128,1.2128,1.2128,1.1915,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,
        1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,1.2041,
        1.2157,1.2157,1.2157,1.2157,1.2157,1.1961,1.2157,1.2157,1.1961,1.2157,1.2157,1.2157,
        1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,1.2076,
        1.2182,1.2182,1.2000,1.2182,1.2182,1.2000,1.2000,1.2182,1.2000,1.2000,1.2182,1.2182,
        1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,
        1.2034,1.2034,1.2034,1.2034,1.2034,1.2034,1.2034,1.2204,1.2034,1.2034,1.2204,1.2034,
        1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,1.2132,
        1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,1.2064,
        1.2154,1.2154,1.2154,1.2154,1.2154,1.2000,1.2154,1.2154,1.2000,1.2154,1.2154,1.2154,
        1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,1.2090,
        1.2174,1.2174,1.2174,1.2174,1.2174,1.2029,1.2174,1.2174,1.2029,1.2029,1.2174,1.2174,
        1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,1.2113,
        1.2192,1.2192,1.2055,1.2055,1.2192,1.2055,1.2055,1.2192,1.2055,1.2055,1.2192,1.2055,
        1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,1.2134,
        1.2078,1.2078,1.2078,1.2078,1.2078,1.2078,1.2078,1.2078,1.2078,1.2078,1.2208,1.2078,
        1.2152,1.2152,1.2152,1.2152,1.2152,1.2026,1.2152,1.2152,1.2026,1.2152,1.2152,1.2152,
        1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,1.2099,
        1.2169,1.2169,1.2169,1.2169,1.2169,1.2049,1.2169,1.2169,1.2049,1.2169,1.2169,1.2169,
        1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,1.2118,
        1.2184,1.2184,1.2069,1.2069,1.2184,1.2069,1.2069,1.2184,1.2069,1.2069,1.2184,1.2184,
        1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,1.2135,
        1.2088,1.2088,1.2088,1.2088,1.2088,1.2088,1.2088,1.2198,1.2088,1.2088,1.2198,1.2088,
        1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,1.2151,
        1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,1.2106,
        1.2165,1.2165,1.2165,1.2165,1.2165,1.2062,1.2165,1.2165,1.2062,1.2165,1.2165,1.2165,
        1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,1.2122,
        1.2179,1.2179,1.2080,1.2179,1.2179,1.2080,1.2080,1.2179,1.2080,1.2080,1.2179,1.2179,
        1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,1.2136,
        1.2096,1.2096,1.2096,1.2096,1.2096,1.2096,1.2096,1.2191,1.2096,1.2096,1.2191,1.2096,
        1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,1.2150,
        1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,1.2111,
        1.2163,1.2163,1.2163,1.2163,1.2163,1.2073,1.2163,1.2163,1.2073,1.2163,1.2163,1.2163,
        1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,1.2124,
        1.2174,1.2174,1.2174,1.2174,1.2174,1.2087,1.2174,1.2174,1.2087,1.2174,1.2174,1.2174,
        1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,1.2137,
        1.2185,1.2185,1.2101,1.2101,1.2185,1.2101,1.2101,1.2185,1.2101,1.2101,1.2185,1.2101,
        1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,
        1.2114,1.2114,1.2114,1.2114,1.2114,1.2114,1.2114,1.2114,1.2114,1.2114,1.2196,1.2114,
        1.2160,1.2160,1.2160,1.2160,1.2160,1.2080,1.2160,1.2160,1.2160,1.2160,1.2160,1.2160,
        1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,1.2126,
        1.2171,1.2171,1.2171,1.2171,1.2171,1.2094,1.2171,1.2171,1.2094,1.2171,1.2171,1.2171,
        1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,
        1.2181,1.2181,1.2106,1.2181,1.2181,1.2106,1.2106,1.2181,1.2106,1.2106,1.2181,1.2181,
        1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,1.2149,
        1.2117,1.2117,1.2117,1.2117,1.2117,1.2117,1.2117,1.2190,1.2117,1.2117,1.2190,1.2117,
        1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,1.2159,
        1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,1.2128,
        1.2168,1.2168,1.2168,1.2168,1.2168,1.2098,1.2168,1.2168,1.2098,1.2168,1.2168,1.2168,
        1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,1.2138,
        1.2177,1.2177,1.2109,1.2177,1.2177,1.2109,1.2177,1.2177,1.2109,1.2177,1.2177,1.2177,
        1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,
        1.2186,1.2186,1.2120,1.2120,1.2186,1.2120,1.2120,1.2186,1.2120,1.2120,1.2186,1.2120,
        1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,1.2157,
        1.2130,1.2130,1.2130,1.2130,1.2130,1.2130,1.2130,1.2130,1.2130,1.2130,1.2194,1.2130,
        1.2166,1.2166,1.2166,1.2166,1.2166,1.2102,1.2166,1.2166,1.2166,1.2166,1.2166,1.2166,
        1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,
        1.2174,1.2174,1.2174,1.2174,1.2174,1.2112,1.2174,1.2174,1.2112,1.2174,1.2174,1.2174,
        1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,1.2148,
        1.2182,1.2182,1.2122,1.2182,1.2182,1.2122,1.2122,1.2182,1.2122,1.2122,1.2182,1.2182,
        1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,1.2156,
        1.2131,1.2131,1.2131,1.2131,1.2131,1.2131,1.2131,1.2190,1.2131,1.2131,1.2190,1.2131,
        1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,1.2164,
        1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,1.2139,
        1.2172,1.2172,1.2172,1.2172,1.2172,1.2115,1.2172,1.2172,1.2115,1.2172,1.2172,1.2172,
        1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,
        1.2179,1.2179,1.2123,1.2179,1.2179,1.2123,1.2123,1.2179,1.2123,1.2123,1.2179,1.2179,
        1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,1.2155,
        1.2186,1.2132,1.2132,1.2132,1.2186,1.2132,1.2132,1.2186,1.2132,1.2132,1.2186,1.2132,
        1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,1.2163,
        1.2140,1.2140,1.2140,1.2140,1.2140,1.2140,1.2140,1.2140,1.2140,1.2140,1.2193,1.2140,
        1.2170,1.2170,1.2170,1.2170,1.2170,1.2117,1.2170,1.2170,1.2117,1.2170,1.2170,1.2170,
        1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,1.2147,
        1.2177,1.2177,1.2177,1.2177,1.2177,1.2125,1.2177,1.2177,1.2125,1.2177,1.2177,1.2177,
        1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,1.2154,
        1.2183,1.2183,1.2132,1.2132,1.2183,1.2132,1.2132,1.2183,1.2132,1.2132,1.2183,1.2132,
        1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,1.2161,
    ])
)