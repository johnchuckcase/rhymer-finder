import pandas as pd
import spacy
import lyrics_preprocessing as lp
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from scipy.stats import randint as sp_randint
import os
import cPickle as pickle

#Find parent directory of this script
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

POSs = ['ADV','NOUN','ADP','SPACE','DET','SYM','INTJ','PART','PUNCT','VERB','X','NUM','CONJ','ADJ']

# A function to predict the part of speech for the last word
class POS(object):

    def __init__(self):
        self.parser = spacy.en.English()
        if os.path.isfile(project_dir + '/data/POS_model.pkl'):
            self.model = pickle.load()
        else:
            self.model = None

    def transform(self,lines, back = 3):
        #Create a list of all possible POS and n_backs (e.g., "ADJ2" = adjective two words back)
        cols = lp.flatten(map(lambda n_back: map(lambda pos:pos+str(n_back),POSs),range(1,back+1)))
        df = pd.DataFrame(columns = cols)
        i = 0
        while i < min(len(lines),100000):
            if i % 1000 == 0:
                print i
            line_pos = [token.pos_ for token in self.parser(lines[i])]
            if line_pos:
                for n_back in range(1,back+1): #look back five words
                    if len(line_pos) > n_back:
                        #Verb2 = the word 2 words back is a verb
                        df.loc[i,str(line_pos[-n_back-1])+str(n_back)] = 1
                df.loc[i,'label'] = line_pos[-1]
                i += 1
        return df.fillna(0)

    def fit(self, corpus):
        #Create list of words within a list of lines
        lines = lp.corpus2lines(corpus)

        print "Transforming"
        df = self.transform(lines)
        X, y = df.drop('label',axis=1).values, df['label'].values

        print "Tuning"
        #Random Forrest
        clf = RandomForestClassifier()

        # specify parameters and distributions to sample from
        param_dist = {'n_estimators': sp_randint(10,100),
                      "max_depth": [3, None],
                      "max_features": sp_randint(1, 11),
                      "min_samples_split": sp_randint(1, 11),
                      "min_samples_leaf": sp_randint(1, 11),
                      "bootstrap": [True, False],
                      "criterion": ["gini", "entropy"]}

        # run randomized search
        n_iter_search = 20
        random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                           n_iter=n_iter_search)

        random_search.fit(X, y)

        print "Fitting"
        self.model = RandomForestClassifier(**random_search.best_params_)
        self.model.fit(X,y)

    def predict(self, X):
        return self.model.predict(X)


    def savemodel(self):
        with open(project_dir + '/data/POS_model.pkl', 'w') as f:
            pickle.dump(self.model, f)
