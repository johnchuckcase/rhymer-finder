from flask import Flask, request, jsonify, render_template
from datetime import date
from pymongo import MongoClient
import rhymer_finder
import os
import cPickle as pickle
app = Flask(__name__)
import logging

logging.info("Print works")
#Find parent directory of this script
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print "Loading Corpus"
with open(project_dir + '/data/corpus.pkl','r') as f:
    corpus = pickle.load(f)

print "Loading Rhyming Dictionary"
rhymer = rhymer_finder.rhymer_finder()
rhymer.process_corpus(corpus)

print "Loading W2V"
with open(project_dir + '/data/w2v.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

print "Ready"

# home page
@app.route('/')
# def index():
#     return '''<script   src="https://code.jquery.com/jquery-1.12.1.min.js"   integrity="sha256-I1nTg78tSrZev3kjvfdM5A5Ak/blglGzlaZANLPDl3I="   crossorigin="anonymous"></script>
#     <link rel='stylesheet' href='static/stylesheet.css'>
#     <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">
#     <script src='static/shcriptsh.js'></script>
#     <br>
#     <center>
#     <div id='input-div'>
#     <form class="pure-form" style="display: inline">
#     <input type="email" id="lyric-input" placeholder="Enter Lyrics" class="input-form";
# " size=50>
#
#     </div>
#     <div id='block-space'></div>
#     <div id='rhymes-space'></div>
#     </center>'''
def index():
     return render_template('rhymerfinder.html',name=None)


@app.route('/rhyme', methods=["GET"])
def rhyme():

    word_to_rhyme = request.args.get('word_to_rhyme', 0, type=str)
    words = request.args.get('words',type=str).split(',')

    return jsonify(rhymer.find_rhyme(word_to_rhyme.lower(), words))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
