from BackEnd.Document import Document
import os
import pickle
import getpass

class Config:
    def __init__(self,lang='English',dev=False):
        self.user=getpass.getuser()
        self.language=lang
        self.developper=dev
        self.search=[]

        if not os.path.isdir('profile'):
            os.mkdir('profile')
        self.path=''
        self.work=[]
        self.load()
    def load(self):
        if os.path.isfile(os.path.join('profile','configuration')):
            lis=open(os.path.join('profile','configuration'),'r').read().splitlines()
            language=lis[0].split(':')
            dev=lis[1].split(':')
            path=lis[2].split(':')
            work=lis[3].split(':')
            self.developper=dev[1]
            self.path=path[1]
            self.language=language[1]
            self.work=work[1].split(',')
            self.search=pickle.load(open(os.path.join('profile','bm'),'rb'))
            
    def save(self):
        r=open(os.path.join('profile','configuration'),'w')
        r.write('language:'+str(self.language)+'\n')
        r.write('dev:'+str(self.developper)+'\n')
        r.write('path:'+str(self.path)+'\n')
        r.write('work:'+str(','.join(self.work)))
        pickle.dump(self.search, open(os.path.join('profile','bm'),'wb'))
        r.close()