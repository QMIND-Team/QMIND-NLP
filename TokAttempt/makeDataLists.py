print("Importing Modules")

import pandas as pd
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import tflearn as tf
import time
import numpy as np
import h5py

print("Reading CSV")

dataraw = pd.read_csv("speakers_all_new.csv", sep=',')
labels = dataraw.columns
data = dataraw.values.tolist()

AGE_COL = 0
ONSET_COL = 1
BIRTHPLACE_COL = 2
NAME_COL = 3
NATIVELANG_COL = 4
SEX_COL = 5
ID_COL = 6
COUNTRY_COL = 7
MISSING_COL = 8
LEARNMETHOD_COL = 9
RESIDENCE_COL = 10
LENGTH_COL = 11
ACCENT_COL = 12

NUM_STEPS = 1650

#This will eventually be made more efficient, but for now we'll do some stuff twice:

#This first bit here figures out the distribution of the accents

print("Determining Distribution")

count = 0
fullIn = []
for person in data:
    if (not person[ACCENT_COL] == 'rem'):
        fullIn.append([0, person[ACCENT_COL]])
        count +=1
        print(count)

fullY = []
for thing in fullIn:
    fullY.append(thing[1])

sum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for person in fullY:
    sum[int(person)] += 1

#Now, this code ACTUALLY creates fullIn.  Ignore all of the variables made in the upper section

print("Creating Dataset")

count = 0
fullIn = []
for person in data:
    if (not person[ACCENT_COL] == 'rem'):
        mfccTensor = pd.read_csv(person[NAME_COL] + "." + str(count))
        fullIn.append([mfccTensor, person[ACCENT_COL]])
        count += 1
        print(count)

np.random.shuffle(fullIn)
trainIn = fullIn[:int(len(fullIn)*0.8)]
testIn = fullIn[int(len(fullIn)*0.8):]

trainX = []
trainY = []
for thing in trainIn:
    #Data balancing here
    addNum = round(400/sum[int(thing[1])])
    for i in range(0,addNum):
        trainX.append(thing[0])
        trainY.append(thing[1])

#This definitely needs to shuffle again.  Make sure shuffle=True in model.fit in createNN.py

trainY = tf.data_utils.to_categorical(list(trainY), 17)

testX = []
testY = []
for thing in testIn:
    testX.append(thing[0])
    testY.append(thing[1])

testY = tf.data_utils.to_categorical(list(testY), 17)

midTestX = []
for person in testX:
    person = person[:NUM_STEPS]
    midTestX.append(person)

midTrainX = []
for person in trainX:
    person = person[:NUM_STEPS]
    midTrainX.append(person)


#These are fine
goodTestX = np.array(midTestX)
goodTrainX = np.array(midTrainX)

#These ones work
goodTestY = np.array(testY)
goodTrainY = np.array(trainY)

#Put them out to hdf5
h5f = h5py.File('data.h5', 'w')
h5f.create_dataset('testY',data=goodTestY)
h5f.create_dataset('testX',data=goodTestX)
h5f.create_dataset('trainY',data=goodTrainY)
h5f.create_dataset('trainX',data=goodTrainX)

h5f.close()

print("Done!  Make sure createNN.py uses " + str(NUM_STEPS) + " for NUM_STEPS")
