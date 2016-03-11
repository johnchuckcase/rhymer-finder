from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
import random
import lyrics_preprocessing as lp

# 84.23.107.195:8080

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

rhyme_dict = lp.create_rhyme_dict(tab = tab, artist = None)
pos_dict = lp.create_pos_dict(tab = tab, artist = None)
test_data = lp.create_test_data(corpus)

print lp.baseline_accuracy(test_data,rhyme_dict)
