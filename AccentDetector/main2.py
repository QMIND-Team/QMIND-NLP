#Read from the csvs
import pandas as pd
import numpy as np
import math

#Import the TestX from the csv.  It's a list of lists.
collapsedTestX = pd.read_csv("TestData/testX.csv", sep=',', header=None)
collapsedTestX = collapsedTestX.values.tolist()

#Import the TrainX from the csv.  It's a list of lists.
collapsedTrainX = pd.read_csv("TrainData/trainX.csv", sep=',', header=None)
collapsedTrainX = collapsedTrainX.values.tolist()

trainY = pd.read_csv("TrainData/trainY.csv", sep=',', header=None)
trainY = trainY.values.tolist()

testY = pd.read_csv("TestData/testY.csv", sep=',', header=None)
testY = testY.values.tolist()

testX = np.array(collapsedTestX)
midtestX = testX[:,0:26000].tolist()

trainX = np.array(collapsedTrainX)
midtrainX = trainX[:,0:26000].tolist()


testX = []
for person in midtestX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    '''
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    '''
    testX.append(chunks)

trainX = []
for person in midtrainX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    '''
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    '''
    trainX.append(chunks)


#gets rid of some stupid warning about CPU extensions

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tflearn

#network building

net = tflearn.input_data([None, 2000, 13])

net = tflearn.lstm(net, 128, dropout=0.8)

net = tflearn.fully_connected(net, 17, activation='softmax')

net = tflearn.regression(net, optimizer='adam', learning_rate =0.001, loss='categorical_crossentropy')

model = tflearn.DNN(net)

model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True, batch_size=32)

model.save('accent-lstm')
