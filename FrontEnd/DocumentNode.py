
from PyQt4 import QtGui,QtCore

import os

import ntpath


class DocumentNode(QtGui.QPushButton):
    def __init__(self, document):
        super(DocumentNode, self).__init__(document.name,)
        css = """ font-family: 'Montserrat';
                color:white;
                background-color:black;
                font-size:10px;
                
                """
        self.filename=document.name
        self.setStyleSheet(css)
        self.setIcon(QtGui.QIcon('resources/icons/document.png'))
        QtCore.QObject.connect(self, QtCore.SIGNAL('clicked()'), self.clicked)


    def clicked(self):
        f=self.filename.split(' ')
        f='\ '.join(f)
        f=self.filename.split('\'')
        f='\''.join(f)
        os.system('xdg-open '+f)