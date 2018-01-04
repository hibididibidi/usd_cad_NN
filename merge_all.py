def merge_all(Curr=Curr,Bonds=Bonds,OilN=OilN,NetSp=NetSp,FundsRates=FundsRates, Jobs=Jobs, curtestex=1):

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
    return Feed, Y, Ymag, Feedt.iloc[:,-curtestex:] #Defaulting using last 220 full examples as predictor input, can be adjusted later

