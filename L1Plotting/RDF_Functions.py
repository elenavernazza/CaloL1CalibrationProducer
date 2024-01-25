import ROOT

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<ROOT::RVec<int>> Matching(Vfloat L1_pt, Vfloat L1_eta, Vfloat L1_phi, Vfloat Offline_pt, Vfloat Offline_eta, Vfloat Offline_phi) {
        ROOT::RVec<int> good_L1;
        ROOT::RVec<int> good_Of;
        for (int i_Of = 0; i_Of < Offline_pt.size(); i_Of ++) {
            auto Of_part_tlv = TLorentzVector();
            Of_part_tlv.SetPtEtaPhiM(Offline_pt.at(i_Of), Offline_eta.at(i_Of), Offline_phi.at(i_Of), 0);
            float highestL1_pt = -1;
            int highestL1_pt_idx = -1;
            for (int i_L1 = 0; i_L1 < L1_pt.size(); i_L1 ++) {
                // Skip if this online jet has already been matched
                auto L1_part_tlv = TLorentzVector();
                L1_part_tlv.SetPtEtaPhiM(L1_pt.at(i_L1), L1_eta.at(i_L1), L1_phi.at(i_L1), 0);
                if (Of_part_tlv.DeltaR(L1_part_tlv) < 0.5) {
                    if (L1_part_tlv.Pt() > highestL1_pt) {
                        highestL1_pt = L1_part_tlv.Pt();
                        highestL1_pt_idx = i_L1;
                    }
                }
            }
            if (highestL1_pt_idx != -1) {
                good_L1.push_back(highestL1_pt_idx);
                good_Of.push_back(i_Of);
            }
        }
        // for (int i = 0; i < good_L1.size(); ++i) {
        //     cout << L1_pt.at(good_L1.at(i)) << ", " << Offline_pt.at(good_Of.at(i)) << endl;
        // }

        return {good_L1, good_Of};

    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    using Vint = const ROOT::RVec<int>&;
    ROOT::RVec<float> SelectGood (Vfloat Jets, Vint good) {
        ROOT::RVec<float> good_jets;
        for (int i = 0; i < good.size(); ++i) {
            good_jets.push_back(Jets.at(good.at(i)));
        }
        return good_jets;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> GetRatio (Vfloat A, Vfloat B) {
        ROOT::RVec<float> ratio;
        for (int i = 0; i < A.size(); ++i) {
            ratio.push_back(A.at(i)/B.at(i));
        }
        return ratio;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> GetSum (Vfloat A, Vfloat B) {
        ROOT::RVec<float> sum;
        for (int i = 0; i < A.size(); ++i) {
            sum.push_back(A.at(i) + B.at(i));
        }
        return sum;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> SelectBarrel (Vfloat A, Vfloat good_Of_eta) {
        ROOT::RVec<float> A_barrel;
        for (int i = 0; i < good_Of_eta.size(); ++i) {
            if (good_Of_eta.at(i) < 1.305) {
                A_barrel.push_back(A.at(i));
            }
        }
        return A_barrel;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> SelectEndcap (Vfloat A, Vfloat good_Of_eta) {
        ROOT::RVec<float> A_barrel;
        for (int i = 0; i < good_Of_eta.size(); ++i) {
            if (good_Of_eta.at(i) > 1.479) {
                A_barrel.push_back(A.at(i));
            }
        }
        return A_barrel;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> SelectBin (Vfloat A, Vfloat B, float l_bin, float u_bin) {
        ROOT::RVec<float> A_SelectBin;
        for (int i = 0; i < B.size(); ++i) {
            if ((B.at(i) >= l_bin) && (B.at(i) < u_bin)) {
                A_SelectBin.push_back(A.at(i));
            }
        }
        return A_SelectBin;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> SelectBinAbs (Vfloat A, Vfloat B, float l_bin, float u_bin) {
        ROOT::RVec<float> A_SelectBin;
        for (int i = 0; i < B.size(); ++i) {
            if ((abs(B.at(i)) >= l_bin) && (abs(B.at(i)) < u_bin)) {
                A_SelectBin.push_back(A.at(i));
            }
        }
        return A_SelectBin;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> PassThreshold (Vfloat A, Vfloat B, float thr) {
        ROOT::RVec<float> A_SelectBin;
        for (int i = 0; i < B.size(); ++i) {
            if (B.at(i) > thr) {
                A_SelectBin.push_back(A.at(i));
            }
        }
        return A_SelectBin;
    }
""")

ROOT.gInterpreter.Declare("""  
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> FindIeta(Vfloat eta) {
                            
        map<const int, std::vector<float>> TowersEta = {
        {1, {0,      0.087}},   {2, {0.087,  0.174}},   {3, {0.174,  0.261}},   {4, {0.261,  0.348}},   {5, {0.348,  0.435}},
        {6, {0.435,  0.522}},   {7, {0.522,  0.609}},   {8, {0.609,  0.696}},   {9, {0.696,  0.783}},   {10, {0.783, 0.870}},
        {11, {0.870, 0.957}},   {12, {0.957, 1.044}},   {13, {1.044, 1.131}},   {14, {1.131, 1.218}},   {15, {1.218, 1.305}},
        {16, {1.305, 1.392}},   {17, {1.392, 1.479}},   {18, {1.479, 1.566}},   {19, {1.566, 1.653}},   {20, {1.653, 1.740}},
        {21, {1.740, 1.830}},   {22, {1.830, 1.930}},   {23, {1.930, 2.043}},   {24, {2.043, 2.172}},   {25, {2.172, 2.322}},   
        {26, {2.322, 2.500}},   {27, {2.50,  2.650}},   {28, {2.650, 3.000}},   {30, {3.000, 3.139}},
        // {29: {2.830, 3.000}}, Should not be considered. Summed with TT28, such that TT28 goes to |eta| = 3 and summed with TT30, such that TT30 starts at |eta| = 3
        {31, {3.139, 3.314}},   {32, {3.314, 3.489}},   {33, {3.489, 3.664}},   {34, {3.664, 3.839}},   {35, {3.839, 4.013}},
        {36, {4.013, 4.191}},   {37, {4.191, 4.363}},   {38, {4.363, 4.538}},   {39, {4.538, 4.716}},   {40, {4.716, 4.889}},
        {41, {4.889, 5.191}},
        };
        
        ROOT::RVec<float> ieta;
        for (int i = 0; i < eta.size(); ++i) {
            if (eta.at(i) == 0)           ieta.push_back(1);
            else if (eta.at(i) == 5.191)  ieta.push_back(41);
            else {
                int Ieta = -1;
                int sign = copysign(1, eta.at(i));
                for (const auto &[key, value] : TowersEta) {
                    if ((abs(eta.at(i)) > value[0]) && (abs(eta.at(i)) <= value[1])) {
                        Ieta = key;
                        break;
                    }
                }
                ieta.push_back(sign*Ieta);
            }
        }
        return ieta;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> FindIphi(Vfloat phi) {

        map<int, std::vector<double>> TowersPhi;
        vector<double> x(73);
        for (int i = 0; i < 73; i++) {
            x[i] = i * 2 * M_PI / 72;
        }
        for (int i = 0; i < 72; i++) {
            TowersPhi[i+1].push_back(x[i]);
            TowersPhi[i+1].push_back(x[i+1]);
        }
        
        ROOT::RVec<float> iphi;
        for (int i = 0; i < phi.size(); ++i) {
            int p = phi.at(i);
            if (p < 0) p = p + 2 * M_PI;                        

            if (p == 0)               iphi.push_back(1);
            else if (p == 2 * M_PI)   iphi.push_back(72);
            else {
                int Iphi = -1;
                for (const auto &[key, value] : TowersPhi) {
                    if ((p > value[0]) && (p <= value[1])) {
                        Iphi = key;
                        break;
                    }
                }
                iphi.push_back(Iphi);
            }
        }
        return iphi;
    }

""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> SumHCAL (Vfloat TT_ihc, Vfloat TT_iet, Vfloat TT_ieta) {
        ROOT::RVec<float> TT_ihad;
        for (int i_TT = 0; i_TT < TT_ieta.size(); i_TT ++)
            if (abs(TT_ieta.at(i_TT)) < 29) {
                TT_ihad.push_back(TT_ihc.at(i_TT));
            }
            else {
                TT_ihad.push_back(TT_iet.at(i_TT));
            }
        return TT_ihad;
    }
""")

ROOT.gInterpreter.Declare("""
    int NextPhiTower(int iphi) {
        if (iphi == 72) return 1;
        else            return iphi + 1;
    }
    int PrevPhiTower(int iphi) {
        if (iphi == 1)  return 72;
        else            return iphi - 1;
    }
    int NextEtaTower(int ieta) {
        if (ieta == -1) return 1;
        else            return ieta + 1;
    }
    int PrevEtaTower(int ieta) {
        if (ieta == 1)  return -1;
        else            return ieta - 1;
    }
                        
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<ROOT::RVec<float>> ChunkyDonutEnergy (Vfloat L1_ieta, Vfloat L1_iphi, Vfloat TT_ieta, Vfloat TT_iphi, Vfloat TT_iem, Vfloat TT_ihad, Vfloat TT_iet) {

        ROOT::RVec<float> vec_iem_sum;
        ROOT::RVec<float> vec_ihad_sum;
        ROOT::RVec<float> vec_iet_sum;
        
        for (int i = 0; i < L1_ieta.size(); ++i) {
            int max_IEta = NextEtaTower(NextEtaTower(NextEtaTower(NextEtaTower(L1_ieta.at(i)))));
            int min_IEta = PrevEtaTower(PrevEtaTower(PrevEtaTower(PrevEtaTower(L1_ieta.at(i)))));
            int max_IPhi = NextPhiTower(NextPhiTower(NextPhiTower(NextPhiTower(L1_iphi.at(i)))));
            int min_IPhi = PrevPhiTower(PrevPhiTower(PrevPhiTower(PrevPhiTower(L1_iphi.at(i)))));
            
            float iem_sum = 0;
            float ihad_sum = 0;
            float iet_sum = 0;

            for (int i_TT = 0; i_TT < TT_ieta.size(); i_TT ++) {
                if (min_IPhi <= max_IPhi) {
                    if (((TT_ieta.at(i_TT) <= max_IEta) && (TT_ieta.at(i_TT) >= min_IEta)) && 
                        ((TT_iphi.at(i_TT) <= max_IPhi) && (TT_iphi.at(i_TT) >= min_IPhi))) {
                        iem_sum  += TT_iem.at(i_TT);
                        ihad_sum += TT_ihad.at(i_TT);
                        iet_sum  += TT_iet.at(i_TT); 
                    }
                } 
                else {
                    if (((TT_ieta.at(i_TT) <= max_IEta) && (TT_ieta.at(i_TT) >= min_IEta)) &&
                        ((TT_iphi.at(i_TT) >= min_IPhi) || (TT_iphi.at(i_TT) <= max_IPhi))) {
                        iem_sum  += TT_iem.at(i_TT);
                        ihad_sum += TT_ihad.at(i_TT);
                        iet_sum  += TT_iet.at(i_TT); 
                    }                        
                }                         
            }
            vec_iem_sum.push_back(iem_sum/2);
            vec_ihad_sum.push_back(ihad_sum/2);
            vec_iet_sum.push_back(iet_sum/2);
        }
        return {vec_iem_sum, vec_ihad_sum, vec_iet_sum};
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<ROOT::RVec<float>> CutOffline(Vfloat Offline_pt, Vfloat Offline_eta, Vfloat Offline_phi, 
            float cut_pt, float cut_eta, float cut_phi) {
        ROOT::RVec<float> Offline_pt_cut;
        ROOT::RVec<float> Offline_eta_cut;
        ROOT::RVec<float> Offline_phi_cut;
        for (int i_Of = 0; i_Of < Offline_pt.size(); i_Of ++) {
            if ((cut_pt  != -1) && (Offline_pt.at(i_Of) < cut_pt)) continue;
            if ((cut_eta != -1) && (abs(Offline_eta.at(i_Of)) > cut_eta)) continue;
            if ((cut_phi != -1) && (Offline_phi.at(i_Of) < cut_phi)) continue;
            Offline_pt_cut.push_back(Offline_pt.at(i_Of));
            Offline_eta_cut.push_back(Offline_eta.at(i_Of));
            Offline_phi_cut.push_back(Offline_phi.at(i_Of));
        }
        return {Offline_pt_cut, Offline_eta_cut, Offline_phi_cut};
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<ROOT::RVec<float>> CutBarrel(Vfloat Offline_pt, Vfloat Offline_eta, Vfloat Offline_phi, 
            float cut_pt, float cut_eta, float cut_phi) {
        ROOT::RVec<float> Offline_pt_cut;
        ROOT::RVec<float> Offline_eta_cut;
        ROOT::RVec<float> Offline_phi_cut;
        for (int i_Of = 0; i_Of < Offline_pt.size(); i_Of ++) {
            if ((cut_pt  != -1) && (Offline_pt.at(i_Of) < cut_pt)) continue;
            if ((cut_eta != -1) && (abs(Offline_eta.at(i_Of)) > cut_eta)) continue;
            if ((cut_phi != -1) && (Offline_phi.at(i_Of) < cut_phi)) continue;
            Offline_pt_cut.push_back(Offline_pt.at(i_Of));
            Offline_eta_cut.push_back(Offline_eta.at(i_Of));
            Offline_phi_cut.push_back(Offline_phi.at(i_Of));
        }
        return {Offline_pt_cut, Offline_eta_cut, Offline_phi_cut};
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<int> LeadingJets(Vfloat L1_pt, Vfloat L1_eta, Vfloat L1_phi, float etacut) {
        float leading_L1_pt = -1;
        float subleading_L1_pt = -1;
        int leading_L1_id = -1;
        int subleading_L1_id = -1;
        for (int i_L1 = 0; i_L1 < L1_pt.size(); i_L1 ++) {
            if (L1_eta.at(i_L1) > etacut) continue;
            if (L1_pt.at(i_L1) > leading_L1_pt) {
                leading_L1_id = i_L1;
                leading_L1_pt = L1_pt.at(i_L1);
            }
        }
        for (int i_L1 = 0; i_L1 < L1_pt.size(); i_L1 ++) {
            if (i_L1 == leading_L1_id) continue;
            if (L1_eta.at(i_L1) > etacut) continue;
            if (L1_pt.at(i_L1) > subleading_L1_pt) {
                subleading_L1_id = i_L1;
                subleading_L1_pt = L1_pt.at(i_L1);
            }
        }
        return {leading_L1_id, subleading_L1_id};

    }
""")

