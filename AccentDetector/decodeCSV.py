#Read from the csvs
import numpy as np
import pandas as pd
import math

collapsedTestX = pd.read_csv("TestData/testX.csv", sep=',', header=None)
collapsedTestX = collapsedTestX.values.tolist()

testX = []
for person in collapsedTestX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    testX.append(chunks)

collapsedTrainX = pd.read_csv("TrainData/trainX.csv", sep=',', header=None)
collapsedTrainX = collapsedTrainX.values.tolist()

trainX = []
for person in collapsedTrainX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    trainX.append(chunks)

trainY = pd.read_csv("TrainData/trainY.csv", sep=',', header=None)
trainY = trainY.values.tolist()

testY = pd.read_csv("TestData/testY.csv", sep=',', header=None)
testY = testY.values.tolist()

np.savetxt("test.csv", trainX[0], delimiter=",")

#gets rid of some stupid warning about CPU extensions

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



import tflearn



# Data preprocessing (NOT BEING USED)

# Sequence padding

#trainX = pad_sequences(trainX, maxlen=100, value=0.)

#testX = pad_sequences(testX, maxlen=100, value=0.)



#Importing and reformatting data





#network building

net = tflearn.input_data([None, 2637, 13])

#net = tflearn.embedding(net, input_dim=10000, output_dim=128)

net = tflearn.lstm(net, 128, dropout=0.8)

net = tflearn.fully_connected(net, 2, activation='softmax')

net = tflearn.regression(net, optimizer='adam', learning_rate =0.001, loss='categorical_crossentropy')



model = tflearn.DNN(net)

model.fit(trainX, trainY, show_metric=True, batch_size=32)

model.save('accent-lstm')
