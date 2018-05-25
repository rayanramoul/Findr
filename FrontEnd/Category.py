import sys
from PyQt4 import QtGui,QtCore
from BackEnd.HiddenTree import HiddenTree
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QImage, QPalette, QBrush
from PyQt4.QtCore import Qt
from FrontEnd.NodeWindow import NodeWindow


class Category(QtGui.QPushButton):
    def __init__(self, node, stacked, widget, x, y):

        super(Category,self).__init__(node.name, widget)
        css = """
                color:white;
                background-color:#40484E;
                font-size:20px;
                text-align:center;
                """
        self.setStyleSheet(css)
        if node.name=='Hidden':
            stacked.setCurrentWidget(stacked.widget(1))

        self.l1 = QtGui.QLabel(widget)
        self.l1.setText(node.concept)
        css = """
                color:white;
                background-color:transparent;
                font-size:20px;
                text-align:left;
                """
        self.l1.setStyleSheet(css)
        self.l1.move(x,y-30)
        self.setStyleSheet(css)
        self.node = node
        self.setIcon(QtGui.QIcon('resources/icons/'+self.node.concept.lower()+'.png'))
        self.move(x, y)
        self.l1.resize(200,40)
        self.resize(200, 30)



