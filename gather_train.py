import numpy as np
import pandas as pd
import quandl
# import tensorflow as tf
#cd /Users/Thomas/github/usd_cad_NN/

import requests
from get_data import *
# cd C:\Users\thoma\github\usd_cad_NN/
# %matplotlib inline
from datautils import *
from model_eval_funcs import *


Bonds, OilN, NetSp, FundsRates, Jobs=get_data()
Curr=get_curr()
Feed, Y, Ymag, Feed_pred=merge_all(Curr, Bonds, OilN, NetSp, FundsRates, Jobs, 200)
Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev= SplitData3way(Feed.values,Y)
print('inputs are:',Feed.iloc[:,-1])
ask=input('run train_model with default parameters? y/n ')
if ask == 'y':
    best_params=train_model(Bonds,OilN,NetSp,FundsRates, Jobs, days=[10],shapes=[13], probs=[.95])
