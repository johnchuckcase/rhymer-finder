# Import library to read urls
from urllib2 import urlopen
# Import library to parse html
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import pandas as pd
import numpy as np
import re
import time


client = MongoClient()
# Access/Initiate Database
db = client['rap_db']
# Access/Initiate Table
tab = db['lyrics']


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

    #Gather all song links for particular artist

        if artist[0].isdigit():
            url = 'http://www.azlyrics.com/19/' + artist + '.html'
        else:
            url = 'http://www.azlyrics.com/' + artist[0] + '/' + artist + '.html'

        try:
            content = urlopen(url).read()
            # Feed the html to a BeatifulSoup object
            soup = BeautifulSoup(content)
            els = soup.find(id='listAlbum')

            #Do not include song lyrics from "non-rap" songs or repeats (e.g., remixes)
            stop_strings = ['intro','skit','interlude','remix']

            #Parse out urls
            urls = [x['href'][2:] for x in els.find_all(target='_blank') if not any(substr in x.contents[0].lower() for substr in stop_strings)]
            for i, url in enumerate(urls):

                print i, url

                try:
                    # Go to the link and get the html as a string
                    content = urlopen('http://www.azlyrics.com/' + url).read()
                    # Feed the html to a BeatifulSoup object
                    soup = BeautifulSoup(content)

                    # Extract the rows in the table
                    rows = soup.find('div',{'class':'col-xs-12 col-lg-8 text-center'})
                    rows = rows.find('div',{'class':''})
                    text = rows.text

                    time.sleep(5)
                    time.sleep(np.random.rand()*10)

                    if i % 5 == 0:
                        time.sleep(10)
                        time.sleep(np.random.rand()*10)

                    lyrics = ''
                    for t in a:
                        if len(t) > 100:
                            lyrics = lyrics + t.strip().encode('ascii','ignore')

                    #Get year / album
                    year_album = str(soup.find('div',{'class':'panel album-panel noprint'}).text.strip())
                    album = year_album.split('"')[1]
                    year = year_album.split('"')[2].strip().translate(None,'()')

                    #Song Name
                    song = re.split('\.|/',url)[-2]

                    tab.insert_one({'artist':artist, 'url':url, 'lyrics':lyrics, 'song':song, 'album':album, 'year':year})

                    f.writelines(artist + ' - ' + song)
                except:
                    f.writelines("Error: " + artist + " - " + song)
        except:
            f.writelines("Error artist song scrape: " + artist)
