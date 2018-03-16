cd ~/tensorflow/bin
import activate_this
import tensorflow as tf
import keras as k
cd /Users/Thomas/github/usd_cad_NN

import newest_data
import get_US_Bank
from get_data import *
from datautils import *
# from model_eval_funcs import *


Bonds, OilN, NetSp, FundsRates, Jobs=get_data()
Curr=get_curr()
Feed, Y, Ymag, Feed_pred=merge_all(Curr, Bonds, OilN, NetSp, FundsRates, Jobs, 200)
Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev= SplitData3SplitData3waysequential(Feed.values,Y)

Xtrain.shape
window=30
training_inputs=np.zeros([39,window,Xtrain.shape[1]-window])
training_inputs[0,:,0]
for i in range(Xtrain.shape[1]-window):
    training_inputs[:,:,i]=Xtrain[:,i:i+window]
