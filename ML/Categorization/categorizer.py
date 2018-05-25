import pickle
import nltk
from sklearn.naive_bayes import MultinomialNB
from string import punctuation
from nltk.corpus import stopwords



class categorizer:
    def __init__(self,language):
        if True: # Load the existing modals
            with open('ML/Categorization/modals/'+language+'/nasus','rb') as f1:
                self.modal=pickle.load(f1)
            with open('ML/Categorization/modals/'+language+'/vect','rb') as f2:
                self.vect=pickle.load(f2)
            with open('ML/Categorization/modals/'+language+'/tfidf','rb') as f3:
                self.ti=pickle.load(f3)
        self.language=language

    def nasus(self, document):  # predict
        m = self.modal
        doc = open(document, 'r').read()
        l = self.tfidfer([doc], tidf=True)
        return m.predict(l)


    def process(self, text):
        voids=stopwords.words(self.language)
        org=nltk.word_tokenize(text)
        final=[]
        ponct=(set(punctuation))
        word=''
        for word in org:
            if word not in voids and word not in ponct:      # On peut réecrire un mot des qu'il n'est pas un mot vide ou un caractère special
                final.append(word)
        return str(' '.join(word))

        self.tokens=final



    def tfidfer(self, entry, tidf=True): # To Apply on new Documents
        x=self.vect.transform(entry)
        if tidf==True:
            x = self.ti.transform(x)
        return x

    def predict(self, text):
        m = self.modal
        doc = text
        l = self.tfidfer([doc])
        return m.predict(l)[0]


