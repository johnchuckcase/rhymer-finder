from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
import random
import rhymer_finder
import cPickle as pickle

# 84.23.107.195:8080

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

project_dir = '/Users/johncase/Galvanize/rhymerfinder'

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

rhymer = rhymer_finder.rhymer_finder()
rhymer.process_corpus(corpus)

print "Loading W2V"
with open(project_dir + '/data/w2v_all.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

test_data = rhymer.create_test_data(corpus)
print rhymer.accuracy(test_data)

#
# print "Loading Rhyming / POS Dictionary"
# with open(project_dir + '/data/rhymer.pkl','r') as f:
#     rhymer = pickle.load(f) #Rhyming dictionary / POS dictionary
#
# print "Loading W2V"
# with open(project_dir + '/data/w2v_all.pkl','r') as f:
#     rhymer.load_w2v(pickle.load(f))
#
# print "Ready"
