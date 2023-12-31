import matplotlib.pyplot as plt
import matplotlib

import mplhep
plt.style.use(mplhep.style.CMS)

def PlotTrainingTesting(x, y_train, y_test, loss_Name, outdir):
    cmap = matplotlib.cm.get_cmap('Set1')
    plt.plot(x, y_train, label='Training', lw=2, ls='-', marker='o', color=cmap(0))
    plt.plot(x, y_test, label='Testing', lw=2, ls='-', marker='o', color=cmap(1))
    plt.ylabel(loss_Name)
    plt.xlabel('Epoch')
    plt.grid()
    leg = plt.legend(loc='upper right', fontsize=20)
    leg._legend_box.align = "left"
    mplhep.cms.label('Preliminary', data=True, rlabel=r'')
    plt.savefig(outdir+'/'+loss_Name+'.pdf')
    plt.close()

def PlotAllLosses(x, y_reg, y_weight, y_rate, type, outdir):
   
    cmap = matplotlib.cm.get_cmap('Set1')
    plt.plot(x, y_reg, label='Regression loss', lw=2, ls='-', marker='o', color=cmap(0))
    plt.plot(x, y_weight, label='Weights loss', lw=2, ls='-', marker='o', color=cmap(1))
    plt.plot(x, y_rate, label='Rate loss', lw=2, ls='-', marker='o', color=cmap(2))
    plt.ylabel('Loss breakdown')
    plt.xlabel('Epoch')
    plt.grid()
    plt.yscale('log')
    leg = plt.legend(loc='upper right', fontsize=20)
    leg._legend_box.align = "left"
    mplhep.cms.label('Preliminary', data=True, rlabel=r'')
    plt.savefig(outdir+'/'+type+'Losses.pdf')
    plt.close() 

def makePlotsRegAndRate(HISTORY, outdir):

    PlotTrainingTesting(HISTORY['x'], HISTORY['train_RMSE'], HISTORY['test_RMSE'], 'RMSE', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_loss'], HISTORY['test_loss'], 'Loss', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_regressionLoss'], HISTORY['test_regressionLoss'], 'Regression', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_weightsLoss'], HISTORY['test_weightsLoss'], 'Weights', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_rateLoss'], HISTORY['test_rateLoss'], 'Rate', outdir)

    PlotAllLosses(HISTORY['x'], HISTORY['train_regressionLoss'], HISTORY['train_weightsLoss'], HISTORY['train_rateLoss'], 'train', outdir)
    PlotAllLosses(HISTORY['x'], HISTORY['test_regressionLoss'], HISTORY['test_weightsLoss'], HISTORY['test_rateLoss'], 'test', outdir)

def makePlotsReg(HISTORY, outdir):

    PlotTrainingTesting(HISTORY['x'], HISTORY['train_RMSE'], HISTORY['test_RMSE'], 'RMSE', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_loss'], HISTORY['test_loss'], 'Loss', outdir)
    PlotTrainingTesting(HISTORY['x'], HISTORY['train_regressionLoss'], HISTORY['test_regressionLoss'], 'Regression', outdir)
