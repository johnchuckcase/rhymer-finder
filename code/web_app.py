from flask import Flask, request, jsonify
from datetime import date
from pymongo import MongoClient
import rhymer_finder
import os
import cPickle as pickle
app = Flask(__name__)


#Find parent directory of this script
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


print "Loading Rhyming / POS Dictionary"
with open(project_dir + '/data/rhymer.pkl','r') as f:
    rhymer = pickle.load(f) #Rhyming dictionary / POS dictionary

print "Loading W2V"
with open(project_dir + '/data/w2v_all.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

print "Ready"

# home page
@app.route('/')
def index():
    return '''<script   src="https://code.jquery.com/jquery-1.12.1.min.js"   integrity="sha256-I1nTg78tSrZev3kjvfdM5A5Ak/blglGzlaZANLPDl3I="   crossorigin="anonymous"></script>
    <link rel='stylesheet' href='static/stylesheet.css'>
    <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">
    <script src='static/shcriptsh.js'></script>
    <br>
    <center>
    <form class="pure-form">
    <input type="email" id="lyric-input" placeholder="Enter Lyrics" size="50">
    </form>
    <div id='block-space'></div>
    <div id='rhymes-space'></div>
    </center>'''

@app.route('/rhyme', methods=["GET"])
def rhyme():

    word_to_rhyme = request.args.get('word_to_rhyme', 0, type=str)
    words = request.args.get('words',type=str).split(',')

    return jsonify(rhymer.find_rhyme(word_to_rhyme.lower(), words))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
