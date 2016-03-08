import re
import string
from num2words import num2words

#Change numbers into words
def spell_out_num(st):
    st = st.group(0) #Expects a regex return object
    num = int(st)
    if num <= 100:
        return num2words(num).replace('-',' ')
    else:
        return st #Deal with 'one thousand, nine hundred and ninety-nine' cases later

def lyrics2words(lyrics):
    lyrics = re.sub('\[.*\]',' ',lyrics) #Get rid of block titles (e.g., [Verse 1], [Chorus])
    lyrics = re.sub('\(|\)','',lyrics)   #Get rid of words in parentheses
    lyrics = re.sub('[0-9]+',spell_out_num,lyrics) #Spell out numbers
    lyrics = re.sub('[A-Z]{2,}',lambda x: ' '.join(x.group(0)),lyrics) #Space out acronoyms
    lyrics = lyrics.lower()
    lyrics = lyrics.translate(dict.fromkeys(map(ord, string.punctuation))) #unicode translate out punctuation
    return lyrics.split()
