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
    jetPUSType                 = "PhiRing1",
    jetPUSUsePhiRing           = 1,

    # Calibration options
    jetCalibrationType         = "LUT",
    jetCompressPtLUTFile       = "L1Trigger/L1TCalorimeter/data/lut_pt_compress_2017v1.txt",
    jetCompressEtaLUTFile      = "L1Trigger/L1TCalorimeter/data/lut_eta_compress_2017v1.txt",
    jetCalibrationLUTFile      = "L1Trigger/L1TCalorimeter/data/lut_calib_2023v0_ECALZS_PhiRing.txt",


    # sums: 0=ET, 1=HT, 2=MET, 3=MHT
    etSumEtaMin             = [1, 1, 1, 1, 1],
    etSumEtaMax             = [28,  26, 28,  26, 28],
    etSumEtThreshold        = [0.,  30.,  0.,  30., 0.], # only 2nd (HT) and 4th (MHT) values applied
    etSumMetPUSType         = "LUT", # et threshold from this LUT supercedes et threshold in line above
    etSumBypassEttPUS       = 1,
    etSumBypassEcalSumPUS   = 1,

    etSumMetPUSLUTFile      = "L1Trigger/L1TCalorimeter/data/metPumLUT_2023v0_puppiMet_fit.txt",


    # Layer 1 SF
    layer1ECalScaleETBins = cms.vint32([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 256]),
    layer1ECalScaleFactors = cms.vdouble([
        0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,
        0.3334,0.3334,0.3334,0.3334,0.3334,0.3334,0.3334,0.3334,0.3334,0.6667,0.6667,0.6667,0.6667,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,0.6667,0.6667,0.6667,0.0000,0.0000,0.0000,
        0.6000,0.6000,0.6000,0.6000,0.6000,0.6000,0.8000,0.8000,0.8000,0.8000,0.8000,0.8000,1.0000,1.0000,1.0000,1.0000,1.0000,1.2000,1.0000,1.2000,1.2000,1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,0.0000,
        0.7143,0.7143,0.7143,0.8572,0.8572,0.7143,0.8572,0.8572,0.8572,0.8572,0.8572,1.0000,1.0000,1.1429,1.1429,1.1429,1.1429,1.2858,1.1429,1.2858,1.1429,1.1429,1.1429,1.0000,1.0000,0.7143,0.0000,0.0000,
        0.8889,0.8889,0.8889,0.8889,0.8889,0.8889,0.8889,0.8889,1.0000,1.0000,1.0000,1.0000,1.1112,1.1112,1.1112,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.2223,1.1112,1.1112,1.0000,0.8889,0.0000,0.0000,
        0.9091,0.9091,0.9091,0.9091,0.9091,0.9091,0.9091,1.0000,1.0000,1.0000,1.0000,1.0910,1.0910,1.1819,1.1819,1.1819,1.1819,1.2728,1.1819,1.2728,1.2728,1.1819,1.1819,1.0910,1.0910,1.0000,0.0000,0.0000,
        1.0000,0.9231,0.9231,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0770,1.0000,1.0770,1.1539,1.1539,1.1539,1.1539,1.2308,1.3077,1.2308,1.3077,1.3077,1.2308,1.2308,1.1539,1.1539,1.0000,1.0770,0.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0667,1.0000,1.0000,1.0000,1.0667,1.0667,1.0667,1.1334,1.2000,1.2000,1.2000,1.2000,1.2667,1.2000,1.2667,1.2667,1.2667,1.2000,1.2000,1.1334,1.0667,1.1334,0.0000,
        1.0000,1.0000,1.0000,1.0000,1.0589,1.0589,1.0589,1.0000,1.0589,1.0589,1.0589,1.0589,1.1177,1.1765,1.1765,1.1765,1.1765,1.2942,1.1765,1.2942,1.2942,1.2353,1.2353,1.1765,1.1765,1.1177,1.1177,0.0000,
        1.0527,1.0000,1.0000,1.0000,1.0527,1.0527,1.0527,1.0527,1.0527,1.1053,1.0527,1.1053,1.1579,1.2106,1.1579,1.2106,1.2106,1.2632,1.2106,1.2632,1.2632,1.2632,1.2106,1.2106,1.1579,1.1579,1.1579,1.0000,
        1.0477,1.0477,1.0477,1.0477,1.0477,1.0477,1.0477,1.0477,1.0477,1.0953,1.0477,1.0953,1.1429,1.1905,1.1905,1.1905,1.1905,1.2858,1.1905,1.2858,1.2381,1.2381,1.2381,1.1905,1.1905,1.1429,1.1429,1.0000,
        1.0435,1.0435,1.0435,1.0435,1.0435,1.0435,1.0435,1.0435,1.0435,1.0870,1.0870,1.0870,1.1305,1.1740,1.1740,1.1740,1.1740,1.2609,1.1740,1.2609,1.2609,1.2609,1.2174,1.2174,1.1740,1.1740,1.1740,1.0000,
        1.0400,1.0400,1.0400,1.0400,1.0400,1.0400,1.0400,1.0400,1.0800,1.0800,1.0800,1.0800,1.1601,1.2000,1.1601,1.1601,1.2000,1.2800,1.1601,1.2400,1.2400,1.2800,1.2000,1.2000,1.2000,1.1601,1.1601,1.0000,
        1.0371,1.0371,1.0371,1.0371,1.0371,1.0741,1.0741,1.0371,1.0741,1.0741,1.0741,1.1112,1.1482,1.1852,1.1852,1.1852,1.1852,1.2593,1.1852,1.2593,1.2593,1.2593,1.2223,1.2223,1.1852,1.1852,1.1482,1.0000,
        1.0345,1.0345,1.0345,1.0345,1.0345,1.0690,1.0690,1.0690,1.0690,1.0690,1.0690,1.1035,1.1380,1.1725,1.1725,1.1725,1.1725,1.2414,1.1725,1.2414,1.2414,1.2414,1.2069,1.2069,1.2069,1.1725,1.1725,1.0000,
        1.0323,1.0323,1.0323,1.0323,1.0323,1.0646,1.0646,1.0646,1.0646,1.0646,1.0968,1.0968,1.1291,1.1613,1.1613,1.1613,1.1936,1.2581,1.1613,1.2259,1.2259,1.2259,1.2259,1.2259,1.1936,1.1936,1.1613,1.0000,
        1.0304,1.0304,1.0304,1.0304,1.0304,1.0607,1.0607,1.0607,1.0607,1.0910,1.0910,1.0910,1.1213,1.1516,1.1516,1.1516,1.1819,1.2425,1.1516,1.2425,1.2425,1.2425,1.2122,1.2122,1.1819,1.1819,1.1516,1.0000,
        1.0286,1.0286,1.0286,1.0286,1.0286,1.0572,1.0572,1.0572,1.0572,1.0858,1.0858,1.0858,1.1143,1.1429,1.1429,1.1715,1.1715,1.2572,1.1715,1.2286,1.2286,1.2286,1.2000,1.2000,1.2000,1.1715,1.1429,1.0000,
        1.0271,1.0271,1.0271,1.0271,1.0271,1.0541,1.0541,1.0541,1.0541,1.0811,1.0811,1.0811,1.1082,1.1622,1.1352,1.1622,1.1622,1.2433,1.1622,1.2163,1.2163,1.2163,1.1892,1.1892,1.1892,1.1892,1.1352,1.0000,
        1.0257,1.0257,1.0257,1.0257,1.0257,1.0513,1.0513,1.0513,1.0513,1.0770,1.0770,1.0770,1.1026,1.1539,1.1539,1.1539,1.1539,1.2308,1.1539,1.2308,1.2308,1.2052,1.2052,1.2052,1.1795,1.1795,1.1283,1.0000,
        1.0244,1.0244,1.0244,1.0244,1.0244,1.0488,1.0488,1.0488,1.0488,1.0732,1.0732,1.0732,1.0976,1.1464,1.1464,1.1464,1.1464,1.2196,1.1464,1.2196,1.2196,1.2196,1.1952,1.1952,1.1708,1.1708,1.1220,1.0000,
        1.0233,1.0233,1.0233,1.0233,1.0233,1.0466,1.0466,1.0466,1.0466,1.0698,1.0698,1.0698,1.0931,1.1396,1.1396,1.1396,1.1396,1.2326,1.1396,1.2094,1.2094,1.2094,1.1861,1.1861,1.1628,1.1861,1.1163,1.0000,
        1.0223,1.0223,1.0223,1.0223,1.0223,1.0445,1.0445,1.0445,1.0667,1.0667,1.0667,1.0667,1.1112,1.1334,1.1334,1.1334,1.1334,1.2223,1.1556,1.2000,1.2000,1.2000,1.1778,1.1778,1.1778,1.1778,1.1112,1.0000,
        1.0213,1.0213,1.0213,1.0213,1.0426,1.0426,1.0426,1.0426,1.0639,1.0639,1.0639,1.0639,1.1064,1.1277,1.1277,1.1277,1.1277,1.2128,1.1490,1.2128,1.1915,1.1915,1.1915,1.1915,1.1703,1.1703,1.1064,1.0000,
        1.0205,1.0205,1.0205,1.0205,1.0409,1.0409,1.0409,1.0409,1.0613,1.0613,1.0613,1.0817,1.1021,1.1225,1.1225,1.1225,1.1429,1.2041,1.1429,1.2041,1.2041,1.1837,1.1837,1.1837,1.1633,1.1633,1.1021,1.0000,
        1.0197,1.0197,1.0197,1.0197,1.0393,1.0393,1.0393,1.0393,1.0589,1.0589,1.0589,1.0785,1.0981,1.1177,1.1177,1.1177,1.1373,1.1961,1.1373,1.1961,1.1961,1.1961,1.1765,1.1765,1.1569,1.1765,1.0981,1.0000,
        1.0189,1.0189,1.0189,1.0189,1.0378,1.0378,1.0378,1.0378,1.0567,1.0567,1.0567,1.0755,1.0944,1.1133,1.1133,1.1133,1.1321,1.1887,1.1321,1.1887,1.1887,1.1887,1.1699,1.1699,1.1510,1.1699,1.0944,1.0000,
        1.0182,1.0182,1.0182,1.0182,1.0364,1.0364,1.0364,1.0364,1.0546,1.0546,1.0546,1.0728,1.0910,1.1091,1.1091,1.1091,1.1273,1.1819,1.1273,1.1819,1.1819,1.1819,1.1637,1.1637,1.1455,1.1637,1.0910,1.0000,
        1.0176,1.0176,1.0176,1.0176,1.0351,1.0351,1.0351,1.0351,1.0527,1.0527,1.0527,1.0702,1.0878,1.1053,1.1053,1.1053,1.1229,1.1755,1.1229,1.1930,1.1755,1.1755,1.1579,1.1579,1.1404,1.1579,1.0878,1.0000,
        1.0170,1.0170,1.0170,1.0170,1.0339,1.0339,1.0339,1.0339,1.0509,1.0509,1.0509,1.0678,1.0848,1.1017,1.1017,1.1187,1.1187,1.1695,1.1187,1.1865,1.1695,1.1695,1.1526,1.1526,1.1356,1.1526,1.0848,1.0000,
        1.0164,1.0164,1.0164,1.0164,1.0328,1.0328,1.0328,1.0328,1.0492,1.0492,1.0492,1.0656,1.0820,1.0984,1.0984,1.1148,1.1148,1.1640,1.1148,1.1804,1.1640,1.1640,1.1476,1.1476,1.1312,1.1476,1.0820,1.0000,
        1.0159,1.0159,1.0159,1.0159,1.0318,1.0318,1.0318,1.0318,1.0477,1.0477,1.0477,1.0635,1.0794,1.0953,1.0953,1.1112,1.1112,1.1588,1.1112,1.1747,1.1588,1.1588,1.1588,1.1429,1.1429,1.1429,1.0794,1.0000,
        1.0154,1.0154,1.0154,1.0308,1.0308,1.0308,1.0308,1.0308,1.0462,1.0462,1.0462,1.0616,1.0770,1.0924,1.0924,1.1077,1.1077,1.1539,1.1077,1.1693,1.1539,1.1539,1.1539,1.1385,1.1385,1.1385,1.0770,1.0000,
        1.0150,1.0150,1.0150,1.0299,1.0299,1.0299,1.0299,1.0299,1.0448,1.0448,1.0448,1.0598,1.0747,1.0896,1.0896,1.1045,1.1045,1.1493,1.1045,1.1642,1.1493,1.1493,1.1493,1.1493,1.1344,1.1344,1.0747,1.0000,
        1.0145,1.0145,1.0145,1.0290,1.0290,1.0290,1.0290,1.0290,1.0435,1.0435,1.0435,1.0580,1.0725,1.0870,1.0870,1.1015,1.1015,1.1450,1.1015,1.1595,1.1450,1.1450,1.1450,1.1450,1.1305,1.1305,1.0870,1.0000,
        1.0141,1.0141,1.0141,1.0282,1.0282,1.0282,1.0282,1.0282,1.0423,1.0423,1.0423,1.0564,1.0705,1.0846,1.0846,1.0986,1.0986,1.1409,1.0986,1.1550,1.1409,1.1409,1.1409,1.1409,1.1268,1.1268,1.0846,1.0000,
        1.0137,1.0137,1.0137,1.0274,1.0274,1.0274,1.0274,1.0274,1.0411,1.0411,1.0411,1.0548,1.0685,1.0822,1.0822,1.0959,1.0959,1.1370,1.0959,1.1507,1.1370,1.1370,1.1370,1.1370,1.1233,1.1370,1.0822,1.0000,
        1.0134,1.0134,1.0134,1.0267,1.0267,1.0267,1.0267,1.0267,1.0400,1.0400,1.0400,1.0534,1.0667,1.0800,1.0800,1.0934,1.0934,1.1334,1.0934,1.1467,1.1334,1.1334,1.1334,1.1334,1.1200,1.1334,1.0800,1.0000,
        1.0130,1.0130,1.0130,1.0260,1.0260,1.0260,1.0260,1.0260,1.0390,1.0390,1.0390,1.0520,1.0650,1.0780,1.0780,1.0910,1.0910,1.1299,1.0910,1.1429,1.1299,1.1299,1.1299,1.1299,1.1169,1.1299,1.0780,1.0000,
        1.0127,1.0127,1.0127,1.0254,1.0254,1.0254,1.0254,1.0254,1.0380,1.0380,1.0380,1.0507,1.0633,1.0887,1.0887,1.0887,1.0887,1.1393,1.0887,1.1393,1.1266,1.1266,1.1266,1.1266,1.1140,1.1266,1.0760,1.0000,
        1.0124,1.0124,1.0124,1.0247,1.0247,1.0247,1.0247,1.0247,1.0371,1.0371,1.0371,1.0494,1.0618,1.0865,1.0865,1.0865,1.0865,1.1359,1.0865,1.1359,1.1235,1.1235,1.1235,1.1235,1.1112,1.1235,1.0741,1.0000,
        1.0121,1.0121,1.0121,1.0241,1.0241,1.0241,1.0241,1.0241,1.0362,1.0362,1.0362,1.0482,1.0603,1.0844,1.0844,1.0844,1.0844,1.1326,1.0844,1.1326,1.1326,1.1205,1.1205,1.1205,1.1085,1.1205,1.0723,1.0000,
        1.0118,1.0118,1.0118,1.0236,1.0236,1.0236,1.0236,1.0236,1.0353,1.0353,1.0353,1.0471,1.0589,1.0824,1.0824,1.0824,1.0824,1.1295,1.0824,1.1295,1.1295,1.1177,1.1177,1.1177,1.1059,1.1177,1.0706,1.0000,
        1.0115,1.0115,1.0115,1.0230,1.0230,1.0230,1.0230,1.0230,1.0345,1.0345,1.0345,1.0460,1.0575,1.0805,1.0805,1.0805,1.0805,1.1265,1.0805,1.1265,1.1265,1.1150,1.1150,1.1150,1.1035,1.1150,1.0690,1.0000,
        1.0113,1.0113,1.0113,1.0225,1.0225,1.0225,1.0225,1.0225,1.0338,1.0338,1.0338,1.0450,1.0562,1.0787,1.0787,1.0787,1.0787,1.1236,1.0899,1.1236,1.1236,1.1236,1.1124,1.1124,1.1012,1.1124,1.0675,1.0000,
        1.0110,1.0110,1.0110,1.0220,1.0220,1.0220,1.0220,1.0220,1.0330,1.0330,1.0330,1.0440,1.0550,1.0770,1.0770,1.0770,1.0770,1.1209,1.0880,1.1209,1.1209,1.1209,1.1099,1.1099,1.0990,1.1099,1.0660,1.0000,
        1.0108,1.0108,1.0108,1.0216,1.0216,1.0216,1.0216,1.0216,1.0323,1.0323,1.0323,1.0431,1.0646,1.0753,1.0753,1.0753,1.0753,1.1183,1.0861,1.1183,1.1183,1.1183,1.1076,1.1076,1.0968,1.1076,1.0646,1.0000,
        1.0106,1.0211,1.0106,1.0211,1.0211,1.0211,1.0211,1.0211,1.0316,1.0316,1.0316,1.0422,1.0632,1.0737,1.0737,1.0737,1.0843,1.1158,1.0843,1.1158,1.1158,1.1158,1.1053,1.1053,1.0948,1.1053,1.0632,1.0000,
        1.0207,1.0207,1.0104,1.0207,1.0207,1.0207,1.0207,1.0207,1.0310,1.0310,1.0310,1.0516,1.0619,1.0722,1.0722,1.0722,1.0825,1.1135,1.0825,1.1135,1.1135,1.1135,1.1031,1.1031,1.0928,1.1031,1.0619,1.0000,
        1.0203,1.0203,1.0102,1.0203,1.0203,1.0203,1.0203,1.0203,1.0304,1.0304,1.0304,1.0506,1.0607,1.0708,1.0708,1.0708,1.0809,1.1112,1.0809,1.1112,1.1112,1.1112,1.1011,1.1011,1.0910,1.1011,1.0607,1.0000,
        1.0199,1.0199,1.0100,1.0199,1.0199,1.0199,1.0199,1.0199,1.0298,1.0298,1.0298,1.0496,1.0595,1.0694,1.0694,1.0694,1.0793,1.1090,1.0793,1.1090,1.1090,1.1090,1.0991,1.0991,1.0892,1.0991,1.0595,1.0000,
        1.0195,1.0195,1.0098,1.0195,1.0195,1.0195,1.0195,1.0195,1.0292,1.0292,1.0292,1.0486,1.0583,1.0680,1.0680,1.0680,1.0777,1.1068,1.0777,1.1166,1.1068,1.1068,1.0971,1.0971,1.0874,1.0971,1.0583,1.0000,
        1.0191,1.0191,1.0096,1.0191,1.0191,1.0191,1.0191,1.0191,1.0286,1.0286,1.0286,1.0477,1.0572,1.0667,1.0667,1.0667,1.0762,1.1048,1.0762,1.1143,1.1048,1.1048,1.0953,1.0953,1.0858,1.0953,1.0572,1.0000,
        1.0187,1.0187,1.0094,1.0187,1.0187,1.0187,1.0187,1.0187,1.0281,1.0281,1.0281,1.0468,1.0561,1.0655,1.0655,1.0748,1.0748,1.1029,1.0748,1.1122,1.1029,1.1029,1.1029,1.0935,1.0935,1.0935,1.0561,1.0000,
        1.0184,1.0184,1.0092,1.0184,1.0184,1.0184,1.0184,1.0184,1.0276,1.0276,1.0276,1.0459,1.0551,1.0643,1.0643,1.0734,1.0734,1.1010,1.0734,1.1101,1.1010,1.1010,1.1010,1.0918,1.0918,1.0918,1.0551,1.0000,
        1.0181,1.0181,1.0091,1.0181,1.0181,1.0181,1.0181,1.0181,1.0271,1.0271,1.0271,1.0451,1.0541,1.0631,1.0631,1.0721,1.0721,1.0991,1.0721,1.1082,1.0991,1.0991,1.0991,1.0901,1.0901,1.0901,1.0541,1.0000,
        1.0177,1.0177,1.0089,1.0177,1.0177,1.0177,1.0177,1.0177,1.0266,1.0266,1.0266,1.0443,1.0531,1.0620,1.0620,1.0708,1.0708,1.0974,1.0708,1.1062,1.0974,1.0974,1.0974,1.0974,1.0885,1.0885,1.0531,1.0000,
        1.0174,1.0174,1.0087,1.0174,1.0174,1.0174,1.0174,1.0174,1.0261,1.0261,1.0261,1.0435,1.0522,1.0609,1.0609,1.0696,1.0696,1.0957,1.0696,1.1044,1.0957,1.0957,1.0957,1.0957,1.0870,1.0870,1.0609,1.0000,
        1.0171,1.0171,1.0086,1.0171,1.0171,1.0171,1.0171,1.0171,1.0257,1.0257,1.0257,1.0428,1.0513,1.0599,1.0599,1.0684,1.0684,1.0941,1.0684,1.1026,1.0941,1.0941,1.0941,1.0941,1.0855,1.0855,1.0599,1.0000,
        1.0169,1.0169,1.0085,1.0169,1.0169,1.0169,1.0169,1.0169,1.0253,1.0253,1.0253,1.0421,1.0505,1.0589,1.0589,1.0673,1.0673,1.0925,1.0673,1.1009,1.0925,1.0925,1.0925,1.0925,1.0841,1.0841,1.0589,1.0000,
        1.0166,1.0166,1.0083,1.0166,1.0166,1.0166,1.0166,1.0166,1.0248,1.0248,1.0248,1.0414,1.0496,1.0579,1.0579,1.0662,1.0662,1.0910,1.0662,1.0992,1.0910,1.0910,1.0910,1.0910,1.0827,1.0910,1.0579,1.0000,
        1.0163,1.0163,1.0082,1.0163,1.0163,1.0163,1.0163,1.0163,1.0244,1.0244,1.0244,1.0407,1.0488,1.0570,1.0570,1.0651,1.0651,1.0895,1.0651,1.0976,1.0895,1.0895,1.0895,1.0895,1.0814,1.0895,1.0570,1.0000,
        1.0160,1.0160,1.0080,1.0160,1.0160,1.0160,1.0160,1.0160,1.0240,1.0240,1.0240,1.0400,1.0480,1.0560,1.0560,1.0640,1.0640,1.0880,1.0640,1.0960,1.0880,1.0880,1.0880,1.0880,1.0800,1.0880,1.0560,1.0000,
        1.0158,1.0158,1.0079,1.0158,1.0158,1.0158,1.0158,1.0158,1.0237,1.0237,1.0237,1.0394,1.0473,1.0630,1.0630,1.0630,1.0630,1.0945,1.0630,1.0945,1.0867,1.0867,1.0867,1.0867,1.0788,1.0867,1.0552,1.0000,
        1.0156,1.0156,1.0078,1.0156,1.0156,1.0156,1.0156,1.0156,1.0233,1.0233,1.0233,1.0388,1.0466,1.0621,1.0621,1.0621,1.0621,1.0931,1.0621,1.0931,1.0853,1.0853,1.0853,1.0853,1.0776,1.0853,1.0543,1.0000,
        1.0153,1.0153,1.0077,1.0153,1.0153,1.0153,1.0153,1.0153,1.0230,1.0230,1.0230,1.0382,1.0459,1.0611,1.0611,1.0611,1.0611,1.0917,1.0611,1.0917,1.0917,1.0840,1.0840,1.0840,1.0764,1.0840,1.0535,1.0000,
        1.0151,1.0151,1.0151,1.0151,1.0151,1.0151,1.0151,1.0151,1.0226,1.0226,1.0226,1.0376,1.0452,1.0602,1.0602,1.0602,1.0602,1.0903,1.0602,1.0903,1.0903,1.0828,1.0828,1.0828,1.0752,1.0828,1.0527,1.0000,
        1.0149,1.0149,1.0149,1.0149,1.0149,1.0149,1.0149,1.0149,1.0223,1.0223,1.0223,1.0371,1.0445,1.0593,1.0593,1.0593,1.0593,1.0889,1.0667,1.0889,1.0889,1.0815,1.0815,1.0815,1.0741,1.0815,1.0519,1.0000,
        1.0146,1.0146,1.0146,1.0146,1.0146,1.0146,1.0146,1.0146,1.0219,1.0219,1.0219,1.0365,1.0438,1.0584,1.0584,1.0584,1.0584,1.0876,1.0657,1.0876,1.0876,1.0876,1.0803,1.0803,1.0730,1.0803,1.0511,1.0000,
        1.0144,1.0144,1.0144,1.0144,1.0144,1.0144,1.0144,1.0144,1.0216,1.0216,1.0216,1.0360,1.0432,1.0576,1.0576,1.0576,1.0576,1.0864,1.0648,1.0864,1.0864,1.0864,1.0792,1.0792,1.0720,1.0792,1.0504,1.0000,
        1.0142,1.0142,1.0142,1.0142,1.0142,1.0142,1.0142,1.0142,1.0213,1.0213,1.0213,1.0355,1.0497,1.0568,1.0568,1.0568,1.0568,1.0852,1.0639,1.0852,1.0852,1.0852,1.0781,1.0781,1.0710,1.0781,1.0497,1.0000,
        1.0140,1.0140,1.0140,1.0140,1.0140,1.0140,1.0140,1.0140,1.0210,1.0210,1.0210,1.0420,1.0490,1.0560,1.0560,1.0560,1.0630,1.0840,1.0630,1.0840,1.0840,1.0840,1.0770,1.0770,1.0700,1.0770,1.0490,1.0000,
        1.0138,1.0138,1.0138,1.0138,1.0138,1.0138,1.0138,1.0138,1.0207,1.0207,1.0207,1.0414,1.0483,1.0552,1.0552,1.0552,1.0621,1.0828,1.0621,1.0828,1.0828,1.0828,1.0759,1.0759,1.0690,1.0759,1.0483,1.0000,
        1.0137,1.0137,1.0137,1.0137,1.0137,1.0137,1.0137,1.0137,1.0205,1.0205,1.0205,1.0409,1.0477,1.0545,1.0545,1.0545,1.0613,1.0817,1.0613,1.0817,1.0817,1.0817,1.0749,1.0749,1.0681,1.0749,1.0477,1.0000,
        1.0135,1.0135,1.0135,1.0135,1.0135,1.0135,1.0135,1.0135,1.0202,1.0202,1.0202,1.0403,1.0470,1.0537,1.0537,1.0537,1.0605,1.0806,1.0605,1.0806,1.0806,1.0806,1.0739,1.0739,1.0672,1.0739,1.0470,1.0000,
        1.0133,1.0133,1.0133,1.0133,1.0133,1.0133,1.0133,1.0133,1.0199,1.0199,1.0199,1.0398,1.0464,1.0530,1.0530,1.0530,1.0597,1.0795,1.0597,1.0861,1.0795,1.0795,1.0729,1.0729,1.0663,1.0729,1.0464,1.0000,
        1.0131,1.0131,1.0131,1.0131,1.0131,1.0131,1.0131,1.0131,1.0197,1.0197,1.0197,1.0393,1.0458,1.0523,1.0523,1.0589,1.0589,1.0785,1.0589,1.0850,1.0785,1.0785,1.0785,1.0719,1.0654,1.0719,1.0458,1.0000,
        1.0130,1.0130,1.0130,1.0130,1.0130,1.0130,1.0194,1.0130,1.0194,1.0194,1.0194,1.0388,1.0452,1.0517,1.0517,1.0581,1.0581,1.0775,1.0581,1.0839,1.0775,1.0775,1.0775,1.0710,1.0710,1.0710,1.0452,1.0000,
        1.0128,1.0128,1.0128,1.0128,1.0128,1.0128,1.0192,1.0128,1.0192,1.0192,1.0255,1.0383,1.0446,1.0510,1.0510,1.0574,1.0574,1.0765,1.0574,1.0829,1.0765,1.0765,1.0765,1.0701,1.0701,1.0701,1.0446,1.0000,
        1.0126,1.0126,1.0126,1.0126,1.0126,1.0126,1.0189,1.0126,1.0189,1.0189,1.0252,1.0378,1.0441,1.0504,1.0504,1.0567,1.0567,1.0755,1.0567,1.0818,1.0755,1.0755,1.0755,1.0692,1.0692,1.0692,1.0441,1.0000,
        1.0125,1.0125,1.0125,1.0125,1.0125,1.0125,1.0187,1.0125,1.0187,1.0187,1.0249,1.0373,1.0435,1.0497,1.0497,1.0560,1.0560,1.0746,1.0560,1.0808,1.0746,1.0746,1.0746,1.0746,1.0684,1.0684,1.0435,1.0000,
        1.0123,1.0123,1.0123,1.0123,1.0123,1.0123,1.0185,1.0123,1.0185,1.0185,1.0246,1.0369,1.0430,1.0491,1.0491,1.0553,1.0553,1.0737,1.0553,1.0798,1.0737,1.0737,1.0737,1.0737,1.0675,1.0675,1.0491,1.0000,
        1.0122,1.0122,1.0122,1.0122,1.0122,1.0122,1.0182,1.0122,1.0182,1.0182,1.0243,1.0364,1.0425,1.0485,1.0485,1.0546,1.0546,1.0728,1.0546,1.0788,1.0728,1.0728,1.0728,1.0728,1.0667,1.0667,1.0485,1.0000,
        1.0120,1.0120,1.0120,1.0120,1.0120,1.0120,1.0180,1.0180,1.0180,1.0180,1.0240,1.0360,1.0420,1.0480,1.0480,1.0539,1.0539,1.0719,1.0539,1.0779,1.0719,1.0719,1.0719,1.0719,1.0659,1.0659,1.0480,1.0000,
        1.0119,1.0119,1.0119,1.0119,1.0119,1.0119,1.0178,1.0178,1.0178,1.0178,1.0237,1.0356,1.0415,1.0474,1.0474,1.0533,1.0533,1.0711,1.0533,1.0770,1.0711,1.0711,1.0711,1.0711,1.0651,1.0711,1.0474,1.0000,
        1.0117,1.0117,1.0117,1.0117,1.0117,1.0117,1.0176,1.0176,1.0176,1.0176,1.0234,1.0351,1.0410,1.0468,1.0468,1.0527,1.0527,1.0702,1.0527,1.0761,1.0702,1.0702,1.0702,1.0702,1.0644,1.0702,1.0468,1.0000,
        1.0116,1.0116,1.0116,1.0116,1.0116,1.0116,1.0174,1.0174,1.0174,1.0174,1.0232,1.0347,1.0405,1.0521,1.0463,1.0521,1.0521,1.0694,1.0521,1.0752,1.0694,1.0694,1.0694,1.0694,1.0636,1.0694,1.0463,1.0000,
        1.0115,1.0115,1.0115,1.0115,1.0115,1.0115,1.0172,1.0172,1.0172,1.0172,1.0229,1.0343,1.0400,1.0515,1.0515,1.0515,1.0515,1.0743,1.0515,1.0743,1.0686,1.0686,1.0686,1.0686,1.0629,1.0686,1.0458,1.0000,
        1.0113,1.0113,1.0113,1.0113,1.0113,1.0113,1.0170,1.0170,1.0170,1.0170,1.0226,1.0339,1.0396,1.0509,1.0509,1.0509,1.0509,1.0735,1.0509,1.0735,1.0678,1.0678,1.0678,1.0678,1.0622,1.0678,1.0452,1.0000,
        1.0112,1.0112,1.0112,1.0112,1.0112,1.0112,1.0168,1.0168,1.0168,1.0168,1.0224,1.0336,1.0392,1.0503,1.0503,1.0503,1.0503,1.0727,1.0503,1.0727,1.0727,1.0671,1.0671,1.0671,1.0615,1.0671,1.0447,1.0000,
        1.0111,1.0111,1.0111,1.0111,1.0111,1.0111,1.0166,1.0166,1.0166,1.0166,1.0221,1.0332,1.0387,1.0498,1.0498,1.0498,1.0498,1.0719,1.0553,1.0719,1.0719,1.0663,1.0663,1.0663,1.0608,1.0663,1.0442,1.0000,
        1.0110,1.0110,1.0110,1.0110,1.0110,1.0110,1.0164,1.0164,1.0164,1.0164,1.0219,1.0328,1.0383,1.0492,1.0492,1.0492,1.0492,1.0711,1.0547,1.0711,1.0711,1.0656,1.0656,1.0656,1.0602,1.0656,1.0438,1.0000,
        1.0109,1.0109,1.0109,1.0109,1.0109,1.0109,1.0163,1.0163,1.0163,1.0163,1.0217,1.0325,1.0379,1.0487,1.0487,1.0487,1.0487,1.0703,1.0541,1.0703,1.0703,1.0703,1.0649,1.0649,1.0595,1.0649,1.0433,1.0000,
        1.0107,1.0107,1.0107,1.0107,1.0107,1.0107,1.0161,1.0161,1.0161,1.0161,1.0214,1.0321,1.0375,1.0482,1.0482,1.0482,1.0482,1.0696,1.0535,1.0696,1.0696,1.0696,1.0642,1.0642,1.0589,1.0642,1.0428,1.0000,
        1.0106,1.0106,1.0106,1.0106,1.0106,1.0106,1.0159,1.0159,1.0159,1.0159,1.0212,1.0318,1.0424,1.0477,1.0477,1.0477,1.0477,1.0688,1.0530,1.0688,1.0688,1.0688,1.0635,1.0635,1.0583,1.0635,1.0424,1.0000,
        1.0105,1.0105,1.0105,1.0105,1.0105,1.0105,1.0158,1.0158,1.0158,1.0210,1.0210,1.0367,1.0419,1.0472,1.0472,1.0472,1.0524,1.0681,1.0524,1.0681,1.0681,1.0681,1.0629,1.0629,1.0576,1.0629,1.0419,1.0000,
        1.0104,1.0104,1.0104,1.0104,1.0104,1.0104,1.0156,1.0156,1.0156,1.0208,1.0208,1.0363,1.0415,1.0467,1.0467,1.0467,1.0519,1.0674,1.0519,1.0674,1.0674,1.0674,1.0622,1.0622,1.0570,1.0622,1.0415,1.0000,
        1.0103,1.0103,1.0103,1.0103,1.0103,1.0103,1.0154,1.0154,1.0154,1.0206,1.0206,1.0359,1.0411,1.0462,1.0462,1.0462,1.0513,1.0667,1.0513,1.0667,1.0667,1.0667,1.0616,1.0616,1.0565,1.0616,1.0411,1.0000,
        1.0102,1.0102,1.0102,1.0102,1.0102,1.0102,1.0153,1.0153,1.0153,1.0204,1.0204,1.0356,1.0407,1.0457,1.0457,1.0457,1.0508,1.0660,1.0508,1.0660,1.0660,1.0660,1.0610,1.0610,1.0559,1.0610,1.0407,1.0000,
        1.0101,1.0101,1.0101,1.0101,1.0101,1.0101,1.0151,1.0151,1.0151,1.0202,1.0202,1.0352,1.0403,1.0453,1.0453,1.0453,1.0503,1.0654,1.0503,1.0704,1.0654,1.0654,1.0604,1.0604,1.0553,1.0604,1.0403,1.0000,
    ]),

    layer1HCalScaleETBins = cms.vint32([ 1 ,2 ,4 ,6 ,8 ,10 ,12 ,14 ,16 ,18 ,20 ,22 ,24 ,26 ,28 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,256]),
    layer1HCalScaleFactors = cms.vdouble([
        0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,3.1010,1.9938,2.4089,2.5911,2.4060,2.2019,2.0283,1.9430,1.8640,1.7654,0.7619,0.3981,0.4543,
        1.7112,1.6905,1.6456,1.5958,1.6722,1.6663,1.6892,1.7745,1.7824,1.8657,1.8934,1.9873,2.0255,2.1990,2.2416,2.4208,1.8883,2.2223,2.1683,1.9968,1.8048,1.7071,1.5361,1.4565,1.5978,1.0280,0.8558,0.0001,
        1.7138,1.8147,1.7428,1.7776,1.7274,1.7750,1.8060,1.8379,1.8347,1.9254,1.8979,2.0503,2.0485,2.0777,2.1482,2.1704,2.0273,2.1830,2.0078,1.9894,1.7846,1.5882,1.6139,1.5657,1.7671,1.3927,1.1437,0.2086,
        1.5364,1.5870,1.6196,1.5680,1.5850,1.5262,1.5746,1.5842,1.6411,1.6082,1.7030,1.6540,1.7563,1.6802,1.6701,1.7956,1.8203,1.8915,1.7514,1.7138,1.6773,1.6235,1.5851,1.5512,1.7762,1.5486,1.2095,0.7712,
        1.4384,1.4815,1.4759,1.4609,1.4395,1.5220,1.5120,1.4854,1.5278,1.5547,1.5766,1.5874,1.6212,1.6919,1.6502,1.7388,1.7627,1.8330,1.7190,1.7555,1.6797,1.5927,1.5745,1.5367,1.7500,1.5910,1.2327,0.9780,
        1.4475,1.4256,1.4173,1.4028,1.3937,1.5148,1.4525,1.4554,1.4427,1.4843,1.5743,1.5149,1.6438,1.6292,1.6591,1.7237,1.7587,1.8254,1.6971,1.6778,1.6279,1.5583,1.5546,1.5101,1.6388,1.5458,1.2425,1.0251,
        1.3416,1.3692,1.3659,1.4137,1.4020,1.4221,1.3636,1.3757,1.4429,1.4808,1.4852,1.4867,1.5600,1.6182,1.5008,1.6666,1.5921,1.6963,1.5594,1.6013,1.5405,1.4830,1.4344,1.4241,1.5462,1.4391,1.1182,1.0211,
        1.4137,1.3696,1.3299,1.3797,1.2819,1.3566,1.4286,1.3297,1.3850,1.3776,1.3861,1.4307,1.4961,1.5216,1.4614,1.6729,1.6184,1.5715,1.5394,1.5627,1.4279,1.3401,1.4201,1.3237,1.4102,1.4066,1.1360,0.9894,
        1.3025,1.2836,1.3603,1.3749,1.2225,1.2978,1.3008,1.2874,1.4031,1.4499,1.4165,1.4137,1.4147,1.4258,1.4226,1.5484,1.5300,1.5677,1.4630,1.4233,1.4158,1.3410,1.3309,1.3267,1.3581,1.2520,1.1117,1.0247,
        1.2551,1.3011,1.2605,1.2570,1.2633,1.3217,1.3416,1.2290,1.3166,1.3200,1.3735,1.3557,1.3552,1.4489,1.3991,1.4950,1.4802,1.4681,1.3851,1.4442,1.3701,1.3310,1.3308,1.2736,1.3310,1.2392,1.0895,0.9857,
        1.2737,1.2463,1.3297,1.3004,1.2475,1.3260,1.3235,1.3196,1.3015,1.3990,1.3311,1.3278,1.3277,1.4337,1.3109,1.4989,1.4838,1.4257,1.3566,1.3527,1.2976,1.2634,1.2759,1.2622,1.2802,1.2463,1.1073,1.0298,
        1.2321,1.2894,1.2845,1.2208,1.2359,1.3325,1.2087,1.2812,1.2381,1.2970,1.2766,1.2419,1.3407,1.3215,1.2897,1.4120,1.4545,1.3345,1.2559,1.3663,1.2509,1.2391,1.2960,1.2011,1.2888,1.2101,1.1015,0.9747,
        1.2042,1.1959,1.2595,1.2559,1.1636,1.2868,1.2253,1.2418,1.2806,1.2488,1.2383,1.2339,1.3280,1.2755,1.3079,1.3793,1.3995,1.3353,1.2944,1.2685,1.2400,1.1992,1.1466,1.1585,1.2395,1.1927,1.0308,0.9810,
        1.1983,1.2127,1.2180,1.2261,1.1614,1.2594,1.1909,1.1692,1.2603,1.1592,1.2482,1.2075,1.2796,1.2780,1.2852,1.3197,1.3881,1.3650,1.2512,1.2205,1.2369,1.2206,1.1672,1.1487,1.2540,1.1926,1.0740,1.0272,
        1.1646,1.1668,1.2450,1.2087,1.1403,1.2033,1.1864,1.2435,1.1832,1.2532,1.1931,1.1991,1.2363,1.2504,1.2749,1.3130,1.3514,1.3111,1.2240,1.2792,1.2267,1.1987,1.1668,1.1642,1.2104,1.1751,1.0430,0.9876,
        1.1212,1.1580,1.2487,1.1915,1.1200,1.2671,1.1628,1.2016,1.1965,1.2132,1.2338,1.2062,1.1900,1.2895,1.1892,1.3078,1.3022,1.2589,1.1985,1.2458,1.1936,1.1941,1.2002,1.1458,1.1849,1.1542,1.0289,0.9600,
        1.1897,1.1580,1.1872,1.1592,1.1834,1.1930,1.1904,1.1736,1.1725,1.2098,1.2377,1.1886,1.2190,1.2816,1.2110,1.2743,1.3353,1.1984,1.2064,1.2146,1.1968,1.1736,1.1865,1.1099,1.1485,1.1139,1.0433,0.9722,
        1.1230,1.1401,1.1676,1.1952,1.1232,1.1296,1.1879,1.1599,1.1214,1.1465,1.1629,1.1133,1.1415,1.1820,1.1778,1.2237,1.3470,1.1757,1.1241,1.1805,1.1635,1.1269,1.1101,1.1160,1.1508,1.1038,1.0963,0.9669,
        1.1322,1.1796,1.1139,1.1393,1.1532,1.1370,1.1491,1.1180,1.1569,1.1559,1.1048,1.1088,1.1774,1.1680,1.1602,1.2139,1.2955,1.1227,1.1383,1.0835,1.1272,1.0826,1.1125,1.0764,1.0879,1.0719,1.0053,0.9407,
        1.1026,1.0825,1.1337,1.1609,1.1034,1.1118,1.1111,1.1122,1.1025,1.1081,1.1471,1.0914,1.1474,1.1244,1.1581,1.1857,1.2901,1.1439,1.1410,1.0956,1.1232,1.1047,1.1002,1.0711,1.0756,1.0729,1.0231,0.9564,
        1.1114,1.1051,1.1344,1.1190,1.0891,1.1227,1.1268,1.1063,1.0859,1.1002,1.0849,1.0941,1.0833,1.0915,1.0937,1.1490,1.2365,1.1059,1.1077,1.1199,1.0742,1.0941,1.0626,1.0573,1.0836,1.0507,1.0018,0.9328,
        1.0913,1.1356,1.1493,1.1473,1.0798,1.1227,1.1016,1.0644,1.0319,1.0949,1.0850,1.0799,1.0967,1.0831,1.0671,1.1645,1.2291,1.1437,1.1288,1.0839,1.1263,1.0826,1.0812,1.0634,1.0764,1.0420,0.9610,0.9196,
        1.0889,1.0909,1.0936,1.1053,1.0852,1.1063,1.1117,1.0698,1.1018,1.0417,1.0634,1.0567,1.0590,1.0566,1.0753,1.1302,1.2150,1.0784,1.0901,1.0529,1.0928,1.0611,1.0857,1.0350,1.0520,1.0470,0.9659,0.9270,
        1.0865,1.0995,1.0463,1.0864,1.0360,1.1005,1.0686,1.0923,1.0699,1.0894,1.0582,1.0185,1.0439,1.0849,1.0753,1.1729,1.2073,1.0750,1.0641,1.0301,1.0570,1.0497,1.0602,1.0537,1.0475,1.0168,0.9799,0.9106,
        1.0821,1.0827,1.0925,1.1007,1.0421,1.1399,1.1067,1.0529,1.0729,1.0891,1.0643,1.0225,1.0731,1.0681,1.0632,1.1548,1.1897,1.0840,1.0638,1.0494,1.0633,1.0138,1.0600,1.0110,1.0627,1.0186,0.9417,0.8973,
        1.0936,1.0382,1.0530,1.0805,1.0504,1.0742,1.0318,1.0452,1.0713,1.0994,1.0607,1.0212,1.0535,1.0608,1.0202,1.1470,1.1987,1.0668,1.0525,1.1048,1.0616,1.0533,1.0608,1.0143,1.0085,1.0356,0.9595,0.8839,
        1.0323,1.0748,1.0816,1.0825,1.0193,1.1181,1.0512,1.0341,1.0334,1.0499,1.0372,1.0225,1.0511,1.0675,1.0734,1.1314,1.1568,1.0753,1.0465,1.0342,1.0524,1.0566,1.0166,1.0088,1.0221,0.9878,0.9456,0.8704,
        1.0573,1.0712,1.0686,1.0947,1.0447,1.0744,1.0541,1.0571,1.0429,1.0020,1.0466,1.0181,1.0068,1.0195,1.0227,1.1444,1.1803,1.0418,1.0441,1.0356,1.0420,1.0448,1.0323,1.0139,0.9933,1.0239,0.9777,0.8769,
        1.0591,1.0555,1.0454,1.0447,1.0060,1.0581,1.0631,1.0508,1.0316,1.0343,1.0136,1.0303,1.0628,1.0488,0.9853,1.1145,1.1754,1.0154,1.0708,1.0521,1.0297,1.0425,1.0101,0.9925,1.0410,1.0055,0.9357,0.8728,
        1.0885,1.0616,1.0530,1.0517,1.0371,1.0547,1.0586,1.0535,1.0488,1.0010,1.0294,0.9873,1.0286,0.9800,1.0198,1.0678,1.1173,1.0256,1.0139,1.0100,1.0460,1.0030,1.0484,1.0221,0.9863,1.0020,0.9406,0.9103,
        1.0285,1.0245,1.0075,1.0229,1.0038,1.0135,1.0131,1.0020,0.9860,0.9884,0.9912,0.9780,1.0053,1.0131,1.0087,1.0637,1.1203,0.9872,0.9991,1.0023,1.0172,1.0243,1.0257,0.9947,0.9831,0.9936,0.8621,0.8803,
    ]),

    layer1HFScaleETBins = cms.vint32([ 1 ,2 ,4 ,6 ,8 ,10 ,12 ,14 ,16 ,18 ,20 ,22 ,24 ,26 ,28 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,256]),
    layer1HFScaleFactors = cms.vdouble([
        1.2005,1.6347,1.5172,1.1301,0.7461,0.4248,0.1553,0.0979,0.0003,0.2530,0.5828,0.7505,
        0.3352,0.5184,0.3785,0.1349,0.0002,0.0000,0.0000,0.0000,0.0000,0.7015,0.9842,0.9537,
        0.1586,0.3199,0.2156,0.0117,0.0001,0.0003,0.0002,0.1776,0.5014,0.8973,1.0846,0.9983,
        0.5956,0.8420,0.8415,0.6843,0.6544,0.7681,0.9498,1.1367,1.2178,1.1962,1.0262,0.9985,
        0.8109,0.9432,0.9316,0.8640,0.8148,0.8828,0.9946,1.2056,1.2254,1.1621,1.0493,1.0008,
        0.8981,0.9895,0.9796,0.9515,0.8440,0.9290,1.0685,1.2068,1.2718,1.2041,1.0411,1.0000,
        0.9351,1.0134,0.9973,0.9520,0.8707,0.9617,1.0781,1.2312,1.2005,1.1107,1.0173,0.9959,
        0.9381,0.9988,0.9960,0.9627,0.8697,0.9484,1.0756,1.1059,1.1377,1.1014,1.0025,1.0000,
        0.9716,0.9917,1.0050,0.9688,0.8787,0.9452,1.0619,1.1624,1.1650,1.0583,1.0113,0.9950,
        0.9776,0.9918,1.0002,0.9723,0.8836,0.9359,1.0367,1.1032,1.1021,1.0483,1.0000,1.0000,
        1.0022,0.9743,1.0102,0.9643,0.8781,0.9382,1.0312,1.0647,1.0519,1.0664,1.0000,1.0000,
        1.0105,0.9673,1.0128,0.9660,0.8783,0.9327,1.0490,1.0244,1.0581,1.0216,1.0000,1.0000,
        1.0008,0.9650,1.0053,0.9632,0.8833,0.9500,0.9865,1.0460,1.0539,1.0216,1.0000,1.0000,
        1.0128,0.9533,1.0065,0.9501,0.8764,0.9383,1.0260,1.0389,1.0340,0.9922,1.0000,1.0000,
        1.0032,0.9467,1.0111,0.9513,0.8735,0.9345,0.9961,1.0204,1.0022,1.0151,1.0000,1.0000,
        1.0028,0.9490,1.0078,0.9661,0.8688,0.9205,0.9927,1.0452,1.0044,1.0113,1.0000,1.0000,
        1.0131,0.9433,1.0058,0.9470,0.8859,0.9381,0.9933,0.9668,0.9746,1.0224,1.0000,1.0000,
        0.9976,0.9302,0.9958,0.9407,0.8777,0.9171,0.9790,0.9991,1.0336,1.0090,1.0000,1.0000,
        1.0035,0.9358,1.0080,0.9388,0.8687,0.9296,0.9617,0.9891,0.9732,1.0033,1.0000,1.0000,
        0.9934,0.9281,0.9952,0.9398,0.8832,0.9127,0.9408,0.9798,0.9786,1.0000,1.0000,1.0000,
        0.9942,0.9249,0.9904,0.9418,0.8743,0.9157,0.9529,0.9483,0.9912,1.0000,1.0000,1.0000,
        0.9894,0.9258,0.9851,0.9346,0.8843,0.9123,0.9275,0.9890,1.0038,1.0000,1.0000,1.0000,
        0.9908,0.9259,0.9868,0.9311,0.8824,0.9103,0.9278,0.9500,1.0023,1.0000,1.0000,1.0000,
        1.0016,0.9307,0.9828,0.9317,0.8842,0.9127,0.9406,0.9814,0.9909,1.0079,1.0000,1.0000,
        1.0069,0.9227,0.9815,0.9266,0.8803,0.8920,0.9543,1.0057,0.9960,1.0000,1.0000,1.0000,
        1.0085,0.9234,0.9797,0.9286,0.8775,0.8975,0.9670,1.0000,1.0058,1.0000,1.0000,1.0000,
        1.0118,0.9310,0.9765,0.9371,0.8761,0.8861,0.9607,0.9914,1.0000,1.0000,1.0000,1.0000,
        1.0202,0.9267,0.9811,0.9263,0.8850,0.8942,0.9583,0.9939,0.9920,1.0000,1.0000,1.0000,
        1.0244,0.9272,0.9736,0.9190,0.8694,0.8951,0.9541,1.0000,0.9930,0.9937,1.0000,1.0000,
        1.0290,0.9272,0.9735,0.9248,0.8742,0.9145,0.9471,0.9897,1.0000,1.0000,1.0000,1.0000,
        1.0396,0.9264,0.9684,0.9214,0.8746,0.8962,0.9447,0.9807,1.0000,1.0000,1.0000,1.0000,
    ]),

    # HCal FB LUT
    layer1HCalFBLUTUpper = cms.vuint32([
    0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 
    ]),

    layer1HCalFBLUTLower = cms.vuint32([
    0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 
    ])
)
