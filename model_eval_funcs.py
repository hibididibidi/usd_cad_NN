#predictor
from gather_train import *
from tensor_model_funcs import *
import _pickle as pickle

def Pred(X,parameters):
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
#     W3 = parameters['W3']
#     b3 = parameters['b3']

    Z1=tf.matmul(W1,X)+b1
    A1=tf.nn.relu(Z1)
    Z2=tf.matmul(W2,A1)+b2 #could use A1_drop
#     A2=tf.nn.relu(Z2)
#     Z3=tf.matmul(W3,A2)+b3
    sess=tf.Session()
    return (sess.run(tf.sigmoid(Z2)))

def tester_table(Feed_pred,Yhat):
    Test=Feed_pred.iloc[0].T
    Yhat.shape
    Yhat1=Yhat.reshape(-1)
    Z=pd.DataFrame(Yhat1, index=Feed_pred.columns.values)
    Z['current']=Test
    Z.columns=[['Probability','Current']]
    return Z

def train_model(Bonds,OilN,NetSp,FundsRates, Jobs, days=[10,15],shapes=[10, 13], probs=[0.8,0.9]):
  # Testing using test/dev sets from the most recent data and all other data for training set
  testtime=str(pd.Timestamp.now().day)+'_'+str(pd.Timestamp.now().hour)+'_'+str(pd.Timestamp.now().minute)
  testtimestr='test_results'+str(testtime)+'.txt'
  bestparamtime='best_params'+str(testtime)+'.txt'
  file=open(testtimestr,'w')
  file.write('Test Accuracy, Training Accuracy, days ahead, hidden units, keep prob1, keep prob2')
  file.close()
  test_results =[]
  test_accuracy=0.4
  for i in days:
      Curr= get_curr(i)
      Feed, Y, _,_=merge_all(Curr,Bonds,OilN,NetSp,FundsRates, Jobs)
      Xtrain,Ytrain,Xtest,Ytest,Xdev,Ydev=SplitData3way(Feed.values,Y)
      for k in shapes:
          for l in probs:
              for m in probs:
                  parameters,Acc,Train=model_n(Xtrain,Ytrain,Xdev,Ydev, num_epochs=10001, layers=[Xtrain.shape[0], k, 1], learning_rate=0.001, keepprob1=l, keepprob2=m)
                  print(i,'days ahead,', l, 'prob1,', m, 'prob2')
                  test_results.append((Acc,Train))
                  file=open(testtimestr,'a')
                  file.write('\n'+str(Acc)+','+str(Train)+','+str(i)+','+str(k)+','+str(l)+','+str(m))
                  file.close()
                  if Acc>test_accuracy and Acc<Train:
                      test_accuracy=Acc
                      best_params=parameters
                      Day_Un_P1_P2=[i,k,l,m]
  with open(bestparamtime, "wb") as myFile:
    pickle.dump(best_params, myFile)
  print('test results',test_results)
  return(best_params)

def view_top_results(filename):
    test_results=pd.read_csv(filename)
    test_results=test_results.sort_values(['Test Accuracy'], ascending=False)
    return test_results.head(10)

def evaluate_predictor(TT, thresh=0.3):
    TT['Position']=0
    TT=TT[TT>0]
    TT['Position']=np.where(TT['Probability']>(1-thresh), 1,np.where(TT['Probability']<thresh,0,TT['Position']))
    TT.fillna(method='pad',inplace=True,axis=0)# Fill to hold position, 1 means long USD 0 means long CAD
    #     print(TT.dropna(axis=1))
    #     print(TT.iloc[180:])

    # Make summary table--->arrays of days/rates conversion
    TT1=TT['Position'].where(TT['Position']!=TT['Position'].shift()).copy()
    TT1.dropna(axis=0,inplace=True)
    TT1=TT.loc[TT1.index.values]
    startpos=TT1['Position'].values
    conversionexchange=TT1['Current'].values
    print(TT1.iloc[:])

    #     print(startpos)
    ValueUSD=[1/conversionexchange[0]]
    ValueCAD=[1]
#     print(ValueCAD,ValueUSD)
    # print(conversionexchange)
    for i in range(1,len(conversionexchange)):
    #         print('i=',i, 'len c',len(conversionexchange))
        if startpos[i]==0:
            ValueCAD.append(conversionexchange[i]*ValueUSD[-1])
        else:
            ValueUSD.append(ValueCAD[-1]/conversionexchange[i])
    # if startpos[-1]==1:
    # print(ValueCAD,ValueUSD)
    print('1$CAD or ',1/conversionexchange[0],'USD is:','Value in CAD =',ValueCAD[-1],'Value in USD =', ValueUSD[-1])#, 'in', np.timedelta64((TT1.index.values[-1]-TT1.index.values[0]),'D'))
    return (round(float(ValueCAD[-1]),4))

def Quantify_returns(params,Feed_pred,Days=100):
    # _,_,_,Feed_pred= merge_all(curtestex=Days)
    Yhat=Pred(Feed_pred.astype('float32'),params)
    TT=tester_table(Feed_pred,Yhat)
#     print(TT.iloc[50:120])
    evaluate_predictor(TT, 0.5)
    return

def Load_params(filename):
    with open("mySavedDict.txt", "rb") as myFile:
        params = pickle.load(myFile)
    return params
