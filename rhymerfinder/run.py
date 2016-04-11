from pymongo import MongoClient
from bson import BSON, decode_all
import pandas as pd
import numpy as np
import re
import nltk
import string
import random
import rhymer_finder
import cPickle as pickle
import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print "Loading Corpus..."
#LOAD Corpus from BSON
# client = MongoClient()
# target_collection = client.rap_db_new.lyrics
# with open('../data/lyrics.bson', 'rb') as f:
#     target_collection.insert(decode_all(f.read()))

#Load Corpus from MongoDB
# Access Database and Table
# db = client['rap_db']
# tab = db['lyrics']
#corpus = list(set([song['lyrics'] for song in tab.find()]))

#Load Corpus from pickle
with open(project_dir + '/data/corpus.pkl','r') as f:
    corpus = pickle.load(f)


print "Loading W2V..."
with open(project_dir + '/data/w2v.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

#Initialize rhymer_finder object
rhymer = rhymer_finder.rhymer_finder()

print "Creating Rhyming Dictionary..."
rhymer.process_corpus(corpus)



print "Creating Test Data..."
test_data = rhymer.create_test_data(corpus)

print "Assessing Model Accuracy..."
rhymer.accuracy(test_data)

print "Done"
