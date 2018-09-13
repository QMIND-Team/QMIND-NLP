#Predict a single test
import tflearn
import pandas as pd
import scipy.io.wavfile as wav
from python_speech_features import mfcc

#Open the speakers csv
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

#Make sure this is consistent with the way the model was trained
NUM_STEPS = 1650

#Pick which person we're testing on
PERSON_NUM = 300

#Pick a valid person
P_NUM_ORIG = PERSON_NUM


#Set the person
person = data[PERSON_NUM]

#Let the user know if their person was invalid
if PERSON_NUM != P_NUM_ORIG:
    print("Person", P_NUM_ORIG, "was invalid")
    print("Chose", PERSON_NUM, "instead")

#Create the mfcc
#(sampleRate, signal) = wav.read("WavFiles/" + person[NAME_COL] + ".wav")
(sampleRate, signal) = wav.read("WavFiles/" + "Johnny2.wav")
mfccTensor = mfcc(signal, samplerate=sampleRate, nfft=2048)

#Chop the data accordingly
mfccTensor = [mfccTensor[:NUM_STEPS]]

#Craete the net
print("Reconstructing Network...")
net = tflearn.input_data([None, NUM_STEPS, 13])

net = tflearn.lstm(net, 128, dropout=0.8)

net = tflearn.fully_connected(net, 17, activation='softmax')

net = tflearn.regression(net, optimizer='adam', learning_rate =0.001, loss='categorical_crossentropy')

model = tflearn.DNN(net)

#Load previously trained data
print("Loading Model Into Network..")
model.load('accent-lstm')

#Some instructinos
print()
print()
print("How to read these next outputs: The \"predict\" output is the actual output vector.  The values represent how likely the model thinks the input is that output.  So, if the output was [0.35, 0.25, 0.4] then the model thinks the person was [0,0,1] with 40% certainty, [0,1,0] with 25% accuracy, and [1,0,0] with 35% accuracy.  The \"predict_label\" output is the predicted labels, in order of certainty.  So, for the previous example, it would output [2, 0, 1].  Since it thinks the input was a \"2\", but it's also possible it was a \"0\", and unlikely a \"1\"")
print()
print()

accents = ['Southern', 'Regular English', 'Arabic', 'East Asian', 'French', 'Australian', 'British', 'Irish', 'Scottish', 'Latino', 'Indian', 'Russian', 'Slavic', 'German', 'Italian', 'Nordic', 'West African']
#Do the prediction
print("Predicting...")
predict = model.predict(mfccTensor)[0]
predict_label = model.predict_label(mfccTensor)[0]

#Round so they look good
predict = [ round(elem, 3) for elem in list(predict) ]

print("predict:", predict)

sum = 0
for thing in predict:
    sum += thing

print("Sum of predictions", sum)
print("predict_label:", predict_label)
print()
print()
print("The Model's Prediction:  ", accents[predict_label[0]], "", predict[predict_label[0]]*100, "%")
#print("Person was actually a", person[ACCENT_COL])



