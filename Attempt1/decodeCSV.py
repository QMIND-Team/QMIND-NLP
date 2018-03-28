#Read from the csvs
import pandas as pd
import numpy as np
import math
import os
import tflearn

NUM_STEPS = 6000

#Import the TestX from the csv.  It's a list of lists.
collapsedTestX = pd.read_csv("TestData/testX.csv", sep=',', header=None)
collapsedTestX = collapsedTestX.values.tolist()

#Import the TrainX from the csv.  It's a list of lists.
collapsedTrainX = pd.read_csv("TrainData/trainX.csv", sep=',', header=None)
collapsedTrainX = collapsedTrainX.values.tolist()

#Import the TrainY from the csv.  It's a list of lists.
trainY = pd.read_csv("TrainData/trainY.csv", sep=',', header=None)
trainY = trainY.values.tolist()

#Import the TestY from the csv.  It's a list of lists.
testY = pd.read_csv("TestData/testY.csv", sep=',', header=None)
testY = testY.values.tolist()

#Through some numpy magic, grab only the first 100 time steps from each person
testX = np.array(collapsedTestX)
midTestX = testX[:,0:NUM_STEPS*13].tolist()

trainX = np.array(collapsedTrainX)
midTrainX = trainX[:,0:NUM_STEPS*13].tolist()

#We don't need collapsed... anymore.  Delete it to (hopefully) get some meory back

del collapsedTestX
del collapsedTrainX

#Split the file back into the time steps.  Each time step is 13 point long
testX = []
for person in midTestX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    '''
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    '''
    testX.append(chunks)

trainX = []
for person in midTrainX:
    chunks = [person[x:x+13] for x in range(0, len(person), 13)]
    '''
    for chunk in list(chunks):
        if(math.isnan(chunk[0])):
            chunks.remove(chunk)
    '''
    trainX.append(chunks)

# Get rid of mid...

del midTestX
del midTrainX


#gets rid of some stupid warning about CPU extensions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#network building

net = tflearn.input_data([None, NUM_STEPS, 13])

net = tflearn.lstm(net, 128, dropout=0.8)

net = tflearn.fully_connected(net, 17, activation='softmax')

net = tflearn.regression(net, optimizer='adam', learning_rate =0.001, loss='categorical_crossentropy')

model = tflearn.DNN(net)

model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True, batch_size=1)

model.save('accent-lstm')
