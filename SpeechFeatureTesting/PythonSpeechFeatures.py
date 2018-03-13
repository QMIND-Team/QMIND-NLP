from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
import csv

(sampleRate, signal) = wav.read("WavFiles/english44.wav")
mfccTensor = mfcc(signal, samplerate = sampleRate, winlen=0.020, winstep=0.01)


#np.savetxt("mfccFile.csv", mfccTensor, delimiter=",")
np.savetxt("signal.csv", signal, delimiter=",")