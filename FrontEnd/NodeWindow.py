from PyQt4 import QtGui,QtCore
from FrontEnd.DocumentNode import DocumentNode


class Category(QtGui.QPushButton):
    def __init__(self, node):

        super(Category,self).__init__('RETOUR vers '+node.name)
        css = """
                color:white;
                background-color:transparent;
                font-size:12px;
                """

        self.setStyleSheet(css)
        self.node = node
        self.setIcon(QtGui.QIcon('resources/icons/arrow.png'))


class Cat(QtGui.QPushButton):
    def __init__(self, document):
        super(DocumentNode, self).__init__(document.name)
        css = """
                color:white;
                background-color:black;
                font-size:10px;
                """
        self.setText()
        self.filename=document.name
        self.setText(self.filename)
        self.setStyleSheet(css)
        self.setIcon(QtGui.QIcon('resources/icons/document.png'))
        QtCore.QObject.connect(self, QtCore.SIGNAL('clicked()'), self.clicked)

    def clicked(self, cat):
        print('Opening ..'+cat.name)
        NodeWindow(cat,self.stacked)


class NodeWindow(QtGui.QWidget):
    def __init__(self, node, stacked,parent=None):
        super(NodeWindow, self).__init__(parent)
        # Initialize resources
        print('Size node : '+str(len(node.docs)))
        self.layout = QtGui.QVBoxLayout()

        self.setWindowTitle('Findr')
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #24263d;")
        self.buttons = []
        c=Category(node.parent)
        self.layout.addWidget(c)
        self.node=node

        for i in node.docs:
            print('Document : '+i.justname)
            self.layout.addWidget(DocumentNode(i))
        self.setLayout(self.layout)
        stacked.addWidget(self)
        c.clicked.connect(lambda:self.ret(stacked))
        stacked.setCurrentWidget(self)
        self.show()


    def ret(self, stacked):
        if self.node.parent.name=='Hidden':
            stacked.setCurrentIndex(0)
        else:
            stacked.setCurrentIndex(stacked.currentIndex())