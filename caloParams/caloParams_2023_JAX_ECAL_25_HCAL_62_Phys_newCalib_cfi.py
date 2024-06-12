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
    layer1ECalScaleETBins = cms.vint32([ 1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,256]),
    layer1ECalScaleFactors = cms.vdouble([
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,0.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,0.0000,
        0.9675,1.0010,0.9904,0.9871,1.0680,1.0695,1.0255,1.0495,1.1009,1.1193,1.0872,1.1462,1.3068,1.3605,1.2950,1.3341,1.3560,1.3661,1.3488,1.4790,1.4640,1.3964,1.2500,1.0791,0.9637,0.0000,0.0000,0.0000,
        1.0507,1.0241,1.0172,1.0262,1.1174,1.0868,1.0614,1.0762,1.1245,1.1206,1.1375,1.1491,1.2473,1.3239,1.2813,1.3012,1.3171,1.3605,1.2896,1.4226,1.4619,1.3650,1.2740,1.1424,1.0592,0.9885,0.0000,0.0000,
        1.0793,1.0448,1.0363,1.0604,1.0910,1.1133,1.0647,1.0773,1.0941,1.1198,1.1009,1.1330,1.2240,1.3176,1.2661,1.2944,1.2782,1.3401,1.2504,1.3659,1.3675,1.3160,1.2745,1.1549,1.1038,1.0468,0.0000,0.0000,
        1.0816,1.0612,1.0586,1.0584,1.0864,1.0934,1.0646,1.0845,1.0691,1.1055,1.1024,1.1314,1.1875,1.2702,1.2534,1.2623,1.2630,1.2751,1.2486,1.3796,1.3574,1.2921,1.2353,1.1891,1.1384,1.0896,0.0000,0.0000,
        1.0616,1.0650,1.0546,1.0546,1.0725,1.1052,1.0623,1.0783,1.0850,1.1207,1.0795,1.1207,1.1694,1.2574,1.2206,1.2696,1.2428,1.3098,1.1837,1.3330,1.3250,1.3057,1.2312,1.1680,1.1240,1.0887,1.0663,0.0000,
        1.0734,1.0555,1.0466,1.0511,1.0691,1.0754,1.0669,1.0623,1.0746,1.1013,1.1120,1.1331,1.1806,1.2440,1.2226,1.2475,1.2317,1.3001,1.2249,1.3069,1.3172,1.2966,1.2284,1.1587,1.1286,1.1047,1.1016,0.0000,
        1.0639,1.0569,1.0472,1.0616,1.0567,1.0745,1.0739,1.0736,1.0936,1.1190,1.1086,1.1264,1.1802,1.2295,1.2428,1.2305,1.2293,1.2786,1.2001,1.2985,1.3269,1.2816,1.2156,1.1668,1.1520,1.1009,1.0399,0.0000,
        1.0700,1.0635,1.0620,1.0560,1.0696,1.0879,1.0743,1.0616,1.0794,1.1008,1.1082,1.1271,1.1706,1.2134,1.2114,1.2298,1.2219,1.2851,1.2075,1.2962,1.2813,1.2550,1.2141,1.1842,1.1401,1.1217,1.0968,1.0000,
        1.0811,1.0658,1.0832,1.0727,1.0749,1.0761,1.0782,1.0752,1.0902,1.1145,1.1132,1.1058,1.1799,1.2153,1.2065,1.2197,1.2218,1.3320,1.2127,1.2875,1.2895,1.2752,1.2222,1.1897,1.1657,1.1493,1.1133,1.0000,
        1.0625,1.0847,1.0723,1.0791,1.0790,1.0895,1.0816,1.0868,1.0964,1.0999,1.1041,1.1275,1.1577,1.1960,1.2096,1.2031,1.2240,1.2644,1.1886,1.2984,1.2926,1.2486,1.2214,1.1862,1.1626,1.1416,1.1320,1.0000,
        1.0840,1.0678,1.0772,1.0831,1.0946,1.0930,1.0813,1.0755,1.0981,1.1117,1.0946,1.1293,1.1623,1.2029,1.1968,1.2072,1.2021,1.3026,1.2029,1.2580,1.2631,1.2535,1.2243,1.1760,1.1715,1.1386,1.0630,1.0000,
        1.0789,1.0706,1.0648,1.0752,1.0859,1.1084,1.0854,1.0815,1.0932,1.1054,1.1035,1.1233,1.1740,1.1863,1.1903,1.1893,1.2009,1.2749,1.1632,1.2793,1.2620,1.2440,1.2046,1.1812,1.1542,1.1245,1.0748,1.0000,
        1.0802,1.0702,1.0789,1.0762,1.0946,1.0859,1.0835,1.0849,1.1038,1.1103,1.1214,1.1214,1.1673,1.1955,1.1851,1.2066,1.2143,1.2803,1.1760,1.2594,1.2589,1.2432,1.2103,1.1901,1.1612,1.1506,1.1321,1.0000,
        1.0746,1.0708,1.0834,1.0794,1.0811,1.0909,1.0764,1.0742,1.0963,1.1071,1.1110,1.1298,1.1707,1.1758,1.1754,1.2044,1.1983,1.2983,1.1732,1.2498,1.2494,1.2327,1.2011,1.1753,1.1604,1.1420,1.1274,1.0000,
        1.0809,1.0762,1.0776,1.0770,1.0857,1.0951,1.0796,1.0975,1.0946,1.1133,1.1126,1.1168,1.1621,1.1922,1.1845,1.1974,1.2146,1.2608,1.1656,1.2490,1.2471,1.2346,1.2010,1.1725,1.1697,1.1765,1.1550,1.0000,
        1.0892,1.0756,1.0792,1.0857,1.0987,1.1008,1.0832,1.0933,1.1134,1.1051,1.1212,1.1316,1.1551,1.1897,1.1817,1.1931,1.1902,1.2552,1.1745,1.2478,1.2449,1.2222,1.1911,1.1782,1.1542,1.1626,1.1238,1.0000,
        1.0921,1.0774,1.0794,1.0835,1.0854,1.0983,1.0873,1.0848,1.0920,1.1044,1.1086,1.1248,1.1546,1.1756,1.1728,1.1927,1.1940,1.2509,1.1792,1.2399,1.2326,1.2232,1.1907,1.1727,1.1557,1.1300,1.0908,1.0000,
        1.0748,1.0720,1.0706,1.0756,1.0889,1.0885,1.0756,1.0870,1.0911,1.0966,1.1065,1.1144,1.1457,1.1686,1.1723,1.1769,1.1849,1.2626,1.1754,1.2268,1.2243,1.2124,1.1844,1.1712,1.1495,1.1558,1.1075,1.0000,
        1.0686,1.0753,1.0721,1.0697,1.0811,1.0850,1.0791,1.0816,1.0938,1.0963,1.0958,1.1168,1.1410,1.1647,1.1650,1.1807,1.1662,1.2274,1.1646,1.2220,1.2322,1.2011,1.1814,1.1665,1.1451,1.1360,1.1101,1.0000,
        1.0713,1.0642,1.0687,1.0660,1.0783,1.0860,1.0786,1.0877,1.0899,1.0952,1.1009,1.1075,1.1422,1.1493,1.1517,1.1699,1.1733,1.2297,1.1490,1.2280,1.2039,1.1982,1.1781,1.1572,1.1397,1.1444,1.0364,1.0000,
        1.0678,1.0619,1.0612,1.0675,1.0758,1.0752,1.0753,1.0741,1.0854,1.0834,1.0926,1.1128,1.1328,1.1518,1.1537,1.1558,1.1627,1.2236,1.1496,1.2070,1.2107,1.1912,1.1691,1.1453,1.1259,1.1303,1.0442,1.0000,
        1.0643,1.0664,1.0633,1.0633,1.0688,1.0763,1.0781,1.0717,1.0809,1.0880,1.0908,1.1023,1.1282,1.1445,1.1445,1.1523,1.1565,1.2372,1.1512,1.1973,1.2043,1.1863,1.1705,1.1457,1.1355,1.1345,1.0222,1.0000,
        1.0677,1.0632,1.0654,1.0589,1.0703,1.0696,1.0699,1.0720,1.0805,1.0823,1.0895,1.0968,1.1159,1.1391,1.1392,1.1470,1.1520,1.2158,1.1480,1.2052,1.1986,1.1794,1.1590,1.1436,1.1233,1.1304,1.0193,1.0000,
        1.0567,1.0574,1.0547,1.0572,1.0595,1.0624,1.0570,1.0640,1.0686,1.0744,1.0808,1.0864,1.1055,1.1303,1.1262,1.1377,1.1402,1.2006,1.1290,1.1856,1.1820,1.1642,1.1444,1.1259,1.1154,1.1249,1.1140,1.0000,
        1.0427,1.0493,1.0456,1.0498,1.0536,1.0561,1.0543,1.0548,1.0609,1.0698,1.0758,1.0865,1.0944,1.1061,1.1143,1.1176,1.1211,1.1714,1.1175,1.1636,1.1593,1.1455,1.1288,1.1074,1.0981,1.1105,1.0047,1.0000,
        1.0455,1.0452,1.0411,1.0478,1.0457,1.0486,1.0499,1.0484,1.0553,1.0545,1.0615,1.0701,1.0868,1.0994,1.0958,1.1004,1.1061,1.1471,1.0986,1.1412,1.1318,1.1251,1.1061,1.0912,1.0758,1.0866,0.9999,1.0000,
        1.0377,1.0330,1.0341,1.0368,1.0407,1.0360,1.0383,1.0402,1.0443,1.0495,1.0492,1.0559,1.0709,1.0851,1.0853,1.0883,1.0923,1.1348,1.0787,1.1185,1.1159,1.0998,1.0940,1.0768,1.0608,1.0752,1.0125,1.0000,
        1.0330,1.0283,1.0300,1.0289,1.0325,1.0353,1.0339,1.0310,1.0372,1.0418,1.0464,1.0491,1.0600,1.0705,1.0754,1.0760,1.0818,1.1017,1.0674,1.1091,1.1023,1.0969,1.0821,1.0675,1.0533,1.0670,1.0098,1.0000,
        1.0287,1.0252,1.0274,1.0246,1.0318,1.0302,1.0354,1.0337,1.0294,1.0381,1.0409,1.0456,1.0533,1.0672,1.0703,1.0750,1.0782,1.1079,1.0669,1.1008,1.0946,1.0895,1.0661,1.0606,1.0481,1.0460,0.9904,1.0000,
        1.0264,1.0278,1.0262,1.0247,1.0313,1.0316,1.0292,1.0276,1.0321,1.0323,1.0351,1.0462,1.0513,1.0600,1.0624,1.0704,1.0718,1.1040,1.0520,1.0872,1.0870,1.0751,1.0669,1.0618,1.0489,1.0507,1.0000,1.0000,
        1.0256,1.0225,1.0258,1.0179,1.0232,1.0280,1.0248,1.0313,1.0317,1.0317,1.0354,1.0396,1.0462,1.0574,1.0576,1.0629,1.0726,1.0894,1.0588,1.0798,1.0724,1.0721,1.0639,1.0461,1.0358,1.0365,1.0111,1.0000,
        1.0236,1.0188,1.0232,1.0221,1.0234,1.0251,1.0249,1.0237,1.0291,1.0334,1.0322,1.0352,1.0436,1.0529,1.0535,1.0583,1.0640,1.0825,1.0633,1.0772,1.0763,1.0609,1.0681,1.0532,1.0414,1.0338,1.0000,1.0000,
        1.0226,1.0200,1.0191,1.0155,1.0190,1.0215,1.0213,1.0276,1.0233,1.0283,1.0328,1.0395,1.0479,1.0481,1.0481,1.0610,1.0546,1.0800,1.0497,1.0823,1.0686,1.0724,1.0386,1.0389,1.0455,1.0342,1.0000,1.0000,
        1.0184,1.0191,1.0218,1.0203,1.0184,1.0239,1.0204,1.0228,1.0226,1.0294,1.0257,1.0379,1.0381,1.0499,1.0501,1.0457,1.0639,1.0330,1.0407,1.0742,1.0629,1.0514,1.0426,1.0302,1.0228,1.0441,1.0000,1.0000,
        1.0194,1.0200,1.0188,1.0200,1.0212,1.0180,1.0213,1.0276,1.0256,1.0240,1.0170,1.0310,1.0420,1.0425,1.0510,1.0560,1.0657,1.0379,1.0434,1.0580,1.0666,1.0582,1.0470,1.0276,1.0162,1.0443,1.0000,1.0000,
        1.0208,1.0174,1.0160,1.0160,1.0247,1.0203,1.0191,1.0188,1.0232,1.0200,1.0264,1.0360,1.0304,1.0344,1.0400,1.0384,1.0535,1.0639,1.0331,1.0540,1.0513,1.0499,1.0233,1.0415,1.0281,0.9986,1.0000,1.0000,
        1.0169,1.0132,1.0113,1.0109,1.0137,1.0186,1.0122,1.0106,1.0229,1.0180,1.0178,1.0241,1.0318,1.0405,1.0283,1.0411,1.0571,1.0443,1.0424,1.0695,1.0600,1.0568,1.0524,1.0393,1.0185,1.0138,1.0000,1.0000,
        1.0133,1.0168,1.0204,1.0190,1.0147,1.0201,1.0168,1.0101,1.0217,1.0178,1.0279,1.0214,1.0334,1.0272,1.0509,1.0407,1.0574,1.0210,1.0396,1.0442,1.0650,1.0160,1.0468,1.0341,1.0304,0.9995,1.0000,1.0000,
        1.0141,1.0113,1.0126,1.0109,1.0139,1.0146,1.0164,1.0148,1.0169,1.0150,1.0196,1.0225,1.0344,1.0299,1.0305,1.0404,1.0462,1.0387,1.0149,1.0588,1.0536,1.0560,1.0341,1.0209,1.0047,1.0000,1.0000,1.0000,
    ]),

    layer1HCalScaleETBins = cms.vint32([ 1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,256]),
    layer1HCalScaleFactors = cms.vdouble([
        0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,2.0000,1.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,2.0000,0.0000,0.0000,0.0000,
        1.8661,1.9588,1.9092,1.8821,1.9771,1.9460,1.9608,1.9962,2.0812,2.0440,2.1416,2.2280,2.2734,2.3122,2.6816,2.5678,2.4036,2.4802,2.5251,2.2666,1.9139,1.7640,1.6464,1.7089,1.9667,1.3999,1.8711,0.0000,
        1.6941,1.6945,1.6522,1.6731,1.6837,1.7130,1.7496,1.6473,1.7072,1.7202,1.7850,1.8083,1.8491,1.8936,2.0308,2.0015,2.0384,1.9672,2.0141,1.8688,1.7320,1.6318,1.5901,1.5480,1.8783,1.9281,1.8650,1.2694,
        1.5015,1.5146,1.4478,1.5290,1.5656,1.5968,1.5256,1.4715,1.5118,1.6016,1.6084,1.6200,1.6969,1.6678,1.8039,1.7886,1.8615,1.8868,1.7416,1.7268,1.7178,1.6355,1.5775,1.5623,1.8335,1.9140,1.7842,1.6116,
        1.3505,1.4497,1.3891,1.4171,1.4596,1.5136,1.4374,1.4373,1.5103,1.5074,1.5184,1.5525,1.6546,1.6566,1.7963,1.8876,1.8491,1.8843,1.7578,1.7760,1.6849,1.5885,1.6001,1.5777,1.7358,1.7861,1.7360,1.6164,
        1.3498,1.3844,1.4306,1.3710,1.3738,1.3595,1.3817,1.3176,1.3977,1.4503,1.4490,1.4916,1.5470,1.5477,1.6896,1.7066,1.7487,1.7877,1.6774,1.6605,1.5806,1.5067,1.5073,1.5438,1.7080,1.6791,1.5368,1.5482,
        1.2991,1.3567,1.3199,1.3090,1.3291,1.3845,1.3742,1.2640,1.3612,1.3860,1.3426,1.3744,1.4763,1.5329,1.5549,1.6985,1.7385,1.6951,1.6588,1.5683,1.4652,1.4632,1.4369,1.4649,1.5746,1.6316,1.5138,1.5770,
        1.3222,1.3095,1.3101,1.3987,1.3258,1.3111,1.3833,1.3024,1.3588,1.4182,1.3729,1.3837,1.4312,1.5268,1.4960,1.5832,1.5867,1.6618,1.5447,1.4906,1.4424,1.3276,1.4373,1.3927,1.4514,1.5760,1.5077,1.5751,
        1.1798,1.2478,1.3225,1.3115,1.3128,1.3248,1.2837,1.2537,1.3153,1.4059,1.3079,1.3546,1.3657,1.3580,1.4362,1.5772,1.5666,1.5615,1.4948,1.5240,1.4120,1.3307,1.3355,1.3098,1.4068,1.5475,1.4075,1.5827,
        1.2002,1.2772,1.3180,1.2974,1.2756,1.2946,1.2020,1.2836,1.2582,1.3032,1.3083,1.2790,1.3858,1.3896,1.4050,1.4855,1.5506,1.5039,1.3772,1.4041,1.3127,1.3928,1.3899,1.2741,1.3833,1.5098,1.3797,1.6252,
        1.1683,1.2377,1.2931,1.2152,1.1983,1.2939,1.2688,1.1842,1.1842,1.3015,1.2379,1.3105,1.3144,1.3841,1.3158,1.4738,1.4776,1.4758,1.3623,1.3629,1.3512,1.2595,1.2917,1.2477,1.3654,1.5068,1.3812,1.6114,
        1.2746,1.1951,1.1964,1.2679,1.1553,1.2681,1.2765,1.1631,1.2251,1.3068,1.2641,1.1863,1.2818,1.3712,1.3840,1.4205,1.4350,1.4132,1.3668,1.3529,1.3036,1.2783,1.3294,1.2513,1.3664,1.5467,1.3462,1.5948,
        1.1776,1.1823,1.2089,1.1790,1.1735,1.2442,1.2387,1.2053,1.2085,1.2094,1.1755,1.2259,1.3057,1.3110,1.2833,1.3884,1.4007,1.3955,1.3469,1.2990,1.2647,1.2626,1.3247,1.2569,1.3020,1.3286,1.4087,1.5767,
        1.1395,1.1869,1.1364,1.2001,1.1964,1.3119,1.2528,1.1152,1.1417,1.2346,1.1581,1.1533,1.2555,1.2550,1.2515,1.4544,1.4346,1.4033,1.3078,1.2676,1.3349,1.1600,1.2737,1.1970,1.2621,1.4284,1.3207,1.5918,
        1.1266,1.1267,1.1211,1.0957,1.1677,1.2439,1.1990,1.1598,1.1553,1.2183,1.1586,1.1523,1.2300,1.2980,1.1965,1.3080,1.3572,1.3021,1.2160,1.3314,1.2321,1.2439,1.2195,1.1864,1.2579,1.4335,1.2799,1.5647,
        1.1477,1.1390,1.1662,1.1847,1.1489,1.2014,1.1911,1.1424,1.1620,1.2016,1.1298,1.1709,1.1991,1.2045,1.3232,1.3841,1.3376,1.3734,1.2495,1.3052,1.2863,1.2501,1.2545,1.2025,1.2713,1.3638,1.2948,1.5345,
        1.0932,1.1282,1.1168,1.2197,1.1973,1.1978,1.2340,1.1352,1.1450,1.2224,1.0955,1.1473,1.1762,1.2550,1.2290,1.2872,1.2695,1.3267,1.2843,1.2676,1.2005,1.1871,1.2908,1.1590,1.2114,1.3522,1.2861,1.4670,
        1.0693,1.1401,1.0889,1.1446,1.1570,1.2394,1.0947,1.1244,1.1045,1.1436,1.1271,1.0907,1.1873,1.1550,1.2258,1.3165,1.2937,1.3054,1.2328,1.2303,1.2110,1.2215,1.2278,1.1476,1.1981,1.3574,1.2139,1.5131,
        1.1163,1.1696,1.0820,1.1059,1.1689,1.1817,1.0717,1.1288,1.1073,1.2024,1.1088,1.0873,1.1830,1.1996,1.1921,1.3053,1.2893,1.2653,1.2114,1.2151,1.2155,1.1896,1.2153,1.1765,1.2111,1.3708,1.1929,1.3768,
        1.0647,1.1402,1.1036,1.1472,1.1104,1.1711,1.1964,1.0338,1.0775,1.1371,1.1124,1.0783,1.1471,1.2093,1.1429,1.3450,1.3012,1.2488,1.2143,1.2136,1.1975,1.1874,1.2264,1.1042,1.1942,1.3043,1.2305,1.4543,
        0.9679,1.0874,1.0458,1.0941,1.1604,1.1265,1.1515,1.0806,1.1143,1.1547,1.0443,1.0612,1.1025,1.1744,1.1692,1.3198,1.2276,1.2767,1.2011,1.2072,1.1821,1.1912,1.2013,1.1790,1.2240,1.3779,1.2332,1.4648,
        1.0064,1.0426,1.0750,1.1199,1.0889,1.1450,1.1475,1.0632,1.1101,1.1633,1.0471,1.1371,1.1499,1.2003,1.1516,1.3273,1.2652,1.2714,1.2352,1.1643,1.1701,1.1382,1.1856,1.1124,1.1823,1.3640,1.1910,1.4603,
        1.0872,1.0750,1.0824,1.0944,1.0824,1.1308,1.1210,1.0199,1.1175,1.0786,1.0539,1.0149,1.0860,1.1490,1.1725,1.2979,1.2519,1.2211,1.1990,1.1970,1.1396,1.1826,1.2215,1.1643,1.2436,1.3346,1.1464,1.4311,
        1.1230,1.0563,1.0764,1.0688,1.0265,1.1713,1.0707,1.0809,1.0465,1.1294,1.0589,1.0647,1.1693,1.1413,1.1481,1.2735,1.2412,1.1928,1.2231,1.1660,1.1745,1.1116,1.2330,1.1165,1.1433,1.2982,1.1779,1.3984,
        1.0322,1.0779,1.0046,1.1263,1.1512,1.1918,1.0863,1.0283,1.0010,1.0725,0.9812,1.0426,1.1399,1.1927,1.2190,1.3400,1.2135,1.2461,1.2241,1.1317,1.1342,1.1645,1.1191,1.1149,1.1544,1.3498,1.1787,1.4185,
        1.0488,1.0309,1.0121,1.0432,1.0961,1.1423,1.0901,1.0126,0.9968,1.0539,0.9784,1.0052,1.0712,1.1452,1.1428,1.3405,1.2623,1.2190,1.2000,1.2195,1.1786,1.1165,1.1940,1.0885,1.1621,1.4138,1.4081,1.4655,
        0.9933,1.0101,1.0347,1.0607,1.0540,1.1202,1.0621,0.9978,0.9871,1.0145,0.9733,1.0338,1.0578,1.1345,1.1202,1.3476,1.2241,1.1706,1.1740,1.1783,1.1333,1.1252,1.1746,1.0904,1.1277,1.3960,1.3348,1.3779,
        0.9952,1.0149,0.9930,1.0000,1.0279,1.0875,1.0421,0.9581,0.9580,1.0338,1.0075,0.9569,1.0791,1.0853,1.1219,1.3147,1.2048,1.1473,1.1284,1.1693,1.1327,1.1037,1.1772,1.0815,1.1410,1.3377,1.3198,1.3406,
        0.9822,1.0000,0.9602,0.9886,0.9994,1.0798,0.9812,0.9719,0.9253,0.9966,0.9664,0.9796,1.0005,1.0805,1.0891,1.3700,1.2195,1.1387,1.1137,1.1378,1.1127,1.0849,1.1605,1.0852,1.0752,1.3948,1.2511,1.3734,
        0.9612,1.0224,0.9558,1.0066,1.0090,1.0404,1.0219,0.9511,0.9122,1.0020,0.9065,0.9408,1.0010,1.0496,1.0817,1.3364,1.2232,1.1323,1.0822,1.1521,1.0978,1.0765,1.1492,1.0755,1.0806,1.3193,1.1963,1.4075,
        0.9791,0.9958,0.9333,0.9790,0.9823,1.0495,0.9908,0.9489,0.9235,0.9550,0.8821,0.9830,1.0093,1.0533,1.0804,1.3376,1.1175,1.1168,1.0645,1.0886,1.1140,1.0910,1.1298,1.0356,1.0521,1.3375,1.1331,1.3565,
        0.9677,0.9789,0.9462,1.0226,0.9808,1.0083,1.0020,0.9557,0.8975,0.9455,0.9000,0.9300,0.9668,1.0187,1.0523,1.3414,1.1423,1.1047,1.1136,1.1268,1.0795,1.0796,1.1208,1.0664,1.0655,1.3221,1.1086,1.2465,
        0.9359,0.9831,0.9143,0.9822,0.9680,1.0385,0.9846,0.9586,0.8606,0.9330,0.8877,0.9025,0.9547,1.0713,1.0665,1.3351,1.1617,1.1182,1.0958,1.0969,1.0407,1.0758,1.1293,1.0637,1.0463,1.3076,1.0904,1.1550,
        0.9254,1.0179,0.9451,0.9742,0.9527,1.0252,0.9761,0.9234,0.8634,0.9222,0.9367,0.9435,0.9677,1.0411,1.0835,1.2937,1.1789,1.0793,1.0919,1.0777,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9563,0.9792,0.9390,0.9822,0.9585,0.9869,0.9673,0.9012,0.9070,0.9400,0.8708,0.9388,0.9672,1.0239,1.0470,1.2813,1.1060,1.0856,1.0708,1.0715,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9393,0.9834,0.9268,0.9959,0.9746,0.9734,0.9526,0.9461,0.8845,0.9308,0.8422,0.9141,0.9468,1.0362,1.0265,1.2490,1.1186,1.0947,1.0695,1.0651,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9380,0.9527,0.8892,0.9421,0.9603,1.0179,0.9641,0.9317,0.8681,0.9380,0.8724,0.9160,0.9574,1.0157,1.0841,1.2753,1.0636,1.0751,1.0786,1.0998,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9391,0.9692,0.9077,0.9290,0.9317,0.9997,0.9450,0.9276,0.8888,0.9378,0.8980,0.9348,0.9861,1.0134,1.0268,1.2635,1.0404,1.0718,1.0435,1.0729,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9376,0.9846,0.8980,0.9749,0.9453,0.9856,0.9359,0.8922,0.9127,0.9103,0.8424,0.9400,0.9341,1.0146,1.0408,1.2609,1.0221,1.0753,1.0852,1.0750,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9345,0.9664,0.8813,0.9560,0.9341,0.9760,0.9560,0.8878,0.8956,0.9474,0.8709,0.9543,0.9821,1.0384,1.0471,1.2950,1.0274,1.0693,1.0704,1.0979,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        0.9189,0.9769,0.8939,0.9682,0.9203,0.9591,0.9472,0.8970,0.8532,0.9223,0.8257,0.9014,0.9457,1.0543,1.0390,1.2508,1.0330,1.0825,1.0371,1.0592,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
    ]),

    layer1HFScaleETBins = cms.vint32([ 1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,30 ,35 ,40 ,45 ,50 ,55 ,60 ,65 ,70 ,75 ,80 ,85 ,90 ,95 ,100 ,256]),
    layer1HFScaleFactors = cms.vdouble([
        1.5000,2.0000,1.5000,1.0000,0.5000,0.5000,0.5000,0.0000,0.0000,0.5000,0.5000,1.0000,
        0.3338,0.5392,0.3274,0.0005,0.0004,0.0002,0.0004,0.0000,0.2046,0.9095,1.0919,0.9937,
        0.3679,0.6483,0.5619,0.2062,0.1440,0.3867,0.6976,1.2548,1.3379,1.1690,1.0512,0.9937,
        0.7201,0.8767,0.8472,0.6493,0.5998,0.9625,1.1189,1.4437,1.4196,1.2118,1.0174,0.9961,
        0.8977,0.9806,0.9698,0.8971,0.8540,1.2630,1.4026,1.5567,1.5789,1.2687,1.0328,1.0077,
        0.9682,1.0264,1.0228,0.9675,0.9016,1.2668,1.4488,1.4495,1.4249,1.2623,1.0232,0.9962,
        0.9942,1.0434,1.0479,0.9979,0.9504,1.2682,1.3833,1.4317,1.2550,1.1103,1.0104,0.9972,
        1.0103,1.0408,1.0483,1.0342,0.9806,1.3137,1.3197,1.3952,1.2463,1.1219,0.9989,0.9967,
        1.0481,1.0398,1.0602,1.0495,0.9518,1.2903,1.3312,1.3017,1.1643,1.0556,1.0000,1.0000,
        1.0492,1.0394,1.0680,1.0401,0.9808,1.2657,1.3243,1.2576,1.1519,1.0279,0.9988,0.9970,
        1.0554,1.0276,1.0577,1.0693,0.9862,1.2916,1.2786,1.2860,1.0972,1.0250,1.0000,1.0000,
        1.0599,1.0185,1.0650,1.0751,0.9785,1.2552,1.2706,1.2211,1.1024,1.0202,0.9962,0.9907,
        1.0616,0.9995,1.0581,1.0732,0.9764,1.2511,1.2444,1.1654,1.0648,1.0288,1.0000,1.0000,
        1.0627,1.0014,1.0588,1.0661,0.9756,1.2697,1.2120,1.1503,1.0716,1.0194,1.0000,1.0000,
        1.0491,0.9979,1.0553,1.0819,0.9769,1.2345,1.2655,1.1297,1.0365,0.9947,1.0000,1.0000,
        1.0559,0.9893,1.0773,1.0698,0.9864,1.2536,1.1743,1.1621,1.0184,1.0162,1.0000,1.0000,
        1.0484,0.9903,1.0791,1.0836,0.9718,1.2470,1.1843,1.0901,1.0304,0.9913,0.9938,1.0000,
        1.0413,0.9827,1.0820,1.0764,0.9756,1.2141,1.2111,1.0933,1.0414,1.0026,0.9916,1.0000,
        1.0446,0.9720,1.0738,1.0753,0.9772,1.2422,1.1781,1.0780,1.0151,0.9940,1.0000,1.0000,
        1.0304,0.9761,1.0808,1.0787,0.9400,1.2408,1.1569,1.0612,1.0228,0.9977,1.0000,1.0000,
        1.0368,0.9756,1.0647,1.0805,1.0014,1.2270,1.1686,1.0174,1.0326,0.9976,1.0000,1.0000,
        1.0361,0.9765,1.0838,1.0760,0.9601,1.2187,1.1357,1.0146,1.0129,0.9985,1.0000,1.0000,
        1.0268,0.9761,1.0744,1.0868,0.9742,1.2164,1.1647,1.0382,0.9861,0.9897,1.0000,1.0000,
        1.0376,0.9729,1.0646,1.0738,0.9588,1.2256,1.1216,1.0303,1.0021,0.9976,1.0000,1.0000,
        1.0292,0.9759,1.0772,1.0896,0.9512,1.2221,1.1469,1.0292,1.0127,1.0000,1.0000,1.0000,
        1.0434,0.9826,1.0669,1.0752,0.9811,1.2133,1.1814,1.0179,1.0287,1.0081,0.9782,0.9806,
        1.0499,0.9832,1.0632,1.0705,0.9853,1.2058,1.1816,1.0732,0.9748,1.0116,0.9868,1.0000,
        1.0623,0.9882,1.0598,1.0641,0.9819,1.1929,1.1192,1.0083,0.9795,1.0088,1.0000,1.0000,
        1.0827,0.9914,1.0576,1.0593,0.9938,1.1537,1.0854,0.9533,0.9766,1.0000,1.0000,1.0000,
        1.0911,0.9966,1.0552,1.0597,0.9974,1.1509,1.0627,0.9756,0.9982,1.0000,1.0000,1.0000,
        1.1007,0.9938,1.0468,1.0617,0.9870,1.1625,1.0592,1.0000,1.0070,0.9593,1.0000,1.0000,
        1.1164,0.9937,1.0462,1.0548,0.9865,1.0930,1.0001,1.0214,1.0020,1.0000,1.0000,1.0000,
        1.1119,0.9908,1.0429,1.0572,0.9851,1.0831,0.9908,1.0000,0.9779,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
        1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,1.0000,
    ]),

    # HCal FB LUT
    layer1HCalFBLUTUpper = cms.vuint32([
    0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 
    ]),

    layer1HCalFBLUTLower = cms.vuint32([
    0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 0xBBBABBBA, 
    ])
)