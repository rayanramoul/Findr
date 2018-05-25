class VisibleTree:
    def __init__(self, concept=" "):
        self.concept = concept
        self.documents = None
        self.kids={}

    def printer(self):
        print('Racine :')
        for j in self.kids:
            j.print()

