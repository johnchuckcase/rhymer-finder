from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
from num2words import num2words
from text2num import text2num
from collections import defaultdict, Counter
import random



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

#Change "fivethirty" into "five thirty"
# def space_out_numbers(lyrics):
#     for word in lyrics.split():
#         for i in range(3,len(word)-3): #shortest possible number word is three ("one","ten")
#             #if word can be split up into two number words
#             if text2num(word[:i]) and text2num(word[:i]):
#


#Called by lyrics2words and lyrics2lines
def preprocess_lyrics(lyrics):
    lyrics = re.sub('\[.*\]','',lyrics) #Get rid of block titles (e.g., [Verse 1], [Chorus])
    lyrics = re.sub('\(|\)','',lyrics)   #Get rid of words in parentheses
    lyrics = re.sub('[0-9]+',spell_out_num,lyrics) #Spell out numbers
    lyrics = lyrics.translate(dict.fromkeys(map(ord, string.punctuation))) #unicode translate out punctuation
    lyrics = re.sub('[A-Z]{2,}',lambda x: ' '.join(x.group(0)),lyrics) #Space out acronoyms
    lyrics = lyrics.lower()
    # lyrics = space_out_numbers(lyrics)
    return lyrics

def lyrics2words(lyrics):
    return preprocess_lyrics(lyrics).split()

def hasVowels(word):
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


def create_test_data(corpus):

    test_data = []
    #Loop over every song
    for lyrics in corpus:
        lyrics = lyrics2lines(lyrics)

        for i in range(len(lyrics)-1):
            if not lyrics[i] or not lyrics[i+1]:
                continue
            word1 = lyrics[i][-1]
            word2 = lyrics[i+1][-1]

            #do the last words of this line and next line rhyme?
            # if lp.doTheyRhyme(word1, word2) and not word1 == word2:
                # test_data.append([' '.join(lyrics[i]),' '.join(lyrics[i+1])])
            test_data.append([' '.join(lyrics[i]),' '.join(lyrics[i+1])])
    return test_data

def create_rhyme_dict(tab, artist = None):

    #Retrieve all lyrics
    if artist: #If looking for specific artist
        corpus = list(set([song['lyrics'] for song in tab.find({'artist':artist})]))
    else: #Return all artists
        corpus = list(set([song['lyrics'] for song in tab.find()]))

    #Preprocess lyrics and return list of words
    word_list = map(lambda lyrics: lyrics2words(lyrics),corpus)
    words = set([word for song in word_list for word in song]) #flatten list of list

    rhyme_dict = defaultdict(set)
    unknown = 0
    for word in words:

        #If word is unknown, try to figure out pronounciation
        # if not word in arpabet:
            # try_update_arpabet(word)

        # if known word and >= pronounciation has a vowel
        if word in arpabet and hasVowels(word):

            #loop over all possible pronounications of word
            for phones in arpabet[word]:

                #If this pronounciation has a vowel
                if any(map(lambda phon: phon[:2] in vowels,phones)):

                    #find the final vowel sound in the word
                    vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]

                    #Append word to rhyming dictionary
                    rhyme_dict[tuple(phones[vowel_ind:])].update([word])
    return rhyme_dict

def baseline_accuracy(test_data,rhyme_dict):
    scores = []
    best_poss_scores = []
    for i in range(10):
        #Predict new word
        hits = 0
        poss_hits = 0
        trys = 0
        for couplet in test_data:

            #Last word of first and second lines
            test_x = couplet[0].split()[-1]
            test_y = couplet[1].split()[-1]

            #If unknown word or vowel-less
            if not test_x in arpabet or not hasVowels(test_x):
                continue

            #Take first pronuciation
            phones = arpabet[test_x][0]

            #find the final vowel sound in the word
            vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]
            phones_to_rhyme = phones[vowel_ind:]

            #Create list of possible rhymes based on rhyming_dictionary
            poss_targets = rhyme_dict[tuple(phones_to_rhyme)]

            #PREDICT
            #Choose a random word from possible rhymes
            yhat = random.sample(poss_targets,1)[0]

            trys += 1
            if yhat == test_y:
                hits += 1

            if test_y in poss_targets:
                poss_hits += 1
        #compute accuracy and append to list
        scores.append(hits / float(len(test_data)))
        best_poss_scores.append(poss_hits / float(len(test_data)))
    return np.mean(scores), np.mean(best_poss_scores) #0.0065038 accuracy

#If word is not in arpabet, try to figure out if it can be tweaked
def try_update_arpabet(word):

    #"rappin" = "rapping", 20838 => 19511
    if word.endswith('in') and word + 'g' in arpabet:
        arpabet.update( {word : map(lambda pron: pron[:-1]+[u'N'],  arpabet[word + 'g'])} )

    #"trigga" = "trigger", 19511 => 19244
    elif word.endswith('a') and word[:-1] + 'er' in arpabet:
        arpabet.update( {word : map(lambda pron: pron[:-1]+[u'AH0'],  arpabet[word[:-1] + 'er'])} )

    #"aint" = "ain't", 19244 => 19231
    elif word.endswith('t') and word[:-1] + "'t" in arpabet:
        arpabet.update( {word : arpabet[word[:-1] + "'t"]} )

    #"copssss" = 'cops', 19231 => 18852
    elif re.findall(r'(.)\1+\b',word) and re.sub(r'(.)\1+\b',r'\1',word) in arpabet:
        arpabet.update( {word : re.sub(r'(.)\1+\b',r'\1',word)} )

    #'fivethirty' =
