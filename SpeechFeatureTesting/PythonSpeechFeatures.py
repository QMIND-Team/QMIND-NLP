from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
import csv

(sampleRate, signal) = wav.read("WavFiles/english17.wav")

#newsignal = []
#for point in list(signal):
   # newsignal.append(point[0])



mfccTensor = mfcc(signal, samplerate = sampleRate, nfft=2048)

print(type(mfccTensor))
np.savetxt("mfccFile.csv", mfccTensor, delimiter=",")
#np.savetxt("newsignal.csv", newsignal, delimiter=",")