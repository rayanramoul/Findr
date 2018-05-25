class Node: # Represent a concept
    def __init__(self, concept,parent):
        self.concept = concept
        self.titles = []
        self.docs=[]
        self.visible=False
        self.kids={}
        self.name = str(len(self.docs))
        self.parent=parent

    def addkid(self,node):
        self.kids[str(node.concept)]=node


    def empty(self):
        return len(self.docs)==0

    def haskids(self):
        return len(self.kids)==0

    def documents(self):
        return {self.concept:self.titles}

    def getsubdocs(self):
        l=[]
        l=self.docs
        for i in self.kids:
            if self.kids[i].visible is True:
                l=l+self.kids[i].getsubdocs()
        return l

    def add(self, document):
        self.titles.append(document.name)
        self.docs.append(document)
        self.name = str(len(self.docs))
        self.visible=True


    def delete(self, document):
        if document in self.docs:
            self.docs.remove(document)
            return 1
        return 0

