import ROOT

ROOT.gInterpreter.Declare("""
    float convert (string a) {
        try { return stod(a); }
        catch (std::exception& e) { return 0; }
    }
""")

ROOT.gInterpreter.Declare("""
    vector<vector<float>> read_SFs (const char *filename, string SFstring) {
        vector<vector<float>> layer1HCalScaleFactors;
        ifstream file(filename);
        while (file.is_open()) {
            string line;
            while (getline(file, line)) {
                if (line.find(SFstring) != string::npos) {
                    // skip the next line that contains the opening bracket
                    getline(file, line);
                    while (line.find("]") == string::npos) {
                        vector<float> row;
                        line.erase(0, line.find_first_not_of(" ,"));
                        line.erase(line.find_last_not_of(" ,") + 1);
                        string value;
                            while (line.find(",") != string::npos) {
                                value = line.substr(0, line.find(","));
                                row.push_back(convert(value));
                                line.erase(0, line.find(",") + 1);
                            }
                        row.push_back(convert(line));
                        layer1HCalScaleFactors.push_back(row);
                        getline(file, line);
                    }
                }
            }
            file.close();
        }
        return layer1HCalScaleFactors;
    }

    vector<double> read_ETBins (const char *filename, string ETstring) {
        vector<double> layer1ScaleETBins;
        layer1ScaleETBins.push_back((double)0.);
        ifstream file(filename);
        while (file.is_open()) {
            string line;
            while (getline(file, line)) {
                if (line.find(ETstring) != string::npos) {
                    // skip the next line that contains the opening bracket
                    line.erase(0, line.find("([") + 2);
                    line.erase(line.find("])"));
                    string value;
                    while (line.find(",") != string::npos) {
                        value = line.substr(0, line.find(","));
                        layer1ScaleETBins.push_back((double)convert(value)*2.); // from GeV to iEt
                        line.erase(0, line.find(",") + 1);
                    }
                    layer1ScaleETBins.push_back((double)convert(line)*2.); // from GeV to iEt
                    break;
                }
            }
            file.close();
        }
        return layer1ScaleETBins;
    }

""")

# [FIXME] remove HF if calibration is ok
# [FIXME] save map in aoutput folder
ROOT.gInterpreter.Declare("""

    static TH2D* HCAL_SFmap;

    void load_HCAL_SFs (const char *filename, const char *output) {
        string ETstring_HCAL = "layer1HCalScaleETBins";
        string SFstring_HCAL = "layer1HCalScaleFactors";
        vector<double> layer1ScaleETBins_HCAL = read_ETBins (filename, ETstring_HCAL);
        vector<vector<float>> layer1ScaleFactors_HCAL = read_SFs (filename, SFstring_HCAL);

        string ETstring_HF = "layer1HFScaleETBins";
        string SFstring_HF = "layer1HFScaleFactors";
        vector<double> layer1ScaleETBins_HF = read_ETBins (filename, ETstring_HF);
        vector<vector<float>> layer1ScaleFactors_HF = read_SFs (filename, SFstring_HF);
                          
        int rows = layer1ScaleFactors_HCAL[0].size(); // eta
        int cols = layer1ScaleFactors_HCAL.size();
        const Double_t *ybins = layer1ScaleETBins_HCAL.data();
        
        // cout << "Ybins" << endl;
        // for (int i = 0; i < layer1ScaleETBins_HCAL.size(); i++) cout << ybins[i] << " ";
        // cout << endl;
                          
        HCAL_SFmap = new TH2D("HCAL_SFmap", "HCAL_SFmap", rows, 0.5, rows+0.5, cols, ybins);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                HCAL_SFmap->SetBinContent(i+1, j+1, layer1ScaleFactors_HCAL[j][i]);
            }
        }

        HCAL_SFmap->GetXaxis()->SetTitle("i#eta");
        HCAL_SFmap->GetYaxis()->SetTitle("iEt [0.5 GeV]");
        cout << "Saving to " << Form("%s/SFmap_HCAL.root", output) << endl;
        TFile* f = new TFile(Form("%s/SFmap_HCAL.root", output),"RECREATE");
        HCAL_SFmap->Write();
        f->Close();
                          
        TCanvas* c1 = new TCanvas("c1","c1",800,800);
        HCAL_SFmap->SetTitle("");
        HCAL_SFmap->Draw("COLZ");
        HCAL_SFmap->GetZaxis()->SetRangeUser(0., 2.);
        c1->SetLeftMargin(0.11);
        c1->SetRightMargin(0.14);
        c1->SaveAs(Form("%s/SFmap_HCAL.png", output));
        c1->SaveAs(Form("%s/SFmap_HCAL.pdf", output));
        c1->Close();
    }
""")

ROOT.gInterpreter.Declare("""

    static TH2D* HF_SFmap;

    void load_HF_SFs (const char *filename, const char *output) {
        string ETstring = "layer1HFScaleETBins";
        string SFstring = "layer1HFScaleFactors";
        vector<double> layer1ScaleETBins = read_ETBins (filename, ETstring);
        vector<vector<float>> layer1ScaleFactors = read_SFs (filename, SFstring);

        int rows = layer1ScaleFactors[0].size(); // x-axis = [1,12] = ieta
        int cols = layer1ScaleFactors.size();    // y-axis = [0,256] = energy
        const Double_t *ybins = layer1ScaleETBins.data();
   
        HF_SFmap = new TH2D("HF_SFmap", "HF_SFmap", rows, 0.5, rows+0.5, cols, ybins);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                HF_SFmap->SetBinContent(i+1, j+1, layer1ScaleFactors[j][i]);
            }
        }

        HF_SFmap->GetXaxis()->SetTitle("i#eta");
        HF_SFmap->GetYaxis()->SetTitle("iEt [0.5 GeV]");    
        cout << "Saving to " << Form("%s/SFmap_HF.root", output) << endl;
        TFile* f = new TFile(Form("%s/SFmap_HF.root", output),"RECREATE");
        HF_SFmap->Write();
        f->Close();
        
        TCanvas* c1 = new TCanvas("c1","c1",800,800);
        HF_SFmap->SetTitle("");
        HF_SFmap->Draw("COLZ");
        HF_SFmap->GetZaxis()->SetRangeUser(0., 2.);
        c1->SetLeftMargin(0.11);
        c1->SetRightMargin(0.14);
        c1->SaveAs(Form("%s/SFmap_HF.png", output));
        c1->SaveAs(Form("%s/SFmap_HF.pdf", output));
        c1->Close();
    }
""")

ROOT.gInterpreter.Declare("""

    static TH2D* ECAL_SFmap;

    void load_ECAL_SFs (const char *filename, const char *output) {
        string ETstring = "layer1ECalScaleETBins";
        string SFstring = "layer1ECalScaleFactors";
        vector<double> layer1ScaleETBins = read_ETBins (filename, ETstring);
        vector<vector<float>> layer1ScaleFactors = read_SFs (filename, SFstring);

        int rows = layer1ScaleFactors[0].size(); // x-axis = [1,28] = ieta
        int cols = layer1ScaleFactors.size();    // y-axis = [0,256] = energy
        const Double_t *ybins = layer1ScaleETBins.data();
  
        ECAL_SFmap = new TH2D("ECAL_SFmap", "ECAL_SFmap", rows, 0.5, rows+0.5, cols, ybins);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                ECAL_SFmap->SetBinContent(i+1, j+1, layer1ScaleFactors[j][i]);
            }
        }

        ECAL_SFmap->GetXaxis()->SetTitle("i#eta");
        ECAL_SFmap->GetYaxis()->SetTitle("iEt [0.5 GeV]"); 
        cout << "Saving to " << Form("%s/SFmap_ECAL.root", output) << endl;
        TFile* f = new TFile(Form("%s/SFmap_ECAL.root", output),"RECREATE");
        ECAL_SFmap->Write();
        f->Close();
        
        TCanvas* c1 = new TCanvas("c1","c1",800,800);
        ECAL_SFmap->SetTitle("");
        ECAL_SFmap->Draw("COLZ");
        ECAL_SFmap->GetZaxis()->SetRangeUser(0., 2.);
        c1->SetLeftMargin(0.11);
        c1->SetRightMargin(0.14);
        c1->SaveAs(Form("%s/SFmap_ECAL.png", output));
        c1->SaveAs(Form("%s/SFmap_ECAL.pdf", output));
        c1->Close();
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<int> CalibrateIhad (Vfloat TT_ieta, Vfloat TT_ihad, bool apply) {
        ROOT::RVec<float> TT_ihad_calib;
        for (int i_TT = 0; i_TT < TT_ihad.size(); i_TT ++) {
            if (apply) {
                float SF = 0;
                if (abs(TT_ieta.at(i_TT)) < 29) {
                    SF = HCAL_SFmap->GetBinContent(HCAL_SFmap->FindBin(abs(TT_ieta.at(i_TT)), TT_ihad.at(i_TT)));
                }
                else {
                    SF = HF_SFmap->GetBinContent(HF_SFmap->FindBin(abs(TT_ieta.at(i_TT))-29, TT_ihad.at(i_TT)));
                }
                TT_ihad_calib.push_back((int) (TT_ihad.at(i_TT)*SF));
                // cout << TT_ihad.at(i_TT) << " " << TT_ieta.at(i_TT) << " " << SF << " " << (int) (TT_ihad.at(i_TT)*SF) << endl;
            }
            else {
                TT_ihad_calib.push_back(TT_ihad.at(i_TT));
            }
        }
        return TT_ihad_calib;
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> CalibrateIem (Vfloat TT_ieta, Vfloat TT_iem, bool apply) {
        ROOT::RVec<float> TT_iem_calib;
        for (int i_TT = 0; i_TT < TT_iem.size(); i_TT ++) {
            if (apply) {
                float SF = ECAL_SFmap->GetBinContent(ECAL_SFmap->FindBin(abs(TT_ieta.at(i_TT)), TT_iem.at(i_TT)));
                TT_iem_calib.push_back((int) (TT_iem.at(i_TT)*SF));
            }
            else {
                TT_iem_calib.push_back(TT_iem.at(i_TT));
            }
        }
        return TT_iem_calib;
    }
""")

ROOT.gInterpreter.Declare("""
    float TestCalibrateIem (float TT_ieta, float TT_iem) {
        float TT_iem_calib;
        cout << "Bin x = " << ECAL_SFmap->GetXaxis()->FindBin(abs(TT_ieta)) << endl;
        cout << "Bin y = " << ECAL_SFmap->GetYaxis()->FindBin(TT_iem) << endl;
        float SF = ECAL_SFmap->GetBinContent(ECAL_SFmap->FindBin(abs(TT_ieta), TT_iem));
        TT_iem_calib = (int) (TT_iem*SF);
        cout << SF << endl;
        return TT_iem_calib;
    }
""")

ROOT.gInterpreter.Declare("""
    float TestCalibrateIhad (float TT_ieta, float TT_ihad) {
        float TT_ihad_calib;
        cout << "Bin x = " << HCAL_SFmap->GetXaxis()->FindBin(abs(TT_ieta)) << endl;
        cout << "Bin y = " << HCAL_SFmap->GetYaxis()->FindBin(TT_ihad) << endl;
        float SF = HCAL_SFmap->GetBinContent(HCAL_SFmap->FindBin(abs(TT_ieta), TT_ihad));
        TT_ihad_calib = (int) (TT_ihad*SF);
        cout << SF << endl;
        return TT_ihad_calib;
    }
""")
