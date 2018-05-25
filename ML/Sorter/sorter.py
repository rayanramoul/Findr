from sklearn import svm
import pickle
from nltk import word_tokenize
import pipes
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from string import punctuation
# 1 = CONFIG 
# 0 = NON CONFIG
import zipfile
from BackEnd.Document import Document
import textract
import os

import rarfile
import libarchive.public


class sorter:
    def __init__(self):
            self.modal=pickle.load(open(os.path.join('ML','Sorter','modals','configus'), 'rb'))
            self.vect=pickle.load(open(os.path.join('ML','Sorter','modals','vect'), 'rb'))
            self.ti=pickle.load(open(os.path.join('ML','Sorter','modals','tfidf'), 'rb'))


    def tfidf(self, entry1, entry2=None, entry3=None, tidf=True): # For initial Fit
        if entry2!=None:
            entry=entry1+entry2
        else:
            entry=entry1
        if entry3!=None:
            entry=entry+entry3
        x=self.vect.fit_transform(entry)
        if tidf==True:
            x = self.ti.fit_transform(x)
        self.save()
        return x

    def tfidfer(self, entry1, entry2=None, tidf=True): # To Apply on new Documents
        if entry2!=None:
            entry=entry1+entry2
        else:
            entry=entry1
        x=self.vect.transform(entry)
        if tidf==True:
            x = self.ti.transform(x)
        self.save()
        return x

    def counter(self,entry): # Implementation of CountVectorizer()
        x=self.vect.fit_transform(entry)
        X_train_tfidf = self.ti.fit_transform(entry)
        self.save()
        return X_train_tfidf.toarray()[1]

    def save(self):     # Saving all the Modals
        pickle.dump(self.modal,open(os.path.join('modals','configus'),'wb'))
        pickle.dump(self.vect,open(os.path.join('modals','vect'),'wb'))
        pickle.dump(self.ti,open(os.path.join('modals','tfidf'),'wb'))


    def extract(self, text):
        # Feature1 : len(text)
        # Feature2 : len(set(tokenized(text)))
        text=text.lower()
        print('extracting text')
        tk=word_tokenize(text)
        print('tokenizing')
        f2=len(set(tk))
        # Feature3 : number of #
        print('counting')
        f3=text.count('#')
        # Feature4 : number of enable and disabled
        f4=text.count('enabled')+text.count('disabled')+text.count('enable')+text.count('disable')
        # Feature5 : number of 1 or 0
        f5=text.count('0')+text.count('1')
        # Feature6 : number of True False
        f6=text.count('true')+text.count('false')
        # Feature7 : punctuation
        f7=0
        for i in punctuation:
            f7=f7+text.count(i)
        ff=f3+f4+f5+f6+f7
        return len(text),f2,ff

    def transform(self, directory):  # Return a list of all the contents of documents in a directory
        mat=[]
        for path, subdirs, files in os.walk(directory):
            for name in files:
                try:
                    r=open(os.path.join(path, name),'r')
                    text=r.read()
                    mat.append(text)
                    r.close()
                except:
                    pass
        return mat

    def loadmodal(self):
        return pickle.load(open(os.path.join('modals','configus'), 'rb'))

    def predict(self,document):
        m=self.modal
        print('\nLet\'s predict ! \n')
        l=[]
        l.append(self.extract(document))
        return m.predict(l)


    def find_mime_with_file(self,path):
        filename = pipes.quote(path)
        try:
            return os.popen(r"/usr/bin/file -i {0}".format(filename)).read()
        except:
            import magic
            mime = magic.Magic(mime=True)
            return mime.from_file(path
                                  )
    def majority(self, l):
        return max(l,key=l.count)

    def createdocument(self,path,name):
        origin=" "
        d=False
        typo=str(self.find_mime_with_file(path))
        if True:
            if 'document' in typo or 'pdf' in typo:
                try:
                    origin = textract.process(path,encoding='utf-8').decode('utf-8')
                except:
                    pass
                d=True
            if d is False:
                if zipfile.is_zipfile(path):
                    zip=zipfile.ZipFile(path,'r')
                    predictions=[]
                    for i in zip.namelist():
                        r=zip.open(i,'r').read()
                        predictions.append(Document(path,r,i))
                    categories=[]
                    languages=[]
                    for j in predictions:
                        languages.append(j.language)
                        categories.append(j.category)
                    catfinal=str(self.majority(categories))
                    langfinal=str(self.majority(languages))
                    return Document(path, r, name, type=catfinal, language=langfinal)
                if rarfile.is_rarfile(path):
                    zip=rarfile.RarFile(path,'r')
                    predictions=[]
                    for i in zip.namelist():
                        try:
                            r=zip.open(i,'r').read()
                            predictions.append(Document(path,r,i))
                        except:
                            pass
                    categories=[]
                    languages=[]
                    for j in predictions:
                        languages.append(j.language)
                        categories.append(j.category)
                    catfinal=str(self.majority(categories))
                    langfinal=str(self.majority(languages))
                    return Document(path, r, name, type=catfinal, language=langfinal)
                if path.endswith('.7z'):
                    with open(path, 'rb') as f:
                        predictions=[]
                        for entry in libarchive.public.memory_pour(f.read()):
                            try:
                                predictions.append(Document(path, entry, entry.name))
                            except:
                                pass
                        categories = []
                        languages = []
                        for j in predictions:
                            languages.append(j.language)
                            categories.append(j.category)
                        catfinal = str(self.majority(categories))
                        langfinal = str(self.majority(languages))
                        return Document(path, r, name, type=catfinal, language=langfinal)
                if 'image' in typo:
                    return Document(path,'',name,'Img')
                if 'audio' in typo:
                    return Document(path,'',name,'Aud')
                if 'video' in typo:
                    return Document(path,'',name,'Vid')
                if typo=="text/plain":
                    origin = open(path, 'r').read()
                    if self.predict(origin) == 1:
                        return None
                    else:
                        origin = open(path, "r").read()
            return Document(path,origin,name)

        else:
            print('Can\'t open file '+path+'\n')
            return
