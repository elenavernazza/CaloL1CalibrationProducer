#librairies utiles
import numpy as np
from math import *
from itertools import product
import copy
import pandas as pd

import tensorflow as tf
from tensorflow import keras
import sklearn
# Regression import
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from tensorflow.keras.constraints import max_norm
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

inputs = keras.Input(shape = (81,41), name = 'chunky_donut')

enc = OneHotEncoder()
values = [[i%41 + 1, i] if (i%41 + 1 != 29) else [28,i] for i in range(513)]
enc.fit(values)

#OH = keras.layers.Lambda(lambda x : enc.transform(x).toarray(), name='one_hot_encoder')

#inputs = OH(inputs)
layer1 = Dense(164,input_dim=41, activation = 'softplus', name = 'NN1', kernel_initializer='normal',bias_initializer='zeros', bias_constraint = max_norm(0.))
cache = Dense(512, name = 'cache', activation = 'softplus', kernel_initializer='normal',bias_initializer='zeros', bias_constraint = max_norm(0.))
layer2 = Dense(1, name = 'NN2',activation = 'softplus',kernel_initializer='normal',bias_initializer='zeros', bias_constraint = max_norm(0.))

#layer1 = Dense(128, input_dim=2, activation='softplus', name = 'NN1', kernel_initializer='normal',bias_initializer='zeros')
#layer2 = Dense(1, activation='softplus', name = 'NN2',kernel_initializer='normal',bias_initializer='zeros')


couche = Sequential()
couche.add(layer1)
couche.add(cache)
#couche.add(Dense(256, activation = 'relu', name = 'cache_2',kernel_initializer='ones',bias_initializer='zeros'))
couche.add(layer2)
#le reseau de neurone partagé par tous (inputs_dim = 2)

separation_l = []
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,0,:],name=f"tour_{0}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,1,:],name=f"tour_{1}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,2,:],name=f"tour_{2}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,3,:],name=f"tour_{3}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,4,:],name=f"tour_{4}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,5,:],name=f"tour_{5}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,6,:],name=f"tour_{6}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,7,:],name=f"tour_{7}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,8,:],name=f"tour_{8}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,9,:],name=f"tour_{9}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,10,:],name=f"tour_{10}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,11,:],name=f"tour_{11}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,12,:],name=f"tour_{12}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,13,:],name=f"tour_{13}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,14,:],name=f"tour_{14}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,15,:],name=f"tour_{15}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,16,:],name=f"tour_{16}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,17,:],name=f"tour_{17}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,18,:],name=f"tour_{18}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,19,:],name=f"tour_{19}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,20,:],name=f"tour_{20}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,21,:],name=f"tour_{21}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,22,:],name=f"tour_{22}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,23,:],name=f"tour_{23}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,24,:],name=f"tour_{24}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,25,:],name=f"tour_{25}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,26,:],name=f"tour_{26}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,27,:],name=f"tour_{27}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,28,:],name=f"tour_{28}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,29,:],name=f"tour_{29}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,30,:],name=f"tour_{30}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,31,:],name=f"tour_{31}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,32,:],name=f"tour_{32}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,33,:],name=f"tour_{33}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,34,:],name=f"tour_{34}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,35,:],name=f"tour_{35}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,36,:],name=f"tour_{36}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,37,:],name=f"tour_{37}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,38,:],name=f"tour_{38}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,39,:],name=f"tour_{39}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,40,:],name=f"tour_{40}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,41,:],name=f"tour_{41}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,42,:],name=f"tour_{42}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,43,:],name=f"tour_{43}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,44,:],name=f"tour_{44}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,45,:],name=f"tour_{45}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,46,:],name=f"tour_{46}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,47,:],name=f"tour_{47}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,48,:],name=f"tour_{48}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,49,:],name=f"tour_{49}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,50,:],name=f"tour_{50}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,51,:],name=f"tour_{51}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,52,:],name=f"tour_{52}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,53,:],name=f"tour_{53}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,54,:],name=f"tour_{54}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,55,:],name=f"tour_{55}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,56,:],name=f"tour_{56}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,57,:],name=f"tour_{57}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,58,:],name=f"tour_{58}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,59,:],name=f"tour_{59}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,60,:],name=f"tour_{60}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,61,:],name=f"tour_{61}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,62,:],name=f"tour_{62}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,63,:],name=f"tour_{63}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,64,:],name=f"tour_{64}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,65,:],name=f"tour_{65}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,66,:],name=f"tour_{66}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,67,:],name=f"tour_{67}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,68,:],name=f"tour_{68}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,69,:],name=f"tour_{69}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,70,:],name=f"tour_{70}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,71,:],name=f"tour_{71}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,72,:],name=f"tour_{72}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,73,:],name=f"tour_{73}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,74,:],name=f"tour_{74}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,75,:],name=f"tour_{75}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,76,:],name=f"tour_{76}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,77,:],name=f"tour_{77}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,78,:],name=f"tour_{78}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,79,:],name=f"tour_{79}")(inputs)))
separation_l.append(couche(keras.layers.Lambda(lambda x : x[:,80,:],name=f"tour_{80}")(inputs)))

outputs = keras.layers.Add()(separation_l)
model1 = keras.Model(inputs, outputs, name = 'CMS')
#model1.summary()
#keras.utils.plot_model(model1, "model1.png")

def custom_loss(y_true, y_pred):
    return tf.nn.l2_loss((y_true - y_pred)/(y_true+0.1))

model1.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=custom_loss)

if __name__ == "__main__" :

    df = pd.read_csv('/data_CMS/cms/motta/CaloL1calibraton/2022_04_02_NtuplesV0/hdf5dataframes/test.csv')
    df = df[['ev','i_eta','i_em','i_had','i_et']]
    df.set_index('ev',inplace=True)
    df_e = df[['i_eta','i_em']]

    dfjetPt = pd.read_csv('/data_CMS/cms/motta/CaloL1calibraton/2022_04_02_NtuplesV0/hdf5dataframes/testPt.csv')
    dfjetPt = dfjetPt[['ev','jetPt']]
    dfjetPt.set_index('ev', inplace=True)
    
    print('Step 1')

    df_dummies = pd.get_dummies(df_e, columns=['i_eta'])
    for i in range(35,42):
        df_dummies['i_eta_'+str(i)] = 0

    X = np.array([df_dummies.loc[i].to_numpy() for i in df.index.drop_duplicates(keep='first')])
    Y = np.array([dfjetPt.loc[i].array[0] for i in dfjetPt.index])

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    model1.fit(X_train, Y_train, epochs=20, batch_size=128,verbose=1)

    print('Step 2')

    model1 = keras.models.load_model("lr_0.001_n1_164_n2_512_15ep__bs_128_me_3.0/model/saved_model.pb", compile=False)

    print('Step 3')