import tensorflow as tf
def weight_variable(shape):
    initial= tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def model_n(X_train, Y_train, X_test, Y_test, X_predict, learning_rate = 0.001, keepprob1 =1, keepprob2=1, num_epochs = 10000, print_cost = True, layers = [4,50,1]):

    cost=[]
    layers_dims=layers
    parameters={}

    #Create Placeholders for data
    X=tf.placeholder(tf.float32)
    Y=tf.placeholder(tf.float32)

    #determine NN architecture and create variables for W&b
    W1=weight_variable([layers_dims[1],layers_dims[0]])
    b1=bias_variable([layers_dims[1],1])
    W2=weight_variable([layers_dims[2],layers_dims[1]])
    b2=bias_variable([layers_dims[2],1])
#     W3=weight_variable([layers_dims[3],layers_dims[2]])
#     b3=bias_variable([layers_dims[3],1])
    #Calculate forward prop with Z for each hidden layer
    keep_prob1 = tf.placeholder(tf.float32)
    keep_prob2 = tf.placeholder(tf.float32)

    X_drop = tf.nn.dropout(X, keep_prob1)
    Z1_drop=tf.matmul(W1,X_drop)+b1 #could use A1_drop
#     Z1=tf.matmul(W1,X)+b1
    A1=tf.nn.relu(Z1_drop)
    # Drop out
    A1_drop = tf.nn.dropout(A1, keep_prob2)

    Z2=tf.matmul(W2,A1_drop)+b2 #could use A1_drop
#     A2=tf.nn.relu(Z2)  # To use if 2 hidden layers
#     Z3=tf.matmul(W3,A2)+b3  # To use if 2 hidden layers


    #cross_entropy = determine loss
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Z2, labels=Y))

    #back_prop, determine update steps, update parameters with steps using tf.train.AdamOptimizer(learning rate).minimize(cross_entropy)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    #determine accuracy of training set
    correct_prediction = tf.equal(tf.round(tf.sigmoid(Z2)),Y)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #train model
    sess=tf.Session()
    sess.run(tf.global_variables_initializer())
    for i in range(num_epochs):
        _,c= sess.run([train_step, cross_entropy],feed_dict={X: X_train, Y: Y_train, keep_prob1: keepprob1, keep_prob2: keepprob2})

        if i%2500 == 0:
            train_accuracy = accuracy.eval(session=sess,feed_dict={
                X:X_train, Y: Y_train, keep_prob1:1.0, keep_prob2:1.0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        if print_cost == True and i % 10 == 0:
            cost.append(c)

    #determine accuracy of test set
    print('layers = ', layers, 'cost =', c, 'train accuracy =', train_accuracy)
    print('test accuracy=', sess.run(accuracy, feed_dict={X:X_test,Y:Y_test,keep_prob1:1.0, keep_prob2:1.0}))
    acc=sess.run(accuracy,feed_dict={X:X_test, Y:Y_test,keep_prob1:1.0, keep_prob2:1.0})
    parameters={'W1':sess.run(W1), 'W2': sess.run(W2),'b1':sess.run(b1),'b2':sess.run(b2)}
#     print('prediction USD will gain in 20d =',sess.run(tf.sigmoid(Z3), feed_dict={X:X_predict, keep_prob:1.0}))


    # plot the cost
    # plt.plot(np.squeeze(cost))
    # plt.ylabel('cost')
    # plt.xlabel('iterations (per tens)')
    # plt.title("Learning rate =" + str(learning_rate))
    # plt.show()
    return parameters, acc, train_accuracy

# parameters,acc=model_n(Xtrain,Ytrain,Xtest,Ytest, Feed_pred, num_epochs=20001, layers=[Xtrain.shape[0], 50, 1], learning_rate=0.001, keepprob=0.8)
