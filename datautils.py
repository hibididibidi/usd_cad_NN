import pandas as pd
import numpy as np

def merge_all(Curr,Bonds,OilN,NetSp,FundsRates, Jobs, pred_days=100):
    Curr.columns=Curr.columns.get_level_values(0)
    OilN.columns=OilN.columns.get_level_values(0)
    Feedt=pd.merge(Bonds,OilN,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,FundsRates,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,Jobs,how='outer',left_index=True,right_index=True)
    Feedt['NetSp']=NetSp
    Feedt.fillna(method='pad',inplace=True)
    Feedt=pd.merge(Curr,Feedt,how='outer',left_index=True,right_index=True)
    Feed=Feedt.copy()
    Feed.dropna(inplace=True) #this will drop all current prices too if the data has not been updated
    Y=Feed['Result']
    Ymag=Feed['Gain']
    Feed.drop(['Result','Gain'],axis=1, inplace=True)
    Feed=Feed.T
    Feedt.drop(['Result','Gain'],axis=1, inplace=True)
    Feedt.dropna(axis=0,inplace=True)
    Feedt=Feedt.T
    Y=Y.values.reshape(1,Feed.shape[1])
    Ymag=Ymag.values.reshape(1,Feed.shape[1])
    return Feed, Y, Ymag, Feedt.iloc[:,-pred_days:] #Defaulting using last 100 full examples as predictor input, can be adjusted later

def SplitData3way(X,Y,percent_train=90):
    #First cut out the recent test and dev sets: all values in training set are prior to values in the test and dev
    ntrain=int(percent_train/100*X.shape[1])
    Permuttrain=list(np.random.permutation(ntrain))
    Xtrain=np.float32(X[:,Permuttrain])
    Ytrain=np.float32(Y[:,Permuttrain])
    m=X.shape[1]
#     X=(X-X.mean(axis=1).reshape(-1,1))/X.std(axis=1).reshape(-1,1) ###### Batch normalization did not seem to have any effect
    Permuttestdev= list(np.random.permutation(m-ntrain)+ntrain)
#     print(Permuttestdev)
    ntest=len(Permuttestdev)//2
#     print(ntest)
    Permuttest=Permuttestdev[:ntest]
    Permutdev=Permuttestdev[ntest:]
    Xtest=np.float32(X[:,Permuttest])
    Ytest=np.float32(Y[:,Permuttest])
    Xdev=np.float32(X[:,Permutdev])
    Ydev=np.float32(Y[:,Permutdev])
#     print(Xtrain, Ytrain, Xtest, Ytest, Xdev)
    return Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev

def merge_all_DB(Curr,Bonds,OilN,NetSp,FundsRates, Jobs, pred_days=100):
    Curr.columns=Curr.columns.get_level_values(0)
    OilN.columns=OilN.columns.get_level_values(0)
    Feedt=pd.merge(Bonds,OilN,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,FundsRates,how='outer',left_index=True,right_index=True)
    Feedt=pd.merge(Feedt,Jobs,how='outer',left_index=True,right_index=True)
    Feedt['NetSp']=NetSp
    Feedt.fillna(method='pad',inplace=True)
    Feedt=pd.merge(Curr,Feedt,how='outer',left_index=True,right_index=True)
    Feed=Feedt.copy()
    Feed.dropna(inplace=True) #this will drop all current prices too if the data has not been updated
    return Feed

def SplitData3waysequential(X,Y,percent_train=90, percent_dev=5):
    #First cut out the recent test and dev sets: all values in training set are prior to values in the test and dev
    ntrain=int(percent_train/100*X.shape[1])
    Xtrain=np.float32(X[:,:ntrain])
    Ytrain=np.float32(Y[:,:ntrain])
    m=X.shape[1]
#     X=(X-X.mean(axis=1).reshape(-1,1))/X.std(axis=1).reshape(-1,1) ###### Batch normalization did not seem to have any effect

    ntest=int((percent_dev+percent_train)/100*X.shape[1])
    Xtest=np.float32(X[:,ntrain:ntest])
    Ytest=np.float32(Y[:,ntrain:ntest])
    Xdev=np.float32(X[:,ntest:])
    Ydev=np.float32(Y[:,ntest:])
#     print(Xtrain, Ytrain, Xtest, Ytest, Xdev)
    return Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev
