#Scrape song lyrics for each url in "url.txt" (created in scrape_artist.py)

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import pandas as pd
import numpy as np
import re
import time

client = MongoClient()
# Access/Initiate Database
db = client['rap_db']
# Access/Initiate Table
tab = db['lyrics']

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Users to randomly cycle through for each request
user_agents = ["Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6)",
                "Gecko/20070725 Firefox/2.0.0.6",
                "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            	"Opera/9.00 (Windows NT 5.1; U; en)"
                "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3",
                "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
                "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, Like Gecko) Version/6.0.0.141 Mobile Safari/534.1+",
                'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']


artists = ['dmx','toohort','pablo','masterp','50cent','drake','bone','saltnpepa',\
           'juvenile','youngjeezy','wizkhalifa','lilb','lilwayne','guccimane','missy',\
           'west','rundmc','ugk','snoopdogg','jadakiss','scarface','icp','nickiminaj',\
          'three6mafia','getoboys','ti','camron','bizmarkie','icecube','nelly','game',\
          'lupefiasco','lilkim','jayz','clipse','icet','puffdaddy','royceda59','eminem',\
          'cypress','krsone','mosdef','rakim','tribecalledquest','tyga','fatjoe',\
          'publicenemy','kweli','brotherali','twista','llcoolj','mobbdeep','ludacris',\
           'gangstarr','goodiemob','techn9ne','busta','wale','delasoul','methodman',\
          'common','raekwon','xzibit','beastie','nas','outkast','e40','blackalicious',\
          'redman','ghostface','roots','wutang','rza','canibus','gza','aesoprock',\
          'jcole','kendricklamar']

#Get the list of already scraped urls
if os.path.exists(project_dir + '/data/html/already_scraped_urls.txt'):
    with open(project_dir + '/data/html/already_scraped_urls.txt','r') as urls_f:
        already_scraped = [url.strip() for url in urls_f]
else:
    already_scraped = []

#Get the list of total urls and exclude any that have already been scraped
with open(project_dir + '/data/html/urls.txt','r') as urls_f:
    urls = [url.strip() for url in urls_f if url[:7] == '/lyrics' and not url in already_scraped]

#Randomize URLS for more covert scraping
np.random.shuffle(urls)

#Loop over all songs for artist
for i, url in enumerate(urls):
    try:
        print i, url

        # Go to the link and get the html as a string
        headers = {"User-Agent":np.random.choice(user_agents)}
        req = requests.get('http://www.azlyrics.com/' + url, headers=headers)

        # Feed the html to a BeatifulSoup object
        soup = BeautifulSoup(req.content, 'lxml')

        #Lyrics from Webpage
        rows = soup.find('div',{'class':'col-xs-12 col-lg-8 text-center'})
        rows = rows.find('div',{'class':''})
        lyrics = rows.text

        #Strip trailing whitespaces and unicode madness
        lyrics = lyrics.strip().encode('ascii','ignore')

        #Get year / album from bottom of page
        if soup.find('div',{'class':'panel album-panel noprint'}):
            year_album = str(soup.find('div',{'class':'panel album-panel noprint'}).text.strip())
            album = year_album.split('"')[1]
            year = year_album.split('"')[2].strip().translate(None,'()')
        else:
            album = ''
            year = ''

        #Get Song and Artist Name from URL
        song = re.split('\.|/',url)[-2]
        artist = url.split('/')[2]
        artist_dir = project_dir + '/data/html/' + artist

        #Add lyrics and meta-info to database
        tab.insert_one({'artist':artist, 'url':url, 'lyrics':lyrics, 'song':song, 'album':album, 'year':year})

        #Save raw html to file
        with open(artist_dir + '/' + song + '.html','w') as home_f:
            home_f.write(req.content.decode('utf-8').encode('ascii', 'ignore'))

        #Note that the url has been scraped
        with open(project_dir + '/data/html/urls_already_scraped.txt','a') as urls_f:
            urls_f.write("%s\n" % url)

        #Sleep a random amount of time between requests. Every 5, sleep more.
        time.sleep(np.random.randint(20,30) + np.random.rand())
        if i % 5 == 0:
            time.sleep(np.random.randint(20,30) + np.random.rand())

    except:
        print("Error: " + artist + " - " + song)
