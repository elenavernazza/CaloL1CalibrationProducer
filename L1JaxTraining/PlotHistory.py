import os, glob, imageio
import matplotlib.pyplot as plt
import numpy as np
from SFPlots import PlotSF, PlotSF2D

from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(image, text, position=(1, 1), font_size=30, text_color=(0, 0, 0)):
    # Convert the image to RGB mode if it's in a different mode (e.g., RGBA)
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/abattis-cantarell/Cantarell-Regular.otf", font_size)
    draw.text(position, text, fill=text_color, font=font)
    return image

def AddText(plot_list):
    plot_list_counter = []
    for i, plot in enumerate(plot_list):
        image = Image.open(plot)
        iterator_text = "Epoch {}".format(i)
        image_with_overlay = add_text_overlay(image, iterator_text)
        image_with_overlay.save(plot)
        plot_list_counter.append(image_with_overlay)

def PlotLoss(TrainLoss, TestLoss, TrainResp, TestResp, odirLoss, i):
    
    TrainLoss = np.load(TrainLoss)['arr_0']
    TestLoss = np.load(TestLoss)['arr_0']
    bins = np.linspace(0,15,31)
    fig, axs = plt.subplots(2, 1, figsize=(12,12))
    axs[0].hist(TrainLoss, color='red', linewidth=2, histtype='step', label='Train: Mean = {:.3f}'.format(np.mean(TrainLoss)), bins=bins, density=True)
    axs[0].hist(TestLoss, color='blue', linewidth=2, histtype='step', label='Test: Mean = {:.3f}'.format(np.mean(TestLoss)), bins=bins, density=True)
    axs[0].set_ylabel('A.U.')
    axs[0].set_xlabel('Loss')
    axs[0].set_yscale('log')
    axs[0].legend()

    TrainResp = np.load(TrainResp)['arr_0']
    TestResp = np.load(TestResp)['arr_0']
    bins = np.linspace(0,5,51)
    axs[1].hist(TrainResp, color='red', linewidth=2, histtype='step', label='Train: Std = {:.3f}'.format(np.std(TrainResp)), bins=bins, density=True)
    axs[1].hist(TestResp, color='blue', linewidth=2, histtype='step', label='Test: Std = {:.3f}'.format(np.std(TestResp)), bins=bins, density=True)
    axs[1].set_ylabel('A.U.')
    axs[1].set_xlabel('Response')
    axs[1].legend()

    savefile = odirLoss + '/Loss_{}'.format(i)
    plt.savefig(savefile+'.png')
    plt.savefig(savefile+'.pdf')
    print(savefile)

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--indir",    dest="indir",   help="Input folder with trained model",     default=None)
    parser.add_option("--tag",      dest="tag",     help="tag of the training folder",          default="")
    parser.add_option("--out",      dest="odir",    help="Output folder",                       default=None)
    parser.add_option("--v",        dest="v",       help="Ntuple type ('ECAL' or 'HCAL')",      default='HCAL')
    parser.add_option("--perf",     dest="perf",    help="Performance history",                 default=False, action='store_true')
    parser.add_option("--loss",     dest="loss",    help="Loss history",                        default=False, action='store_true')
    (options, args) = parser.parse_args()
    print(options)

    indir = options.indir
    odirSFs = indir+'/History/SFs'
    os.system("mkdir -p {}".format(odirSFs))
    if options.loss:
        odirLoss = indir+'/History/Loss'
        os.system("mkdir -p {}".format(odirLoss))
    if options.perf:
        odirPerf = indir+'/History/Performance'
        os.system("mkdir -p {}".format(odirPerf))

    SFsHistory = glob.glob(indir + '/History/ScaleFactors_*')
    for i, SF_filename in enumerate(SFsHistory):
        print(" ### Reading {} --> {}".format(i, SF_filename))
        if options.v == "ECAL": cols = 28
        if options.v == "HCAL": cols = 40
        ScaleFactors = np.loadtxt(open(SF_filename, "rb"), delimiter=',', usecols=range(0,cols))
        eta_binning = np.arange(1,cols+1)

        # Definition of energy bin edges from the header
        with open(SF_filename) as f:
            header = f.readline().rstrip()
        header = header.split("[")[1].split("]")[0]
        et_binning = header.split(',')[:-1]
        et_binning = [float(i) for i in et_binning]
    
        PlotSF(ScaleFactors, et_binning, odirSFs, options.v, eta_binning, i_epoch=i)

        et_binning = header.split(',')
        et_binning = [float(i) for i in et_binning]
        PlotSF2D(ScaleFactors, odirSFs, et_binning, eta_binning, options.v, i_epoch=i)

        if options.loss:
            TrainLoss = indir+'/History/TrainLoss_{}.npz'.format(i)
            TestLoss = indir+'/History/TestLoss_{}.npz'.format(i)
            TrainResp = indir+'/History/TrainResp_{}.npz'.format(i)
            TestResp = indir+'/History/TestResp_{}.npz'.format(i)
            PlotLoss(TrainLoss, TestLoss, TrainResp, TestResp, odirLoss, i)

        if options.perf:
            caloname = "/History/caloParams_2023_JAX{}_{}_newCalib_cfi".format(indir, i)
            cmd = "python3 ProduceCaloParams.py --name {}" \
                " --HCAL {}".format(caloname, SF_filename)
            print(cmd)
            os.system(cmd)

            cmd = "python3 RDF_ResolutionFast.py --indir JetMET__Run2022G-PromptReco-v1__Run362617__AOD__GT130XdataRun3Promptv3_CaloParams2023v02_noL1Calib_data_reco_json/GoodNtuples" \
                " --reco --target jet --raw --PuppiJet --jetPtcut 30 --etacut 3 --nEvts 100000 --no_plot" \
                " --HCALcalib --caloParam {}.py --outdir {} --tag {}".format(caloname, odirPerf, i)
            print(cmd)
            os.system(cmd)

            cmd = "python3 comparisonPlotsFast.py --indir {} --target jet --reco" \
                " --old 0/NtuplesVold --unc 0/NtuplesVunc --doRate False --doTurnOn False --tag {}".format(odirPerf, i)
            print(cmd)
            os.system(cmd)

    plot_list = glob.glob(odirSFs + '/Calib_vs_Eta_HCAL*.png')
    AddText(plot_list)
    plot_map = list(map(lambda plot: imageio.imread(plot), plot_list))
    imageio.v2.mimsave(indir+'/History/Calib_vs_Eta_HCAL.gif', plot_map, format='GIF', duration=500)

    plot_list = glob.glob(odirSFs + '/SFs_2D_HCAL*.png')
    AddText(plot_list)
    plot_map = list(map(lambda plot: imageio.imread(plot), plot_list))
    imageio.v2.mimsave(indir+'/History/SFs_2D_HCAL.gif', plot_map, format='GIF', duration=500)

    if options.loss:
        plot_list = glob.glob(odirLoss + '/Loss*.png')
        AddText(plot_list)
        plot_map = list(map(lambda plot: imageio.imread(plot), plot_list))
        imageio.v2.mimsave(indir+'/History/Loss.gif', plot_map, format='GIF', duration=500)

    if options.perf:
        plot_list = glob.glob(odirPerf + '/PerformancePlots*/PNGs/comparisons__jet/response_inclusive_res__jet.png')
        AddText(plot_list)
        plot_map = list(map(lambda plot: imageio.imread(plot), plot_list))
        imageio.v2.mimsave(indir+'/History/response_inclusive.gif', plot_map, format='GIF', duration=500)

