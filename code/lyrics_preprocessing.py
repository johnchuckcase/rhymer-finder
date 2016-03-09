from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
from num2words import num2words
from collections import defaultdict

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Get pronouncation dictionary
arpabet = nltk.corpus.cmudict.dict()
vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']

#Change numbers into words
def spell_out_num(st):
    st = st.group(0) #Expects a regex return object
    num = int(st)
    if num <= 100:
        return num2words(num).replace('-',' ')
    else:
        return st #Deal with 'one thousand, nine hundred and ninety-nine' cases later

#Called by lyrics2words and lyrics2lines
def preprocess_lyrics(lyrics):
    lyrics = re.sub('\[.*\]','',lyrics) #Get rid of block titles (e.g., [Verse 1], [Chorus])
    lyrics = re.sub('\(|\)','',lyrics)   #Get rid of words in parentheses
    lyrics = re.sub('[0-9]+',spell_out_num,lyrics) #Spell out numbers
    lyrics = lyrics.translate(dict.fromkeys(map(ord, string.punctuation))) #unicode translate out punctuation
    lyrics = re.sub('[A-Z]{2,}',lambda x: ' '.join(x.group(0)),lyrics) #Space out acronoyms
    lyrics = lyrics.lower()
    return lyrics

def lyrics2words(lyrics):
    return preprocess_lyrics(lyrics).split()

def hasVowels(word):
    print word
    for pronounce in arpabet[word]:
        if any(map(lambda phone: phone[:2] in vowels,pronounce)):
            return True
    return False

#Return list of lists: each line has a list of its words
def lyrics2lines(lyrics):
    lines = re.split('\n+',preprocess_lyrics(lyrics).replace('\r','').strip())
    return [line.split() for line in lines]

def doTheyRhyme(word1,word2):
    try:
        phones1, phones2 = arpabet[word1], arpabet[word2]
        #if neither word have a vowel
        if (len(phones1) == 1 and not phones1[0][0] in vowels) or (len(phones2) == 1 and not phones2[0][0] in vowels):
            assert(0)
    except AssertionError:
        return False
    except:
        return False
    #They rhyme if the last vowel phoneme and all subsequent phonemes match
    for phone1 in phones1:
        for phone2 in phones2:
            #In the list of phonemes for each word, find the last vowel sound. phone[:2] excludes stress from consideration
            vowel_ind1 = np.where(map(lambda phone: phone[:2] in vowels if len(phone)>1 else phone[0],phone1))[0][-1]
            vowel_ind2 = np.where(map(lambda phone: phone[:2] in vowels if len(phone)>1 else phone[0],phone2))[0][-1]
            if phone1[vowel_ind1:] == phone2[vowel_ind2:]:
                return True
    return False


def create_rhyme_dict(artist = None):

    #Retrieve all lyrics
    if artist: #If looking for specific artist
        corpus = list(set([song['lyrics'] for song in tab.find({'artist':artist})]))
    else: #Return all artists
        corpus = list(set([song['lyrics'] for song in tab.find()]))

    #Preprocess lyrics and return list of words
    word_list = map(lambda lyrics: lyrics2words(lyrics),corpus)
    words = set([word for song in word_list for word in song]) #flatten list of list

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
                    if hasVowels(phones):
                        #find the final vowel sound in the word
                        vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]

                        if not word in rhyme_dict[tuple(phones[vowel_ind:])]:
                            rhyme_dict[tuple(phones[vowel_ind:])].append(word)
    return rhyme_dict
