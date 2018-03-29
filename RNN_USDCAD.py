# cd ~/tensorflow/bin
# import activate_this
import tensorflow as tf
import keras as ke
# from keras.layers import TimeDistributed

# cd /Users/Thomas/github/usd_cad_NN
# import newest_data
# import get_US_Bank
from get_data import *
from datautils import *
from model_eval_funcs import *
import pandas as pd
import _pickle as pickle
import h5py
# from model_eval_funcs import *




def resizing(X,Y, window):
    inputs=np.zeros([X.shape[1]-window,X.shape[0],window])
    for i in range(X.shape[1]-window):
        inputs[i,:,:]=X[:,i:i+window]
    X_sized=np.transpose(inputs,(0,2,1))
    Y_sized=Y.reshape(-1,1)
    Y_sized=Y_sized[window:,:]
    return X_sized, Y_sized


def batch_culling(X,Y, bs=64):
    batches=len(X)//bs
    X_culled=X[:batches*bs,:,:]
    Y_culled=Y[:batches*bs,:]
    return X_culled,Y_culled

def model(Tx, Ty, nfeatures, neurons, prob, mode='single_dense'):

    x=ke.layers.Input(shape=(Tx,nfeatures))

    model = ke.models.Sequential()
    model.add(ke.layers.LSTM(neurons, input_shape=(Tx,nfeatures), return_sequences=True, stateful=True)) #returning sequences if true means 3D output, instead of 2D for false
    if mode== 'double_dense':
        model.add(ke.layers.Dense(32,activation='relu'))
        model.add(ke.layers.Dropout(prob))
    model.add(ke.layers.Dense(1,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model
    # return model

def modelB(Tx, Ty, nfeatures, neurons, prob, mode='single_dense',bs=64):

    x=ke.layers.Input(shape=(Tx,nfeatures),batch_shape=(bs,Tx,nfeatures))


    lstm_out=ke.layers.LSTM(neurons, input_shape=(Tx,nfeatures), return_sequences=True, stateful=True)(x) #returning sequences if true means 3D output, instead of 2D for false
    lstm_out=ke.layers.LSTM(5, input_shape=(Tx,nfeatures), return_sequences=True, stateful=True)(x) #returning sequences if true means 3D output, instead of 2D for false
    # if mode== 'double_dense':
    #     model.add(ke.layers.Dense(32,activation='relu'))
    #     model.add(ke.layers.Dropout(prob))
    flat=ke.layers.Flatten()(lstm_out)
    y=ke.layers.Dense(1,activation='sigmoid')(flat)
    model = ke.models.Model(inputs=x, outputs=y)
    model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.summary()

    return model

Bonds, OilN, NetSp, FundsRates, Jobs=get_data()
# Curr=get_curr(10)
# Feed, Y, Ymag, Feed_pred=merge_all(Curr, Bonds, OilN, NetSp, FundsRates, Jobs, 200)
# Xtrain, Ytrain, Xtest, Ytest, Xdev, Ydev= SplitData3waysequential(Feed.values,Y)
# Modelo=model(window, 1, training_inputs.shape[2], 32)
# window=30
# training_inputs,Ytrain=resizing(Xtrain,Ytrain,window)
# Xtest,Ytest=resizing(Xtest,Ytest,window)
# Xdev,Ydev=resizing(Xdev,Ydev,window)
# temp=Modelo.fit(training_inputs,Ytrain,epochs=2,batch_size=128)
# Modelo.test_on_batch(Xtest,Ytest)[1]
# Modelo.test_on_batch(Xdev,Ydev)
# dir(temp)
#
# dir(h5py)
def train_test_RNNmodel(Bonds,OilN,NetSp,FundsRates, Jobs, daysahead=[20],shapes=[12], timesteps=[20],probs=[1], mode='single_dense', epochs=50, bs=64):
  # Testing using test/dev sets from the most recent data and all other data for training set
  testtime=str(pd.Timestamp.now().day)+'_'+str(pd.Timestamp.now().hour)+'_'+str(pd.Timestamp.now().minute)
  testtimestr='test_resultsRNN'+str(testtime)+'.txt'
  bestparamtime='best_paramsRNN'+str(testtime)+'.h5'
  file=open(testtimestr,'w')
  file.write('Test Accuracy, Training Accuracy, Test Loss, Training Loss, days ahead, timesteps, LSTMneurons, dropout')
  file.close()
  test_results =[]
  R=[]
  r_initial=1.0
  test_accuracy=0.4
  counter=0
  for i in daysahead:
      Curr= get_curr(i)
      Feed, Y, _,Feed_pred=merge_all(Curr,Bonds,OilN,NetSp,FundsRates, Jobs, 212)
      Xtrain,Ytrain,Xtest,Ytest,Xdev,Ydev=SplitData3waysequential(Feed.values,Y)
      for j in timesteps:
          X_tr,Y_tr=resizing(Xtrain,Ytrain,j)
          X_te,Y_te=resizing(Xtest,Ytest,j)
          X_tr,Y_tr=batch_culling(X_tr,Y_tr,bs=bs)
          X_te,Y_te=batch_culling(X_te,Y_te,bs=bs)
          for k in shapes:
              for l in probs:
                  modelo=modelB(j,1,X_tr.shape[2],k,l, mode,bs=bs)
                  Trained=modelo.fit(X_tr,Y_tr,epochs=epochs,batch_size=bs)
                  # for m in probs:
                      # parameters,Acc,Train=model(Xtrain,Ytrain,Xdev,Ydev, num_epochs=10001, layers=[Xtrain.shape[0], k, 1], learning_rate=0.001, keepprob1=l, keepprob2=m)
                      # print(i,'days ahead,', l, 'prob1,', m, 'prob2')
                      # test_results.append((Acc,Train))
                      # R.append(Quantify_returns(parameters, Feed_pred))
                  Acc=modelo.evaluate(x=X_te,y=Y_te,batch_size=bs)[-1]
                  Te_loss=modelo.evaluate(x=X_te,y=Y_te,batch_size=bs)[0]
                  TrainAcc=Trained.history['acc'][-1]
                  Train_loss=Trained.history['acc'][0]
                  X,_=resizing(Feed_pred.values,Y , j)
                  X,_=batch_culling(X,Y,bs=64)
                  Yhat=modelo.predict(X,batch_size=64)
                  Feed_pred_cut=Feed_pred.iloc[:,-192:]
                  r=Quantify_returns_keras(Feed_pred_cut,Yhat)
                  file=open(testtimestr,'a')
                  file.write('\n'+str(Acc)+','+str(TrainAcc)+','+str(Te_loss)+','+str(Train_loss)+','+str(i)+','+str(j)+','+str(k)+','+str(l)+','+str(r))
                  file.close()
                  print('test results',Acc)
                  counter+=1
                  print('run number:',counter,'/',len(daysahead)*len(timesteps)*len(shapes)*len(probs))
                  print('daysahead:',i,', timesteps:',j,', shapes:',k, 'probs:',l)
                  # if Acc>test_accuracy:# and Acc<TrainAcc:
                  #     test_accuracy=Acc
                  #     modelo.save(bestparamtime)
                  #     best_model=modelo
                  #     print('test results updated',Acc)
                  if r>r_initial:# and Acc<TrainAcc:
                      r_initial=r
                      modelo.save(bestparamtime)
                      best_model=modelo
                      print('test results updated',r)
                      R.append([i,j,k])
                      # Day_Un_P1_P2=[i,k,l,m]
      # with open(bestparamtime, "wb") as myFile:
  #   pickle.dump(best_params, myFile)
  print('test results',Acc)
  print(R)
  return best_model, Feed_pred, Y


# modela, Feed_pred, Y=train_test_RNNmodel(Bonds,OilN,NetSp,FundsRates, Jobs, daysahead=[5, 20],shapes=[10,20,30], timesteps=[10,20],probs=[1], mode='single_dense',bs=64)
modela, Feed_pred, Y=train_test_RNNmodel(Bonds,OilN,NetSp,FundsRates, Jobs, daysahead=[5,10,15],shapes=[20,30], timesteps=[10,20],probs=[0.9], mode='double_dense',epochs=50,bs=64)
# i,j,k,l=20,10,12,1
# X,Y=X_tr,Y_tr
# bs=64
# mode='single_dense'
# epochs=20
# modela=ke.Model()
# modela=ke.models.load_model('best_paramsRNN22_11_59.h5')
X,_=resizing(Feed_pred.values,Y , 20)
# X,_=batch_culling(X,Y,bs=64)
# X.shape
Yhat=modela.predict(X,batch_size=64)
# Yhat.shape
Feed_pred_cut=Feed_pred.iloc[:,20:]
# Yhat
# from model_eval_funcs import *
Quantify_returns_keras(Feed_pred_cut,Yhat)
# TT=tester_table(Feed_pred_cut,Yhat)
# #     print(TT.iloc[50:120])
# Yhat
# R=evaluate_predictor(TT, 0.5)
