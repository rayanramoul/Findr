from nltk.corpus import stopwords
from nltk import word_tokenize
import operator

def detect(text):
    text=str(text)
    fr=stopwords.words('french')
    ar=stopwords.words('arabic')
    en=stopwords.words('english')
    org = word_tokenize(text)
    lang={}
    lang['french']=0
    lang['english']=0
    lang['arabic']=0

    for i in en:
        if i in org:
            lang['english']=lang['english']+1
    for i in ar:
        if i in org:
            lang['arabic']=lang['arabic']+1
    for i in fr:
        if i in org:
            lang['french'] = lang['french'] + 1
    return max(lang.items(), key=operator.itemgetter(1))[0]
