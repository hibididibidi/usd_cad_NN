#predictor
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

def run_model(days)
  # Testing using test/dev sets from the most recent data and all other data for training set
  testtime=str(pd.Timestamp.now().day)+'_'+str(pd.Timestamp.now().hour)
  testtimestr='test_results'+str(testtime)+'.txt'
  file=open(testtimestr,'w')
  file.write('Test Accuracy, Training Accuracy, days ahead, hidden units, keep prob1, keep prob2')
  file.close()
  days=[10,12,14]
  shapes=[10,13,16]
  probs=[0.8,0.9,1]
  test_results =[]
  test_accuracy=0.6
  for i in days:
      Curr= Currency(USDCAD,i)
      Feed, Y, _,_=merge_all()
      Xtrain,Ytrain,Xtest,Ytest,Xdev,Ydev=SplitData3way(Feed.values,Y)
      for k in shapes:
          for l in probs:
              for m in probs:
                  parameters,Acc,Train=model_n(Xtrain,Ytrain,Xdev,Ydev, Xtest, num_epochs=10001, layers=[Xtrain.shape[0], k, 1], learning_rate=0.001, keepprob1=l, keepprob2=m)
                  print(i,'days ahead,', l, 'prob1,', m, 'prob2')
                  test_results.append((Acc,Train))
                  file=open(testtimestr,'a')
                  file.write('\n'+str(Acc)+','+str(Train)+','+str(i)+','+str(k)+','+str(l)+','+str(m))
                  file.close()
                  if Acc>test_accuracy and Acc<Train:
                      test_accuracy=Acc
                      best_params=parameters
                      Day_Un_P1_P2=[i,k,l,m]
  return print('test results',test_results)
