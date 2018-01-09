import numpy as np
import pandas as pd
import quandl
# import tensorflow as tf
import requests
from get_data import *
# cd C:\Users\thoma\github\usd_cad_NN/
# %matplotlib inline
from datautils import *
from get_data import *
from model_eval_funcs import *


Bonds, OilN, NetSp, FundsRates, Jobs=get_data()
Curr=get_curr()
Feed, Y, Ymag, Feedt=merge_all(Curr, Bonds, OilN, NetSp, FundsRates, Jobs)
Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev= SplitData3way(Feed.values,Y)

print('inputs are:',Feed.iloc[:,-5:])
