#Scrape the song urls for each artist and save them to "urls.txt"
import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import numpy as np
import time

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Users to randomly cycle through for each request
user_agents = ["Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6)",
                "Gecko/20070725 Firefox/2.0.0.6",
                "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            	"Opera/9.00 (Windows NT 5.1; U; en)"
                "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3",
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

#Save the urls for the songs by all artists into one file
for artist in artists:

    print "Getting URLS for", artist
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
    headers = {"User-Agent":np.random.choice(user_agents)}
    req = requests.get(url, headers=headers)

    #Save raw html to file
    with open(artist_dir + '/url_page.html','w') as home_f:
        home_f.write(req.content.decode('utf-8').encode('ascii', 'ignore'))

    #Feed the html to a BeatifulSoup object
    soup = BeautifulSoup(req.content,'lxml')

    #Parse out the song url tags
    els = soup.find(id='listAlbum')

    #Do not include song lyrics from "non-rap" songs or repeats (e.g., remixes)
    stop_strings = ['intro','skit','interlude','remix']

    #Parse out urls for artist
    urls = [x['href'][2:] for x in els.find_all(target='_blank') if not any(substr in x.contents[0].lower() for substr in stop_strings)]

    #Append urls to list of urls for all artists
    with open(project_dir + '/data/html/urls.txt','a') as urls_f:
        for url in urls:
            urls_f.write("%s\n" % url)

    time.sleep(np.random.randint(10,20))
