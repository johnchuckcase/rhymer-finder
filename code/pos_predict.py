import pandas as pd
import spacy
import lyrics_preprocessing as lp


# A function to predict the part of speech for the last word
class POS(object):

    def __init__(self):
        self.parser = spacy.en.English()
        self.model = None

    def fit(self, corpus):
        #Create list of words within a list of lines
        lines = lp.corpus2lines(corpus)
        X, y = get_XY(lines)

    def get_XY(self,lines):
        df = pd.DataFrame()
        i = 0
        while i < 100000:
            line_pos = [token.pos_ for token in nlp(lines[i])]
            if line_pos:
                for n_back in range(1,4): #look back five words
                    if len(line_pos) > n_back:
                        #Verb2 = the word 2 words back is a verb
                        df.loc[i,str(line_pos[-n_back-1])+str(n_back)] = 1
                df.loc[i,'label'] = line_pos[-1]
                i += 1
        df = df.fillna(0)
        return df.drop('label',axis=1).values, df['label'].values
