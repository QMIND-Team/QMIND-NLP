import os
import pandas as pd
try:
    dataraw = pd.read_csv("speakers_all_new.csv", sep=',')
except Exception as e:
    raise FileNotFoundError("Please put the \"speakers_all_new.csv\" made by \"AddAccentColumn.py\" into this folder!")

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
for person in data:
    if(person[ACCENT_COL] == 'rem'):
        try:
            os.remove(person[NAME_COL] + ".wav")
        except:
            count += 1
            print(person[NAME_COL])
print(count)
