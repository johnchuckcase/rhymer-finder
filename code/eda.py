from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
import nltk
import string
import random
import rhymer_finder

# 84.23.107.195:8080

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

rhymer = rhymer_finder.rhymer_finder()
rhymer.process_corpus(corpus)

test_data = rhymer.create_test_data(corpus)
print rhymer.accuracy(test_data)
