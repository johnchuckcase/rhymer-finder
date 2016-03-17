from flask import Flask, request
from datetime import date
from pymongo import MongoClient
import rhymer_finder

app = Flask(__name__)

# Access Database and Table
client = MongoClient()
db = client['rap_db']
tab = db['lyrics']

#Retrieve all lyrics
corpus = list(set([song['lyrics'] for song in tab.find()]))

rhymer = rhymer_finder.rhymer_finder()
rhymer.process_corpus(corpus)

# home page
@app.route('/')
def index():
    print rhymer
    return '''<script   src="https://code.jquery.com/jquery-1.12.1.min.js"   integrity="sha256-I1nTg78tSrZev3kjvfdM5A5Ak/blglGzlaZANLPDl3I="   crossorigin="anonymous"></script>
    <link rel='stylesheet' href='static/stylesheet.css'>
    <script src='static/shcriptsh.js'></script>
    <form>
  Line 1<br>
  <input type="text" id="lyric-input" name="line1">Lyric</input><br>
</form><div id='block-space'></div><div id='rhymes-space'></div>'''

@app.route('/rhyme', methods=["GET"])
def rhyme():
    return '''RAWR'''



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
