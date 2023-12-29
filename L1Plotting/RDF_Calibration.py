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

    vector<float> read_ETBins (const char *filename, string ETstring) {
        vector<float> layer1HCalScaleETBins;
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
                        layer1HCalScaleETBins.push_back(convert(value));
                        line.erase(0, line.find(",") + 1);
                    }
                    layer1HCalScaleETBins.push_back(convert(line));
                    break;
                }
            }
            file.close();
        }
        return layer1HCalScaleETBins;
    }

""")

ROOT.gInterpreter.Declare("""

    static TH2D* HCAL_SFmap;

    void load_HCAL_SFs (const char *filename) {
        string ETstring = "layer1HCalScaleETBins";
        string SFstring = "layer1ECalScaleFactors";
        vector<float> layer1HCalScaleETBins = read_ETBins (filename, ETstring);
        vector<vector<float>> layer1HCalScaleFactors = read_SFs (filename, SFstring);

        int rows = layer1HCalScaleFactors.size();
        int cols = layer1HCalScaleFactors[0].size();
   
        HCAL_SFmap = new TH2D("layer1HCalScaleFactors", "layer1HCalScaleFactors", rows, -0.5, rows-0.5, cols, layer1HCalScaleETBins.front(), layer1HCalScaleETBins.back());
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                HCAL_SFmap->SetBinContent(i+1, j+1, layer1HCalScaleFactors[i][j]);
            }
        }
     
        TFile* f = new TFile("/data_CMS/cms/vernazza/L1TCalibration/CMSSW_13_1_0_pre4_Fix/CMSSW_13_1_0_pre4/src/CaloL1CalibrationProducer/L1Plotting/HCAL_SFmap.root","RECREATE");
        HCAL_SFmap->Write();
        f->Close();
    }
""")

ROOT.gInterpreter.Declare("""
    using Vfloat = const ROOT::RVec<float>&;
    ROOT::RVec<float> CalibrateIhad (Vfloat TT_ihad, Vfloat TT_ieta) {
        ROOT::RVec<float> TT_ihad_calib;
        for (int i_TT = 0; i_TT < TT_ieta.size(); i_TT ++) {
            float SF = HCAL_SFmap->GetBinContent(HCAL_SFmap->FindBin(TT_ieta.at(i_TT), TT_ihad.at(i_TT)));
            TT_ihad_calib.push_back(TT_ihad.at(i_TT)*SF);
        }
        return TT_ihad_calib;
    }
""")

