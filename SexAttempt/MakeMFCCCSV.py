import pandas as pd
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import tflearn as tf
import time
import numpy as np

dataraw = pd.read_csv("WavFiles/speakers_all_new.csv", sep=',')
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

fullIn = []


t = time.time()

count = 0

for person in data:
    if (not (person[ACCENT_COL] == 'rem')):
        (sampleRate, signal) = wav.read("WavFiles/" + person[NAME_COL] + ".wav")
        mfccTensor = mfcc(signal, samplerate = sampleRate, nfft=2048, winlen=0.01, winstep=0.01)
        fullIn.append([mfccTensor, person[SEX_COL]])
        count +=1
        print(count)

np.random.shuffle(fullIn)
trainIn = fullIn[:int(len(fullIn)*0.8)]
testIn = fullIn[int(len(fullIn)*0.8):]

trainX = []
trainY = []
for thing in trainIn:
    trainX.append(thing[0])
    trainY.append(thing[1])

trainY = tf.data_utils.to_categorical(list(trainY), 2)

testX = []
testY = []
for thing in testIn:
    testX.append(thing[0])
    testY.append(thing[1])

testY = tf.data_utils.to_categorical(list(testY), 2)

elapsed = time.time() - t

print(elapsed)

#Collapse trainX
collapsedTrainX = []
for person in trainX:
    collapsedPerson = []
    for timeStep in person:
        collapsedPerson.extend(timeStep)
    collapsedTrainX.append(collapsedPerson)

collapsedTestX = []
for person in testX:
    collapsedPerson = []
    for timeStep in person:
        collapsedPerson.extend(timeStep)
    collapsedTestX.append(collapsedPerson)

# Convert each to a panda data frame, and output each to a csv
df = pd.DataFrame.from_records(collapsedTrainX)
df.to_csv("TrainData/trainX.csv", index=False, header=False)
df = pd.DataFrame.from_records(collapsedTestX)
df.to_csv("TestData/testX.csv", index=False, header=False)
df = pd.DataFrame.from_records(trainY)
df.to_csv("TrainData/trainY.csv", index=False, header=False)
df = pd.DataFrame.from_records(testY)
df.to_csv("TestData/testY.csv", index=False, header=False)
