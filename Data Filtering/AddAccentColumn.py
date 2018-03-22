# This script will add an "Accent" column to the main csv file

import pandas as pd

# Accents
Southern = ['texas', 'alabama', 'georgia, usa', 'tennesse', 'mississippi', 'north carolina', 'south carolina',
            'lousiana', 'arkansas', 'virginia, usa', 'kentuky', 'oklahama', 'west virginia']
RegularEnglish = ['ontario', 'saskatchewan', 'alberta', 'british columbia', 'manitoba', 'newfoundland', 'newbrunswick',
                  'prince edward island', 'california', 'pennsylvania', 'hawaii', 'michigan', 'illinois',
                  'arizona', 'colorado', 'alaska', 'minnesota', 'washington', 'missouri', 'oregon', 'wisconsin', 'indiana',
                  'connecticut', 'utah', 'new mexico', 'montana', 'maine', 'nevada', 'iowa', 'kansas', 'wyoming', 'nebraska',
                  'new hampshire', 'vermont', 'delaware', 'south dakota', 'north dakota', 'idaho'] #include english as native language

Arabic = ['egypt', 'saudi arabia', 'lebanon', 'morocco', 'iraq', 'yemen', 'bahrain', 'libya', 'kuwait',
          'united arab emirates', 'qatar', 'tunisia', 'algeria', 'jordan', 'oman']

EastAsain = ['china', 'tawain', 'singapore', 'japan', 'korea', 'thailand', 'vietnam']

French = ['france'] #include french as native language

British = ['england', 'wales']

Irish = ['ireland']

Scottish = ['scotland']

Latin = ['argentina', 'honduras', 'brazil', 'portugal', 'spain', 'mexico', 'colombia', 'chile', 'uruguay', 'bolivia',
         'chile', 'venezuela', 'ecuador']

Australian = ['australia']

Indian = ['india']

Russian = ['ukraine', 'russia', 'belarus', 'uzbekistan', 'moldova', 'estonia', 'latvia'] #include russian as native language

Slavic = ['serbia', 'macedonia', 'croatia', 'slovakia']

German = ['germany'] #include german as native language

Italian = ['italy']

Nordic = ['swedish', 'finnish', 'norwegian', 'icelandic', 'danish']

WestAfrican = ['nigeria', 'niger', 'ghana', 'togo', 'benin', 'liberia', 'sierra leone', 'guinea', 'mali', 'mauritania',
               'cameroon', 'chad']

# Read the data from the csv, and drop the unnecessary columns
dataraw = pd.read_csv("speakers_all.csv", sep=',')
dataraw['Accent'] = ''

labels = dataraw.columns

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

#Convert to a normal list of lists
data = dataraw.values.tolist()

#Start throwing things out
count = 0
for person in list(data):
    if "true" in str(person[MISSING_COL]).lower():
        count += 1
        data.remove(person)
    elif "synthesized" in person[NAME_COL]:
        count += 1
        data.remove(person)
        print(person)
    elif person[NATIVELANG_COL] != 'english' and person[ONSET_COL] < 5 and person[LENGTH_COL] > 5 and person[AGE_COL] < 40:
        count += 1
        print(person)
        data.remove(person)

#Check everything
for person in data:
    person[ACCENT_COL] = 'null'
    for place in Southern:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'southern'
            break
    if person[ACCENT_COL] != 'null':
        continue
    for place in RegularEnglish:
        if place in person[BIRTHPLACE_COL] and 'english' in person[NATIVELANG_COL]:
            person[ACCENT_COL] = 'american'
            break
    if person[ACCENT_COL] != 'null':
        continue
    for place in Arabic:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'arabic'
            break
    if person[ACCENT_COL] != 'null':
        continue
    for place in EastAsain:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'east asian'
            break
    if person[ACCENT_COL] != 'null':
        continue
    if 'france' in person[BIRTHPLACE_COL] and 'french' in person[NATIVELANG_COL]:
        person[ACCENT_COL] = 'french'
        continue
    #Keep australian before british.  New South Wales, Australia
    if 'australia' in person[BIRTHPLACE_COL]:
        person[ACCENT_COL] = 'australian'
        continue
    for place in British:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'british'
            break
    if person[ACCENT_COL] != 'null':
        continue
    if 'ireland' in person[BIRTHPLACE_COL]:
        person[ACCENT_COL] = 'irish'
        continue
    if 'scotland' in person[BIRTHPLACE_COL]:
        person[ACCENT_COL] = 'scottish'
        continue
    for place in Latin:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'latin'
            break
    if person[ACCENT_COL] != 'null':
        continue
    if 'india' in person[BIRTHPLACE_COL]:
        person[ACCENT_COL] = 'indian'
        continue
    for place in Russian:
        if place in person[BIRTHPLACE_COL] and 'russian' in person[NATIVELANG_COL]:
            person[ACCENT_COL] = 'russian'
            break
    if person[ACCENT_COL] != 'null':
        continue
    for place in Slavic:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'slavic'
            break
    if person[ACCENT_COL] != 'null':
        continue
    if 'germany' in person[BIRTHPLACE_COL] and 'german' in person[NATIVELANG_COL]:
        person[ACCENT_COL] = 'german'
        continue
    if 'italy' in person[BIRTHPLACE_COL]:
        person[ACCENT_COL] = 'italian'
        continue
    for place in Nordic:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'nordic'
            break
    if person[ACCENT_COL] != 'null':
        continue
    for place in WestAfrican:
        if place in person[BIRTHPLACE_COL]:
            person[ACCENT_COL] = 'west african'
            break
    if person[ACCENT_COL] != 'null':
        continue

# Convert back to a DataFrame
df = pd.DataFrame.from_records(data, columns=labels)
#print(df)

df.to_csv("speakers_all_new.csv", index=False)

# Make a fun table
table = {}
for person in data:
    if person[ACCENT_COL] not in table:
        table.update({person[ACCENT_COL] : 0})
    else:
        table.update({person[ACCENT_COL] : table[person[ACCENT_COL]]+1})

# Convert to a DataFrame object, for pretty printing :)
Tabdf = pd.DataFrame(list(table.items()))
# Name the columns
Tabdf.columns = ['accent','number']
#Sort descending by nunmber
Tabdf.sort_values(by='number', inplace=True, ascending=False)

#print(Tabdf)

# result = df.to_string(index=False, header=False)
# print(result)


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
