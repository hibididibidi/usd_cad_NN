# usd_cad_NN
binary classification neural network to predict whether to own US dollar or Canadian dollar

#Introduction
This program pulls data from the web (mostly from Quandl but also some data .csv files), creates a training set of 39 inputs, trains a single layer Neural Netowrk, that uses binary classification to determine whether the value of the USD compared with CAD will increase (1) or decrease(0) in a specified number of days ahead.
It is a study to see how well this type of network can predict the outcome given fairly well known correlated values.

#Data Gathering and Manipulation
Data is normalized if the mean of the input was outside of the range -10:10 or the std was outside 0.1-10.
Many of the data values are not daily and therefore missing data is filled from previous values.
Each data set has different start dates and therefore the earliest date that was used was from the latest start date.
Some monthly data (i.e. jobs report) is released on a certain day so that data had to be shifted to apply only once it had become available.  
To give an indication of whether the exchange rate was trending up or down, the valuefrom the previous day was included as well as the 5, 10, 30 and 100 day moving averages

The training set data has actual dates stripped off.
In order to avoid training the network on training examples that may be very similar (caused by filling of missing data) to the test/dev examples, only the first 90% of data is used in the training set and the latest 10% is used in the development and test sets (5% each). 

#Setting up and Training the Model
The model was trained with:
  - different dropout probabilities applied on both the input and hidden layer. 
  - different number of units in the hidden layer.
  - different number of "days ahead" in which the exchange rate was evaluated as being greater than or less than the current
  - Relu acitivation function for hidden layer
  - Sigmoid activation function for the output layer

The trained model with the greatest accuracy on the development set and had a training accuracy greater than the dev set accuracy was determined and the parameters for the model were saved as "best_params".
The metric used to determine whether or successful implementation was if the model could achieve a test set accuracy of 67%. This is considered somewhat abitrary however it was viewed as a value that in the long run would prove to be profitable.

Testing the Trained Model
These "best_params" were then used to evaluate the model on the test set and to see how well the model performed, it was backtested in chronological order on the most recent X number of days where if the model predicted the USD/CAD were to increase, a starting value of 1$CAD would be exchanged into USD and converted back and forth depending on the output of the model. 
Because the sigmoid function was used as the activation of the output layer, the final output value was a probability and as such the threshold or required probability to exchange the currency could be altered from the default of 0.5.

#HOW TO USE
To train network, open python and run :
$ from gather_train import *

This will then prompt you to train the NN with default drop out, hidden units, daysahead parameters. This only runs one set of parameters. If you'd like to see the network run on multiple parameters, decline the prompt to train and use the function train_model with any values for the parameters as outlined in the model_eval_funcs.py file. One the model has been trained, the weights and biases that result in the greatest accuracy of the development set are saved into a dictionary called best_params and also saved into a new .txt file whose title begins best_params. If you'd like to load an old set of params, run the Load_params(filename) function.

To test the profitability of the model, the function Quantify_returns can be run which takes the most recent X number of days (100 as default) and starts with 1$CAD and converts it back and forth to USD when the model so dictates.

