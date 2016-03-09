from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
import lyrics_preprocessing as lp


# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

test_data = []

#Loop over every song
for lyrics in corpus:
    lyrics = lp.lyrics2lines(lyrics)

    for i in range(len(lyrics)-1):
        if not lyrics[i] or not lyrics[i+1]:
            continue
        word1 = lyrics[i][-1]
        word2 = lyrics[i+1][-1]

        #do the last words of this line and next line rhyme?
        if lp.doTheyRhyme(word1, word2) and not word1 == word2:
            test_data.append([' '.join(lyrics[i]),' '.join(lyrics[i+1])])

rhyme_dict = lp.create_rhyme_dict()

scores = []
for i in range(1000):
    #Predict new word
    hits = 0
    for couplet in test_data:
        #Last word of first line
        test_x = couplet[0].split()[-1]
        test_y = couplet[1].split()[-1]

        #Take first pronuciation
        phones = lp.arpabet[test_x][0]

        #find the final vowel sound in the word
        vowel_ind = np.where(map(lambda phone: phone[:2] in lp.vowels,phones))[0][-1]
        phones_to_rhyme = phones[vowel_ind:]

        poss_targets = rhyme_dict[tuple(phones_to_rhyme)]

        yhat = np.random.choice(poss_targets)

        if yhat == test_y:
            hits += 1
    scores.append(hits / float(len(test_data)))
print np.mean(scores)
print np.std(scores)
