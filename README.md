# RhymerFinder
RhymerFinder predicts the rhymes in a song based on preceding lyrics by using gensim's Word2Vec implementation.
[See my blog post for details.](http://johnchuckcase.com/rhymerfinder/)

##Installation
`python setup.py install`

##Accuracy Metrics
`python rhymerfinder/run.py`

##Scraping
The lyrics corpus is provided in data/corpus.pkl.
However, if you would like to re-scrape the lyrics into a Mongo database run the following:

To scrape the song URLs for each artist (outputed into data/html/urls.txt):

```python rhymerfinder/scrape_artists.py```

To scrape the HTML source, parse the lyrics, and store them using MongoDB (HTML source outputed to data/html/[artist name]):

```python rhymerfinder/scrape_songs.py```

##Rhyme Your Own Lyrics
You can also use RhymerFinder to rhyme your own lyrics at the iPython command line (replicating the behavior of [rhymerfinder.com](https://www.rhymerfinder.com)).

First, train a rhymerfinder object:
```
import rhymer_finder
import cPickle as pickle

#Initialize rhymer_finder object
rhymer = rhymer_finder.rhymer_finder()

print "Loading Corpus..."
with open('./data/corpus.pkl','r') as f:
    corpus = pickle.load(f)

print "Loading W2V..."
with open('./data/w2v.pkl','r') as f:
    rhymer.load_w2v(pickle.load(f))

print "Creating Rhyming Dictionary..."
rhymer.process_corpus(corpus)
```
Now you can use the "find_rhyme" method like so:
```rhymer.find_rhyme(Lyrics, Word_to_Rhyme)```

For example,
```
rhymer.find_rhyme('You will see him on tv any given sunday win the superbowl and drive off in a','sunday')
      Cos-sim     Rhymes
0      0.41    hyundai
1      0.39      andre
2      0.37   driveway
3      0.35        ave
...    ...        ...
```
