from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from nltk.stem.porter import *
from nltk.stem.isri import *
from nltk.stem.snowball import FrenchStemmer
from ML.Categorization.categorizer import categorizer
from NLP.detect import detect
import chardet
import re
import os
import magic
import time

class Document:
    def __init__(self, path, text,name,type=None,language=None):
        # initialisation du document et analyse de l'extension
        origin=" "
        self.justname=name
        self.visible=False
        self.name=path
        try:
            self.text=self.transform(text)
        except:
            self.text=str(text)
        self.type=""
        if language is None:
            self.language=detect(text)
        else:
            self.language=language

        if self.language=='unknown':
            self.language='english'
        if type is None:
            cat = categorizer(self.language)
            self.category = str(cat.predict(self.text))
        elif type in ['Img','Vid','Aud']:
            self.category=type
        else:
            self.category=type
        self.tags=[]
        self.tokens=[]
        self.tok=word_tokenize(self.text)

        if self.language=='english':
            ps = PorterStemmer()
        elif self.language=='french':
            ps=FrenchStemmer()
        elif self.language=='arabic':
            ps=ISRIStemmer()

        for i in self.tok:
            self.tokens.append(ps.stem(i.lower()))
        self.score=0
        try:
            self.addtag(time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(self.name))))
        except:
            self.addtag(time.strftime('%d/%m/%Y', time.gmtime(os.path.getctime(self.name))))
#        self.addtag(self.justname)
        mime = magic.Magic(mime=True)
        if os.path.isdir(self.name):
            self.addtag('Folder')
        else:
            typ=mime.from_file(self.name)
            self.addtag(typ)
    def setcategory(self,cat):
        self.category=cat

    def text(self):
        return self.text

    def transform(self,text):
        d=''
        i=0
        bool=True
        text=text.replace('\n',' ')
        text=text.replace('\t',' ')
        for i in range(len(text)):
            if text[i]=='\\':
                i=i+1
                while text[i]!=' ':
                    i=i+1
            else:
                d=d+text[i]
        return d


    def addtag(self,tag):
        self.tags.append(tag)

    def deletetag(self):
        pass

    def tostemmed(self):
        self.totokens()
        self.textStemmed=' '.join(self.tokens)

    def totokens(self):
        voids=stopwords.words('english')
        org=word_tokenize(self.text)
        final=[]
        ponct=(set(punctuation))
        for word in org:
            if word not in voids and word not in ponct:      # On peut réecrire un mot des qu'il n'est pas un mot vide ou un caractère special
                final.append(PorterStemmer().stem(word))

        self.tokens=final
