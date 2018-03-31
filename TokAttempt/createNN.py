print("Importing Modules")

import os
import tflearn
import h5py

NUM_STEPS = 1650

h5f = h5py.File('data.h5', 'r')
trainX = h5f['trainX']
trainY = h5f['trainY']
testX = h5f['testX']
testY = h5f['testY']

#gets rid of some stupid warning about CPU extensions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#network building
print("Building Network")

net = tflearn.input_data([None, NUM_STEPS, 13])

net = tflearn.lstm(net, 128, dropout=0.8)

net = tflearn.fully_connected(net, 17, activation='softmax')

net = tflearn.regression(net, optimizer='adam', learning_rate =0.001, loss='categorical_crossentropy')

model = tflearn.DNN(net)

model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True, batch_size=128, shuffle=True)

model.save('accent-lstm')
