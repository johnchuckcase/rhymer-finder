import re
from num2words import num2words
import string
import cPickle as pickle
from nltk.corpus import stopwords
import numpy as np

vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']

#Called by lyrics2words and lyrics2lines
def preprocess_lyrics(lyrics):
    lyrics = lyrics.strip()
    lyrics = re.sub('\[.*\]','',lyrics) #Get rid of block titles (e.g., [Verse 1], [Chorus])
    lyrics = re.sub('\(|\)','',lyrics)   #Get rid of words in parentheses
    lyrics = re.sub('[0-9]+',spell_out_num,lyrics) #Spell out numbers
    lyrics = lyrics.translate(dict.fromkeys(map(ord, string.punctuation))) #unicode translate out punctuation
    lyrics = re.sub('[A-Z]{2,}',lambda x: ' '.join(x.group(0)),lyrics) #Space out acronoyms
    lyrics = lyrics.lower()
    # lyrics = space_out_numbers(lyrics)
    return lyrics

#Deconstruct list of lists into one list
def flatten(l):
    return [item for sublist in l for item in sublist]

def lyrics2words(lyrics):
    return preprocess_lyrics(lyrics).split()

def hasVowels(word,arpabet):
    for pronounce in arpabet[word]:
        if any(map(lambda phone: phone[:2] in vowels,pronounce)):
            return True
    return False

#Creates list of lines from string
def lyrics2lines(lyrics):
    return re.split('\n+',preprocess_lyrics(lyrics).replace('\r','').strip())

#Creates list of lines from corpus (list of strings)
def corpus2lines(corpus):
    return flatten(map(lyrics2lines,corpus))

#Change numbers into words
def spell_out_num(st):
    st = st.group(0) #Expects a regex return object
    num = int(st)
    if num <= 100:
        return num2words(num).replace('-',' ')
    else:
        return st #Deal with 'one thousand, nine hundred and ninety-nine' cases later

#Find the average vector for a list of words ("line")
def avg_vec(line,w2v_model):
    stop = stopwords.words('english')
    line = filter(lambda word: word not in stop and word in w2v_model,line)
    return reduce(lambda x,y: x+y,map(lambda word: w2v_model[word],line),np.zeros(w2v_model['the'].shape)) / len(line)
