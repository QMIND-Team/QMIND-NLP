#Script to make a histogram for the distribution of the lengths of the MFCCs

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
from python_speech_features import mfcc

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

count = 0

fullIn = []
for person in data:
    if (not person[ACCENT_COL] == 'rem'):
        (sampleRate, signal) = wav.read("WavFiles/" + person[NAME_COL] + ".wav")
        mfccTensor = mfcc(signal, samplerate = sampleRate, nfft=2048)
        fullIn.append([mfccTensor, person[ACCENT_COL]])
        count +=1
        print(count)

fullX = []
for thing in fullIn:
    fullX.append(thing[0])

counts = []
for person in fullX:
    counts.append(len(person))

plt.hist(counts, bins='auto')
plt.ylabel('Amount');

plt.show()

print("Done")
