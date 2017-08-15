import pandas as pd
import numpy as np
import re
import nltk
import string
from num2words import num2words
from collections import defaultdict, Counter
import random
import cPickle as pickle
from gensim.models import Word2Vec
import os

from text2num import text2num
import lyrics_preprocessing as lp

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW']

class rhymer_finder(object):
    def __init__(self, rhyme_dict = {}):
        #initialize rhyming dictionary
        self.rhyme_dict = rhyme_dict
        #define pronounciation dictionary
        self.arpabet = nltk.corpus.cmudict.dict()

    def load_w2v(self,w2v_model):
        self.w2v_model = w2v_model

    def process_corpus(self, corpus):
        self.rhyme_dict = self.create_rhyme_dict(corpus)

    def doTheyRhyme(self,word1,word2):
        try:
            phones1, phones2 = self.arpabet[word1], self.arpabet[word2]
            #if neither word have a vowel
            if (len(phones1) == 1 and not phones1[0][0] in vowels) or (len(phones2) == 1 and not phones2[0][0] in vowels):
                assert(0)
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


    def create_test_data(self,corpus):

        test_data = []
        #Loop over every song
        for lyrics in corpus:
            lyrics = [line.split() for line in lp.lyrics2lines(lyrics)]

            for i in range(len(lyrics)-1):
                if not lyrics[i] or not lyrics[i+1]:
                    continue
                word1 = lyrics[i][-1]
                word2 = lyrics[i+1][-1]

                #do the last words of this line and next line rhyme?
                if self.doTheyRhyme(word1, word2) and not word1 == word2:
                    test_data.append([' '.join(lyrics[i]),' '.join(lyrics[i+1])])

        return test_data

    def create_rhyme_dict(self, corpus):

        #Preprocess lyrics and return list of words
        word_list = map(lambda lyrics: lp.lyrics2words(lyrics),corpus)
        words = set([word for song in word_list for word in song]) #flatten list of list

        rhyme_dict = defaultdict(set)
        unknown = 0
        known = 0
        for word in words:
            #If word is unknown, try to figure out pronounciation
            if not word in self.arpabet:
                self.try_update_arpabet(word)
            # if known word and >= pronounciation has a vowel
            if word in self.arpabet and lp.hasVowels(word,self.arpabet):
                #loop over all possible pronounications of word
                for phones in self.arpabet[word]:
                    #If this pronounciation has a vowel
                    if any(map(lambda phon: phon[:2] in vowels,phones)):
                        #find the final vowel sound in the word
                        vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]
                        #Append word to rhyming dictionary
                        rhyme_dict[tuple(phones[vowel_ind:])].update([word])
                known += 1
            else:
                unknown +=1
        print "known words:", known
        print "unknown words:", unknown
        return rhyme_dict

    def accuracy(self,test_data):
        scores = []
        scores_bl = []
        best_poss_scores = []

        self.couplet_counter = Counter()
        self.couplet_counter_bl = Counter()

        #Run through calculations n times to minimize accuracy metric variance
        for i in range(10):
            hits = 0
            hits_bl = 0
            poss_hits = 0
            trys = 0
            for i_coup, couplet in enumerate(test_data):

                #Last word, first line
                test_x = couplet[0].split()[-1]
                #Last word, second line
                test_y = couplet[1].split()[-1]
                #All words except last word
                training = couplet[0].split() + couplet[1].split()[:-1]

                #If unknown word or vowel-less
                if not test_x in self.arpabet or not lp.hasVowels(test_x,self.arpabet):
                    continue

                #Take first pronuciation
                phones = self.arpabet[test_x][0]

                #find the final vowel sound in the word
                vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]
                phones_to_rhyme = phones[vowel_ind:]

                #Create list of possible rhymes based on rhyming_dictionary
                poss_targets = np.array(list(self.rhyme_dict[tuple(phones_to_rhyme)]))

                #if no possible targets, don't even try to predict
                if not any(poss_targets):
                    continue

                #Keep only the possible rhymes that are known by the Word2Vec model
                filt_targets = np.array(filter(lambda word: word in self.w2v_model, poss_targets))

                #Calculate the average Word2Vec vector for the lyrics
                coup_vec = lp.avg_vec(training,self.w2v_model)

                #Calculate cosine similarity between average vec and every possible rhyme
                sims = np.array(map(lambda word: lp.cosine_sim(coup_vec,self.w2v_model[word]),filt_targets))


                if not np.any(sims):
                    yhat = np.random.choice(poss_targets,1)[0]
                else:
                    yhat = filt_targets[np.argmax(sims)]

                #PREDICT BASELINE
                #Choose a random word from possible rhymes
                yhat_bl = np.random.choice(poss_targets,1)[0]


                if yhat == test_y:
                    self.couplet_counter[i_coup] += 1
                    hits += 1

                if yhat_bl == test_y:
                    hits_bl += 1
                    self.couplet_counter_bl[i_coup] += 1

                if test_y in poss_targets:
                    poss_hits += 1

            #compute accuracy and append to list
            scores.append(hits / float(len(test_data)))
            scores_bl.append(hits_bl / float(len(test_data)))
            best_poss_scores.append(poss_hits / float(len(test_data)))
        print "RhymerFinder Accuracy:", np.mean(scores)
        print "Baseline Accuracy:", np.mean(scores_bl)
        print "Greatest Possible Accuracy:", np.mean(best_poss_scores) #0.0065038 accuracy

    #If word is not in arpabet, try to figure out if it can be tweaked
    def try_update_arpabet(self,word):

        #"rappin" = "rapping", 20838 => 19511
        if word.endswith('in') and word + 'g' in self.arpabet:
            self.arpabet.update( {word : map(lambda pron: pron[:-1]+[u'N'],  self.arpabet[word + 'g'])} )

        #"trigga" = "trigger", 19511 => 19244
        elif word.endswith('a') and word[:-1] + 'er' in self.arpabet:
            self.arpabet.update( {word : map(lambda pron: pron[:-1]+[u'AH0'],  self.arpabet[word[:-1] + 'er'])} )

        #"aint" = "ain't", 19244 => 19231
        elif word.endswith('t') and word[:-1] + "'t" in self.arpabet:
            self.arpabet.update( {word : self.arpabet[word[:-1] + "'t"]} )

         #"copssss" = 'cops', 19231 => 18852
        elif re.findall(r'(.)\1+\b',word) and re.sub(r'(.)\1+\b',r'\1',word) in self.arpabet:
            self.arpabet.update( {word : re.sub(r'(.)\1+\b',r'\1',word)} )

    #To replicate the web app RhymerFinder.com
    def find_rhyme(self,lyrics,word_to_rhyme):

        #If unknown word or vowel-less
        if not word_to_rhyme in self.arpabet or not lp.hasVowels(word_to_rhyme,self.arpabet):
            print "Unknown rhyme word"
            return None

        #Take first pronuciation
        phones = self.arpabet[word_to_rhyme][0]

        #find the final vowel sound in the word
        vowel_ind = np.where(map(lambda phone: phone[:2] in vowels,phones))[0][-1]
        phones_to_rhyme = phones[vowel_ind:]

        #Create list of possible rhymes based on rhyming_dictionary
        poss_targets = np.array(list(self.rhyme_dict[tuple(phones_to_rhyme)]))

        #if no possible targets, don't even try to predict
        if not any(poss_targets):
            print "No possible targets"
            return None

        #Find the average W2V vector over all words
        word_list = lyrics
        line_vec = lp.avg_vec(word_list,self.w2v_model)
        poss_targets = np.array(filter(lambda word: word in self.w2v_model, poss_targets))

        sims = map(lambda word: lp.cosine_sim(line_vec,self.w2v_model[word]),poss_targets)
        sims = np.array(map(lambda num: round(num,2),sims))
        sorted_inds = np.argsort(sims)[::-1]

        # print pd.DataFrame({"Rhymes" : poss_targets[sorted_inds], "Cos-sim" : sims[sorted_inds]})
        return pd.DataFrame({"Rhymes" : list(poss_targets[sorted_inds]), "Cos-sim" : list(sims[sorted_inds])})
