# Import library to read urls
from urllib2 import urlopen
# Import library to parse html
from bs4 import BeautifulSoup
import pandas as pd
import re
# Go to the link and get the html as a string
# content = urlopen('http://www.azlyrics.com/lyrics/jcole/letnasdown.html').read()
content = urlopen('http://www.azlyrics.com/lyrics/nas/nystateofmind.html').read()
# Feed the html to a BeatifulSoup object
soup = BeautifulSoup(content)

# Extract the rows in the table
rows = soup.find('div',{'class':'col-xs-12 col-lg-8 text-center'})
rows = rows.find('div',{'class':''})
text = rows.text
a = re.split(r'\[?\:?]?',text)
