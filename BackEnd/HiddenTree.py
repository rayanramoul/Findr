from BackEnd.VisibleTree import VisibleTree
from BackEnd.Node import Node
from ML.Sorter.sorter import sorter
import os
from nltk import word_tokenize
from nltk.stem.porter import *
import pickle
from BackEnd.Document import Document
import numpy as np
from scipy.sparse import coo_matrix, hstack, vstack
from nltk import word_tokenize
from nltk.corpus import stopwords
from BackEnd.Config import Config
import getpass
import operator
from sklearn.metrics.pairwise import cosine_similarity
import pipes

class HiddenTree(VisibleTree):
    def __init__(self):
        self.user=getpass.getuser()
        self.documents = []
        self.nodes = {}
        self.favoris=[]

        if not os.path.isdir('profile'):
            os.mkdir('profile')
        self.recents=[]
        self.highlighted=[]
        load=open(os.path.join('resources','hiearch'),'r')
        r=load.read().splitlines()

        dom = open(os.path.join('resources','equivalents'), 'r').read().splitlines()
        d=[]
        self.equivalents={}
        self.equivalents['français']={}
        self.equivalents['العربية']={}
        self.equivalents['english']={}
        for bouch in dom:
            s=bouch.split(':')
            self.equivalents['العربية'][s[0]]=s[2]
            self.equivalents['français'][s[0]]=s[1]
            self.equivalents['english'][s[0]]=s[0]


        om = open(os.path.join('resources','equivalents'), 'r').read().splitlines()
        for bi in dom:
            bi.split(':')
        for i in r:
            d.append(i.split(':'))
        self.hiearchy={}
        self.enhiearchy={}
        self.categories=[]
        self.keys={}
        self.configuration=Config()
        language=str(self.configuration.language).lower()
        self.language=language
        for x in d:
            trad=[]
            origin=[]
            for i in x[1].split(','):
                if i!='':
                    trad.append(self.equivalents[language][i])
                    origin.append(i)
            try:
                self.enhiearchy[x[0]]=origin
                self.hiearchy[self.equivalents[language][x[0]]]=trad
                self.categories.append(self.equivalents[language][x[0]])
            except:
                self.hiearchy[self.equivalents[language][x[0]]]=trad
                self.categories.append(self.equivalents[language][x[0]])
        for i in self.categories:
            self.nodes[str(i)]=Node(str(i),self)

        for j in self.hiearchy:
            for y in self.hiearchy[j]:
                if y!='':
                    self.nodes[j].addkid(self.nodes[y])
        progs = ['.c', '.html', '.cpp', '.py', '.perl', '.java', '.css', '.php', '.js', '.css', '.sh', '.bash']
        self.projets={}
        for i in progs:
            self.projets[i]=[]
        if os.path.isfile(os.path.join('profile','documents')):
            self.load()

    def initialize(self,directory):
        progs=['.c','.html','.cpp','.py','.perl','.java','.css','.php','.js','.css','.sh','.bash']

        for path, subdirs, files in os.walk(directory):
            d=False

            for name in files:
                file = os.path.join(path, name)
                if '/.' not in file:
                    for x in progs:
                        if name.endswith(x):
                            tmp={}
                            noup=0
                            print('NAME:'+str(file))
                            limit=str(os.path.dirname(file))
                            print('limit : '+str(limit))
                            d=True
                            for path, subdirs, files in os.walk(limit):
                                for name in files:
                                    bich=False
                                    stro = str(os.path.join(path, name))
                                    for i in progs:
                                        if stro.endswith(i):
                                            try:
                                                tmp[i]=tmp[i]+1
                                                bich=True
                                            except:
                                                tmp[i]=0
                                                tmp[i] = tmp[i] + 1
                                                bich=True
                                    if not bich:
                                        noup=noup+1
                            indice=''
                            maximum=noup
                            for i in tmp:
                                if tmp[i]>maximum:
                                    indice=i
                                    maximum=tmp[i]

                            test=False
                            print('NOUP : '+str(noup))
                            print('TMP : '+str(tmp))

                            for i in self.projets:
                                for j in self.projets[i]:
                                    if limit.startswith(j.justname):
                                        test=True
                            if test is False and indice!='':
                                di = Document(limit, '', limit, type=indice, language=None)
                                self.projets[x].append(di)

                    if not d:
                        if self.contains(file)==False:
                            self.add(file,name)



    def search(self,text):
        lis={}
        text=str(text)
        if str(text) in self.categories:
            lis['Categories']=self.nodes[self.equivalents[self.language][str(text)]].getsubdocs()
        ps = PorterStemmer()
        origin = word_tokenize(str(text))
        hx=self.gettags()
        lis['Tags']=[]
        for i in hx:
            for j in origin:
                for d in hx[i]:
                    if j.lower() in i.lower():
                        lis['Tags'].append(d)

        lis['Documents']=[]
        intermediaire={}
        for d in self.keys:
            for r in origin:
                if ps.stem(r.lower())==d or r.lower()==d.lower():
                    for i in self.keys[d]:
                        try:
                            intermediaire[i]=intermediaire[i]+i.text.count(str(r))

                        except:
                            intermediaire[i]=0
                            intermediaire[i]=intermediaire[i]+i.text.count(str(r))

        sorted_x = dict(sorted(intermediaire.items(), key=operator.itemgetter(1)))
        lise=[]
        for i in sorted_x:
            lise.append(i)
        lis['Documents']=lise
        for d in self.documents:
            if text.lower() in d.justname.lower():
                lis['Documents'].append(d)
        d=lis
        return d

    def contains(self,path):
        for i in self.documents:
            if i.name==path:
                return True
        return False

    def moyenne(self,list):
        count=0
        total=0

        for i in range(1,len(list)):
            if True:
                total=total+list[i]
                count=count+1
        try:
            return total/count
        except:
            return 0

    def hillclimbing(self,vect,ti,totals,doc,cat,lise):
        lise.append(cat)
        winner=cat

        try:
            x=totals[cat].mean(axis=0)
            train=[doc]+totals[cat]
            x=vect.transform(train)
            tfi = ti.transform(x)
            tmp=cosine_similarity(tfi[0:1], tfi)
            min=self.moyenne(tmp[0])
        except:
            min=0

        if len(self.enhiearchy[cat])!=0:
            for i in self.enhiearchy[cat]:
                if True:
                    train = [doc] + totals[i]
                    x = vect.transform(train)
                    tfi = ti.transform(x)
                    mor=cosine_similarity(tfi[0:1],tfi)
                    d=self.moyenne(mor[0])
                    if d>min:
                        min=d
                        winner=str(i)
                    else:
                        lise.append(i)
            if winner==cat:
                return cat
            else:
                return self.hillclimbing(vect,ti,totals,doc,winner,lise)
        else:
            return cat


    def tfidfer(self,entries, language, tidf=True):  # To Apply on new Documents
        with open(os.path.join('ML','Categorization','modals',str(language),'nasus'),'rb') as f1:
            modal = pickle.load(f1)
        with open(os.path.join('ML','Categorization','modals',str(language),'vect'), 'rb') as f2:
            vect = pickle.load(f2)
        with open(os.path.join('ML','Categorization','modals',str(language),'tfidf'), 'rb') as f3:
            ti = pickle.load(f3)
        all=[]
        for entry in entries:
            stop = set(stopwords.words(language))
            temp = word_tokenize(entry)
            bam = []
            for d in entry:
                if d not in stop:
                    bam.append(d)
            fin=' '.join(bam)
            all.append(fin)
        x = vect.transform(all)
        if tidf == True:
            x = ti.transform(x)
        return x

    def add(self, path,name):
        print('Adding '+str(path))
        path = str(path)
        if '/.' in path:
            return
        progs = ['.c', '.html', '.cpp', '.py', '.perl', '.java', '.css', '.php', '.js', '.css', '.sh', '.bash']
        d = False
        if path.endswith(tuple(progs)):
            d=True
            tmp={}
            for x in progs:
                tmp[x]=0
                noup=0
            lim = os.path.dirname(os.path.normpath(path))
            for root, dirs, files in os.walk(lim):
                for name in files:
                    if name.endswith(tuple(progs)):
                        for d in progs:
                            if name.endswith(d):
                                tmp[d]=tmp[d]+1
                            else:
                                noup=noup+1
            indice=''
            maxim=noup
            bab=False
            for soums in tmp:
                if tmp[soums]>=maxim:
                    bab=True
                    indice=soums
                    maxim=tmp[soums]
            if bab:
                di = Document(lim, '', lim, type=indice, language=None)
                test = False
                for i in self.projets:
                    for j in self.projets[i]:
                        if di.justname.startswith(j.justname):
                            test = True
                if test is False:
                    di.score=1/len(self.nodes)
                    self.projets[x].append(di)
        if not d:
            s = sorter()
            ps = PorterStemmer()
            r = s.createdocument(path, name)
            language = r.language
        if not d and r.category not in ['Img','Vid','Aud','.py']:
            something=pickle.load(open(os.path.join('resources','tree',str(r.language),str(r.category)),'rb'))
            with open(os.path.join('ML','Categorization','modals', str(r.language) , 'vect'), 'rb') as f2:
                vect = pickle.load(f2)
            with open(os.path.join('ML','Categorization','modals',str(r.language), 'tfidf'), 'rb') as f3:
                ti = pickle.load(f3)
            self.nodes[self.equivalents[self.language][r.category]].visible = True
            cous=self.hillclimbing(vect,ti,something, r.text ,r.category,[])
            r.setcategory(cous)
            try:
                r.score=1/(len(self.documents)+1)
            except:
                r.score=0

        if r is None:
            return
        else:
            self.nodes[self.equivalents[self.language][r.category]].add(r)
            self.nodes[self.equivalents[self.language][r.category]].visible=True

            r.score=1/(len(self.nodes)+1)

            self.documents.append(r)
            for x in self.hiearchy:
                if r.category in self.hiearchy[x]:
                    self.nodes[x].visible=True
            for i in r.tokens:
                try:
                    self.keys[i.lower()].append(r)
                except:
                    self.keys[i.lower()]=[]
                    self.keys[i.lower()].append(r)
            for i in r.tok:
                try:
                    self.keys[i.lower()].append(r)
                except:
                    self.keys[i.lower()]=[]
                    self.keys[i.lower()].append(r)


    def getdoc(self, name):
        for i in self.documents:
            if i.justname==name:
                return i
        for i in self.projets:
            for j in self.projets[i]:
                if j.justname==name:
                    return j
        return None

    def docs(self):
        r=[]
        for i in self.nodes:
            r.append(self.nodes[i].documents())
        return r

    def save(self):
        pickle.dump(self.documents,open(os.path.join('profile','documents'), 'wb'))
        pickle.dump(self.favoris,open(os.path.join('profile','favoris'),'wb'))
        pickle.dump(self.recents,open(os.path.join('profile','recents'),'wb'))
        pickle.dump(self.projets,open(os.path.join('profile','projets'),'wb'))


    def gettags(self):
        tags={}
        for i in self.documents:
            for j in i.tags:
                try:
                    tags[j].append(i)
                except:
                    tags[j]=[]
                    tags[j].append(i)

        return tags


    def load(self):
        documents=pickle.load(open(os.path.join('profile','documents'),'rb'))
        self.favoris = pickle.load(open(os.path.join('profile','favoris'), 'rb'))
        self.recents = pickle.load(open(os.path.join('profile','recents'), 'rb'))
        self.projets = pickle.load(open(os.path.join('profile','projets'), 'rb'))
        for i in documents:
            soum=self.equivalents[self.language][i.category]
            for x in self.hiearchy:
                if self.equivalents[self.language][i.category] in self.hiearchy[x]:
                    self.nodes[x].visible=True
            for j in i.tokens:
                try:
                    self.keys[j].append(i)
                except:
                    self.keys[j.lower()]=[]
                    self.keys[j.lower()].append(i)
            for d in i.tok:
                try:
                    self.keys[d.lower()].append(i)
                except:
                    self.keys[d.lower()]=[]
                    self.keys[d.lower()].append(i)
            self.nodes[soum].add(i)


            self.documents.append(i)
        highlighted={}
        for i in self.documents:
            highlighted[i.justname]=i.score
        self.highlighted=dict(sorted(highlighted.items(), key=operator.itemgetter(1)))


    def verify(self):
        x=0
        print('Verifying')
        self.configuration.load()
        directories=tuple(self.configuration.work)
        for d in self.documents:
            if not (os.path.isfile(d.name) or os.path.isdir(d.name)) or not (d.name.startswith(directories)):
                self.delete(d.justname)
            x=x+1

        x=0
        for d in self.favoris:
            if not (os.path.isfile(d) or os.path.isdir(d)) or not (d.startswith(directories)):
                self.delete(d)
            x=x+1
        x=0
        for d in self.recents:
            if not (os.path.isfile(d) or os.path.isdir(d)) or not (d.startswith(directories)):
                self.delete(d)

            x=x+1

        for n in self.projets:
            x=0
            for v in self.projets[n]:
                if not (os.path.isdir(v.name)) or not (d.name.startswith(directories)):
                    self.projet[n].pop(x)
                    m = self.getdoc(d)
                    l = m.category
                    self.nodes[l].pop(self.nodes[l].index(m))
                x=x+1

    def delete(self,file):
        print('Deleting '+str(file))
        x=0
        m = self.getdoc(file)
        l = m.category

        for d in self.documents:
            if file==d.justname:
                self.documents.pop(x)
            x=x+1
        x=0
        for d in self.favoris:
            if file==d:
                self.favoris.pop(x)
            x=x+1
        x=0
        for d in self.recents:
            if file==d:
                self.recents.pop(x)
            x=x+1

        x=0
        for n in self.projets:
            for v in self.projets[n]:
                if file==v.justname:
                    self.projets[n].pop(x)

            x=x+1
            self.projets[n]=list(set(self.projets[n]))
        x=0
        for l in self.nodes:
            for x in range(0,len(self.nodes[l].docs)):
                try:
                    if self.nodes[l].docs[x].justname==m.justname:
                        del self.nodes[l].docs[x]
                except:
                    pass
            self.nodes[l].docs = list(set(self.nodes[l].docs))
        del m
