from flask import Flask, request, jsonify, render_template
import json
from datetime import date
from pymongo import MongoClient
import rhymer_finder
import os
import cPickle as pickle
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('rhymerfinder.html',name=None)

@app.route('/rhyme', methods=["GET"])
def rhyme():

    word_to_rhyme = request.args.get('word_to_rhyme', 0, type=str)
    words = request.args.get('words', type=str).split(',')

    try:
        return jsonify(rhymer.find_rhyme(words, word_to_rhyme.lower()).to_dict('list'))
    except:
        return jsonify({"Rhymes": [], "Cos-sim": []})

if __name__ == '__main__':

    # Find parent directory of this script
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # "Loading Corpus"
    with open(project_dir + '/data/corpus.pkl', 'r') as f:
        corpus = pickle.load(f)

    # "Loading Rhyming Dictionary"
    rhymer = rhymer_finder.rhymer_finder()
    rhymer.process_corpus(corpus)

    # "Loading W2V"
    with open(project_dir + '/data/w2v.pkl', 'r') as f:
        rhymer.load_w2v(pickle.load(f))

    # "Ready"
    app.run(host='0.0.0.0', port=8000, debug=True)
