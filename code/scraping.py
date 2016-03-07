# Import library to read urls
from urllib2 import urlopen
import requests
# Import library to parse html
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import re
import pandas as pd
import numpy as np
import re
import time

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

client = MongoClient()
# Access/Initiate Database
db = client['rap_db']
# Access/Initiate Table
tab = db['lyrics']

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

with open('scrap_log','w') as f:

    for artist in artists:

        artist_dir = project_dir + '/data/html/' + artist

        #Gather all song links for particular artist
        if not os.path.exists(artist_dir):
            os.makedirs(artist_dir)

        #50-cent's url is lyrics/19/50-cent for some reason
        if artist[0].isdigit():
            url = 'http://www.azlyrics.com/19/' + artist + '.html'
        else:
            url = 'http://www.azlyrics.com/' + artist[0] + '/' + artist + '.html'

        #Get the url for every song by artist
        content = urlopen(url).read()

        #Save raw html to file
        with open(artist_dir + '/url_page.html','w') as home_f:
            home_f.write(content.decode('utf-8').encode('ascii', 'ignore'))

        #Feed the html to a BeatifulSoup object
        soup = BeautifulSoup(content,'lxml')

        #Parse out the song url tags
        els = soup.find(id='listAlbum')

        #Do not include song lyrics from "non-rap" songs or repeats (e.g., remixes)
        stop_strings = ['intro','skit','interlude','remix']

        #Parse out urls for artist
        urls = [x['href'][2:] for x in els.find_all(target='_blank') if not any(substr in x.contents[0].lower() for substr in stop_strings)]

        time.sleep(np.random.randint(10,20))

        #Loop over all songs for artist
        for i, url in enumerate(urls):

            print i, url

            try:
                # Go to the link and get the html as a string
                headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6)"}
                r = requests.get('http://www.azlyrics.com/' + url, headers=headers)

                # Feed the html to a BeatifulSoup object
                soup = BeautifulSoup(r.content, 'lxml')

                #Lyrics from Webpage
                rows = soup.find('div',{'class':'col-xs-12 col-lg-8 text-center'})
                rows = rows.find('div',{'class':''})
                lyrics = rows.text

                #Strip trailing whitespaces and unicode madness
                lyrics = lyrics.strip().encode('ascii','ignore')

                #Get year / album
                year_album = str(soup.find('div',{'class':'panel album-panel noprint'}).text.strip())
                album = year_album.split('"')[1]
                year = year_album.split('"')[2].strip().translate(None,'()')

                #Get Song Name
                song = re.split('\.|/',url)[-2]

                #Add lyrics and meta-info to database
                tab.insert_one({'artist':artist, 'url':url, 'lyrics':lyrics, 'song':song, 'album':album, 'year':year})

                #Log Lyric Download
                f.write(artist + ' - ' + song)

                #Save raw html to file
                with open(artist_dir + '/' + song + '.html','w') as home_f:
                    home_f.write(r.content.decode('utf-8').encode('ascii', 'ignore'))

                #Sleep a random amount of time between requests. Every 5, sleep more.
                time.sleep(np.random.randint(10,20) + np.random.rand())
                if i % 5 == 0:
                    time.sleep(np.random.randint(10,20) + np.random.rand())

            except:
                print("Error: " + artist + " - " + song)
                f.write("Error: " + artist + " - " + song)
        # except:
        #     print("Error artist song scrape: " + artist)
        #     f.write("Error artist song scrape: " + artist)
