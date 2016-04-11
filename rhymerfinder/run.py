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

#Load Mongo Database
client = MongoClient()
target_collection = client.rap_db.lyrics
with open('../data/lyrics.bson', 'rb') as f:
    target_collection.insert(decode_all(f.read()))

# Access Database and Table
db = client['rap_db']
tab = db['lyrics']

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

rhymer = rhymer_finder.rhymer_finder()

print "Creating Rhyming Dictionary..."
rhymer.process_corpus(corpus)

print "Loading W2V..."
with open(project_dir + '/data/w2v.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

print "Creating Test Data..."
test_data = rhymer.create_test_data(corpus)

print "Assessing Model Accuracy..."
rhymer.accuracy(test_data)

print "Done"
