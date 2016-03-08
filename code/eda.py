from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
from num2words import num2words
from lyrics_preprocessing import lyrics2words
from collections import defaultdict

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

#Preprocess lyrics and return list of words
word_list = map(lambda lyrics: lyrics2words(lyrics),corpus)
words = set([word for song in word_list for word in song]) #flatten list of list

#Get pronouncation dictionary
arpabet = nltk.corpus.cmudict.dict()

vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']

rhyme_dict = defaultdict(list)
for vowel in vowels:
    for word in set(words):
        # if any of the possible pronounications rhyme with word
        if word in arpabet and \
            any(map(lambda phones: \
            any(map(lambda phone: vowel in phone, phones)), arpabet[word])):

            #loop over all possible pronounications of word
            for phones in arpabet[word]:
                #if word has vowels
                if any(map(lambda phone: phone[:2] in vowels,phones)):
                    #find the final vowel sound in the word
                    vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]

                    if not word in rhyme_dict[tuple(phones[vowel_ind:])]:
                        rhyme_dict[tuple(phones[vowel_ind:])].append(word)
