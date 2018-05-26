# -*- coding: utf-8 -*-
import sip
sip.setapi('QString', 1)
sip.setapi('QChar', 1)
import pipes
import sys
from PyQt4 import QtGui,QtCore
from BackEnd.HiddenTree import HiddenTree
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from BackEnd.Node import Node
from BackEnd.Document import Document
import os
from BackEnd.Config import Config
from locale import getdefaultlocale
import getpass
import operator
from os.path import expanduser
from QNotifications import QNotificationArea

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        self.user=getpass.getuser()
        self.configuration=Config()
        self.loadedfav=False
        self.loadedrec=False
#======================== Initialize resources ==================

        self.resources='resources'
        self.background=os.path.join(self.resources,'background.jpg')
        self.logo=os.path.join(self.resources,'zozio.png')
        self.main=0
        self.actualcat='Findr'
# ===================== Create the app ======================
        self.app = QtGui.QApplication(['Findr'])
        self.app.setWindowIcon(QtGui.QIcon(os.path.join(self.resources,'Findr.png')))
        super(MainWindow, self).__init__(parent)

        self.widget = QtGui.QWidget()
        self.stacked=QtGui.QStackedWidget()
        self.stacked.addWidget(self.widget)
        self.stacked.setCurrentWidget(self.widget)

        self.widget.setFixedSize(1200, 600)
        self.setFixedSize(1200, 600)
        self.widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.widget.setStyleSheet("background-color: #24263d;")
        self.configuration.path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

#==================== TRANSLATOR ==================================
        locale = getdefaultlocale()
        translator = QtCore.QTranslator()
        if self.configuration.language == 'العربية':
            language = 'arabic'
            self.app.setLayoutDirection(Qt.RightToLeft)
        else:
            language = self.configuration.language.lower()
        translator.load(os.path.join('translate' , language + '.qm'))
        self.app.installTranslator(translator)

#============================ Logo ==============================
        picture=QtGui.QLabel(self.widget)
        logo=QtGui.QPixmap(os.path.join("resources","zozio.png"))
        logo = logo.scaledToWidth(50)
        logo = logo.scaledToHeight(80)
        picture.setPixmap(logo)
        picture.move(30,30)

#========================== CATEGORIES =================================
        self.ht = HiddenTree()
        for dim in self.configuration.work:
            self.ht.initialize(dim)
            self.ht.verify()
        self.cats=[]
        cats=["Arts", "Health", "News", "Science", "Society",
                             "Business", "Games", "Home", "Recreation", "Sports"]
        if self.configuration.language.lower()=='français':
            for d in cats:
                self.cats.append(str(self.ht.equivalents['français'][d]))

        elif self.configuration.language.lower()=='العربية':
            for d in cats:
                self.cats.append(str(self.ht.equivalents['العربية'][d]))
        else:
            self.cats =cats
        self.searched=False
        self.permanent=self.cats
#==================== SEARCH BAR ===============================
        self.searchtext = QtGui.QLineEdit(self.widget)
        self.searchtext.returnPressed.connect(self.search)
        self.completer=QCompleter()
        self.model=QStringListModel()
        self.model.setStringList(self.cats+self.configuration.search)
        self.completer.setModel(self.model)
        self.searchtext.setCompleter(self.completer)
        self.searchtext.setPlaceholderText(self.tr('Search..'))

        self.searchtext.setFixedSize(190, 25)
        css = """
        background-color:#2b2a49;
        border-color:black;
        border-style:solid;
        """
        self.searchtext.setStyleSheet(css)




#============================= CONTENT ===================================

        self.total=QtGui.QVBoxLayout()
        self.widget.setLayout(self.total)
        self.top=QtGui.QHBoxLayout()
        self.top.addWidget(self.searchtext)
        self.topwidget=QtGui.QWidget()
        self.topwidget.setFixedSize(1000,40)
        self.topwidget.setMaximumSize(1000,40)
        self.topwidget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.closewindow=QPushButton()
        self.closewindow.setText('X')
        self.closewindow.setFixedSize(12,12)
        self.hidewindow=QPushButton()
        self.hidewindow.setText('-')
        self.hidewindow.setFixedSize(12,12)
        self.closewindow.clicked.connect(self.close)
        self.hidewindow.clicked.connect(self.hide)

        self.top.addStretch()
        self.notification=QLabel()
        self.notification.setText(self.tr(''))
        self.notification.setStyleSheet('color:#e0860b;')
        self.top.addWidget(self.notification)
        self.top.addWidget(self.hidewindow)
        self.top.addWidget(self.closewindow)
        self.topwidget.setLayout(self.top)
        self.total.addWidget(self.topwidget)
        self.widget.setLayout(self.total)
        self.content=QtGui.QHBoxLayout()


#============================ FAVORIS CATEGORIES RECENTS ================

        self.listBox=QtGui.QVBoxLayout()              # The Box for categories
        self.catcontent=QtGui.QVBoxLayout()
        self.partone=QtGui.QWidget()
        self.partone.setLayout(self.content)
        self.partone.setStyleSheet('background-color:#282945;')
        self.partone.setFixedSize(1000,500)
        self.parttwo=QtGui.QWidget()
        self.parttwo.setLayout(self.catcontent)
        self.parttwo.setStyleSheet('background-color:#1d1e32;')
        self.total.addWidget(self.partone)

        self.previewwidget=QWidget()
        self.previewbox=QVBoxLayout()
        self.previewwidget.setLayout(self.previewbox)
        self.previewwidget.setStyleSheet('background-color:#252740;')
        self.previewwidget.setFixedSize(270,480)

        if self.configuration.language=='العربية':
            self.content.addWidget(self.previewwidget)
            self.content.addWidget(self.parttwo)
            self.content.addLayout(self.listBox)

        else:
            self.content.addLayout(self.listBox)
            self.content.addWidget(self.parttwo)
            self.content.addWidget(self.previewwidget)

        self.csstreecontent=''' QTreeWidget{
        background-color:#191a2c;font-size:20px;}
       QTreeWidget::branch:closed:has-children:has-siblings {
border-image: none;
image: url('''+str(os.path.join('resources','icons','unexpanded.png'))+''');
}
QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {
border-image: none;
image: url('''+str(os.path.join('resources','icons','expanded.png'))+''');
}'''
        cssarabic=''' QTreeWidget{justifiy:right;align:right;
        background-color:#191a2c;font-size:20px;}
       QTreeWidget::branch:closed:has-children:has-siblings {
border-image: none;
image: url('''+str(os.path.join('resources','icons','unexpanded.png'))+''');
}
QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {
border-image: none;
image: url('''+str(os.path.join('resources','icons','expanded.png'))+''');
}'''
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemSelectionChanged.connect(lambda:self.clicked('tree'))
        self.listBox.addWidget(self.tree)
        if self.configuration.language=='العربية':
            self.tree.setStyleSheet(cssarabic)
        else:
            self.tree.setStyleSheet(self.csstreecontent)
        p=QtGui.QPalette()
        p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText,QtGui.QBrush(QColor("red")))
        self.tree.setPalette(p)
        self.tree.setFixedSize(200,500)

            # ========================= FAVORIS ======================================
        self.favoris = QtGui.QTreeWidgetItem(self.tree)
        self.favoris.setText(0, self.tr("Favorites"))
        self.favoris.setFlags(self.favoris.flags() | Qt.ItemIsTristate)
        self.favoris.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))

        self.favcontainer = QTreeWidget()
        self.favcontainer.setHeaderHidden(True)
        self.favcontainer.setStyleSheet('background-color:#1c1d31;font-size:16px;')
        self.favtree = QTreeWidgetItem(self.favcontainer)
        self.favtree.setText(0, self.tr('Favorites'))
        self.favtree.setExpanded(True)
        lise = []
        for j in self.ht.favoris:
            if j not in lise:
                child = QTreeWidgetItem(self.favtree)

                child.setText(0, j)
                lise.append(j)
        self.favcontainer.itemSelectionChanged.connect(lambda: self.newpreview('Favoris'))




        self.categories= QtGui.QTreeWidgetItem(self.tree)
        self.categories.setText(0,self.tr("Categories"))
        self.categories.setFlags(self.categories.flags() | Qt.ItemIsTristate)
        self.categories.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))
        self.child={}
        for item in self.cats:
            if self.ht.nodes[item].visible:
                self.child[item] = QTreeWidgetItem(self.categories)
                self.child[item].setIcon(0, QtGui.QIcon(os.path.join('resources','icons','folder-blue.png')))
                self.child[item].setFlags(self.child[item].flags() )
                self.child[item].setText(0, item)
                self.child[item].setForeground(0, QtGui.QBrush(QtGui.QColor("#a0833f")))

            else:
                self.child[item] = QTreeWidgetItem()
                self.child[item].setFlags(self.child[item].flags() )
                self.child[item].setIcon(0, QtGui.QIcon(os.path.join('resources','icons','folder-blue.png')))
                self.child[item].setText(0, item)
                self.child[item].setForeground(0, QtGui.QBrush(QtGui.QColor("#a0833f")))


#============================= CAT CONTENT ===============================
        self.title=QLabel()
        self.title.setStyleSheet('background-color:#c78701;color:white;border-radius: 25px;')
        self.title.setText('        FINDR')
        self.title.setFixedSize(130,40)

        self.catcontent.addWidget(self.title)

        self.cou = {}
        self.trou={}
        self.csscatcontent='''QTreeWidget{background-color:#1c1d31;font-size:16px;} QTreeWidget::indicator:unchecked {image: url('''+str(os.path.join('resources','icons','unchecked.png'))+''');}
QTreeWidget::indicator:checked {image: url('''+str(os.path.join('resources','icons','checked.png'))+''');}
QTreeWidget::branch:closed:has-children:has-siblings{border-image: none;image: url('''+str(os.path.join('resources','icons','unexpanded.png'))+''');}
QTreeWidget::branch:open:has-children:!has-siblings,QTreeWidget::branch:open:has-children:has-siblings {border-image: none;image: url(
'''+str(os.path.join('resources','icons','unexpanded.png'))+''');}'''

        for i in self.permanent:
            actualcat=i
            self.trou[actualcat]=QTreeWidget()
            self.trou[actualcat].setHeaderHidden(True)
            self.cou[actualcat]=QTreeWidgetItem(self.trou[i])
            self.trou[actualcat].itemChanged.connect(self.handleItemChanged)
            self.trou[actualcat].setFixedSize(600, 450)
            self.trou[actualcat].setStyleSheet(self.csscatcontent)
            self.cou[actualcat].setExpanded(True)

            self.develop(i, self.cou[i], 0, [])
            self.trou[actualcat].itemSelectionChanged.connect(lambda: self.newpreview(actualcat))
        self.catcontent.addWidget(self.trou[i])
        self.trou['Favoris'] = self.favcontainer


#======================== MULTIMEDIA =====================================
        self.multimedia= QtGui.QTreeWidgetItem(self.tree)
        self.multimedia.setText(0,self.tr("Multimed"))
        self.multimedia.setFlags(self.multimedia.flags() | Qt.ItemIsTristate)
        self.multimedia.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))

        self.multcontainer=QTreeWidget()
        self.multcontainer.setHeaderHidden(True)
        self.multcontainer.setStyleSheet(self.csscatcontent)
        self.trou['Multimed']=self.multcontainer
        self.multtree=QTreeWidgetItem(self.multcontainer)
        self.multtree.setText(0,self.tr('Multimed'))
        self.develop('Multimed', self.multtree, 0,[])
        self.multcontainer.itemSelectionChanged.connect(lambda:self.newpreview('Multimed'))
        self.multtree.setExpanded(True)
#=================================== TAGS ===========================================
        self.tags = QtGui.QTreeWidgetItem(self.tree)
        self.tags.setText(0, self.tr("Tags"))
        self.tags.setFlags(self.tags.flags() | Qt.ItemIsTristate)
        self.tags.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))

        self.tagcontainer = QTreeWidget()
        self.tagcontainer.setHeaderHidden(True)
        self.tagcontainer.setStyleSheet(self.csscatcontent)
        self.trou['Tags'] = self.tagcontainer
        self.tagtree = QTreeWidgetItem(self.tagcontainer)
        self.tagtree.setText(0, self.tr('Tags'))
        self.tagcontainer.itemSelectionChanged.connect(lambda: self.newpreview('Tags'))
        self.tagtree.setExpanded(True)
        #======================== DEVELOPPER ============================
        if self.configuration.developper!='False':
            self.developper= QtGui.QTreeWidgetItem(self.tree)
        else:
            self.developper= QtGui.QTreeWidgetItem()
        self.developper.setText(0,self.tr("Developement"))
        self.developper.setFlags(self.developper.flags() | Qt.ItemIsTristate)
        self.developper.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))
        self.devcontainer=QTreeWidget()
        self.devcontainer.setHeaderHidden(True)
        self.devcontainer.setStyleSheet(self.csscatcontent)
        self.trou['Developement']=self.devcontainer
        self.devtree=QTreeWidgetItem(self.devcontainer)
        self.devtree.setText(0,self.tr('Developement'))
        self.devtree.setExpanded(True)
        self.trou['Developement']=self.devcontainer
        hx = self.ht.projets
        for i in hx:
            child1 = QTreeWidgetItem(self.devtree)
            child1.setText(0, i)
            for d in hx[i]:
                child2 = QTreeWidgetItem(child1)
                child2.setText(0, d.justname)
                if d in self.ht.favoris or d.justname in self.ht.favoris:

                    child2.setCheckState(0, Qt.Checked)
                else:
                    child2.setCheckState(0, Qt.Unchecked)
                child2.setFlags(child2.flags() | Qt.ItemIsUserCheckable)
        self.devcontainer.itemSelectionChanged.connect(lambda:self.newpreview('Developement'))
        self.devcontainer.itemChanged.connect(self.handleItemChanged)

    #=================================== RECENTS ============================

        self.recents= QtGui.QTreeWidgetItem(self.tree)
        self.recents.setText(0,self.tr("Recent"))
        self.recents.setFlags(self.recents.flags() | Qt.ItemIsTristate)
        self.recents.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))
        self.reccontainer=QTreeWidget()
        self.reccontainer.setHeaderHidden(True)
        self.reccontainer.setStyleSheet(self.csscatcontent)
        self.rectree=QTreeWidgetItem(self.reccontainer)
        self.rectree.setText(0,self.tr('Recent'))
        self.reccontainer.itemSelectionChanged.connect(lambda:self.newpreview('rec'))
        self.trou['rec']=self.reccontainer
        self.rectree.setExpanded(True)
        for x in reversed(self.ht.recents):
            child = QTreeWidgetItem(self.rectree)
            child.setText(0, str(x))

#============================= SIDE MENU ===================================
        self.menu=QToolBar()
        self.menu.setStyleSheet('background-color:#22243b;')
        self.menu.setMovable(False)
        self.menu.setIconSize(QtCore.QSize(50,50))
        self.menu.resize(600,30)
        self.menu.addWidget(picture)

        self.addToolBar(Qt.LeftToolBarArea, self.menu)
        self.homebar=self.menu.addAction(' ')
        s=QIcon()
        pix=QPixmap(os.path.join('resources','icons','homehover.png'))
        self.homebar.setIcon(QtGui.QIcon(pix.scaled(50,50)))
        self.homebar.triggered.connect(lambda:self.menuclick('Home'))

        self.configbar=self.menu.addAction(' ')

        self.configbar.setIcon(QtGui.QIcon(os.path.join('resources', 'icons', 'config.png')))
        self.configbar.triggered.connect(lambda:self.menuclick('Configuration'))
        self.widget.setWindowTitle('Findr')




        self.pic = QtGui.QLabel()
        self.pic.setText('.....................................\n.....................................\n................................\n..............................\n.................')
        self.pic.setFixedSize(250,200)
        # use full ABSOLUTE path to the image, not relative
        self.pic.setStyleSheet('font-size:25px;color:#1a1c32;')

        self.documenttitle=QLabel()
        self.previewbox.addWidget(self.documenttitle)
        self.previewbox.addWidget(self.pic)

        self.documenttitle.setStyleSheet('background-color:#23253e;color:#333750;text-align:center;font-size:20px;')
        self.documenttitle.setText(self.tr('Document'))
        self.documenttitle.setAlignment(Qt.AlignCenter)
        self.documenttitle.setFixedSize(250,40)

        but=QPushButton()
        but.setText(self.tr('Open'))
        but.setFixedSize(250, 40)

        but.setStyleSheet('color:white;background-color:#e0a501;')
        lab=QLabel()
        self.previewbox.addWidget(but)
        semilayout=QHBoxLayout()
        self.previewbox.addLayout(semilayout)
        lab.setText(self.tr('Category :'))
        lab.setStyleSheet('color:#15172b;')
        semilayout.addWidget(lab)
        lab=QLabel()
        lab.setText('...........')
        lab.setStyleSheet('color:#303251;')
        semilayout.addWidget(lab)
        lab=QLabel()
        semilayout=QHBoxLayout()
        self.previewbox.addLayout(semilayout)
        lab.setText(self.tr('Key Words :'))
        lab.setStyleSheet('color:#15172b;')
        semilayout.addWidget(lab)
        lab=QLabel()
        lab.setText('...........')
        lab.setStyleSheet('color:#303251;')
        semilayout.addWidget(lab)

        #================================= HIGHLIGHTED ===========================
        self.highlight=QTreeWidgetItem(self.tree)
        self.highlight.setText(0,self.tr('Highlighted'))
        self.highlightcontainer=QTreeWidget()
        self.highlighttree=QTreeWidgetItem(self.highlightcontainer)

        self.highlight.setFlags(self.highlight.flags() | Qt.ItemIsTristate)
        self.highlight.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))

        self.highlightcontainer.setHeaderHidden(True)
        self.highlightcontainer.setStyleSheet(self.csscatcontent)
        self.highlighttree.setText(0,self.tr('Highlighted'))
        self.highlightcontainer.itemSelectionChanged.connect(lambda:self.newpreview('high'))
        self.trou['high']=self.highlightcontainer
        self.highlighttree.setExpanded(True)
        bim=0
        d=[]
        for x in self.ht.highlighted:
            d.append(x)

        for x in reversed(d):
            if True:
                child = QTreeWidgetItem(self.highlighttree)
                child.setText(0, str(x))
                bim=bim+1



        #================================= CONFIGURATION ==========================
        self.config=QWidget()

        self.configcontainer=QVBoxLayout()
        self.toplane=QHBoxLayout()
        self.toplane.addStretch()


        self.closewi=QPushButton()
        self.closewi.setText('X')
        self.closewi.setFixedSize(12,12)
        self.hidewi=QPushButton()
        self.hidewi.setText('-')
        self.hidewi.setFixedSize(12,12)
        self.closewi.clicked.connect(self.close)
        self.hidewi.clicked.connect(self.hide)


        self.toplane.addWidget(self.hidewi)
        self.toplane.addWidget(self.closewi)

        self.config.setLayout(self.configcontainer)
        self.choice=QLabel()
        self.configcontainer.addLayout(self.toplane)
        self.choice.setText(self.tr('Language'))
        self.choice.setAlignment(Qt.AlignCenter)
        self.configcontainer.addWidget(self.choice)
        self.lang=QtGui.QComboBox()
        self.lang.addItem(self.configuration.language)
        for i in ['English','Français','العربية']:
            if i!=self.configuration.language:
                self.lang.addItem(i)
        self.question=QLabel()

        self.question.setText(self.tr('Are you a developper ?'))
        self.question.setAlignment(Qt.AlignCenter)
        self.configcontainer.addWidget(self.lang)
        self.configcontainer.addWidget(self.question)
        self.devyes=QtGui.QRadioButton(self.tr('Yes'))
        self.directories=QListWidget()
        self.adddirectory=QtGui.QPushButton(self.tr('Add a folder'))
        self.suppdirectory=QtGui.QPushButton(self.tr('Delete a folder'))
        self.suppdirectory.clicked.connect(self.suppressdirectory)
        self.adddirectory.clicked.connect(self.addfile)
        for i in self.configuration.work:
            self.directories.addItem(i)

        self.configcontainer.addWidget(self.devyes)
        self.devno=QtGui.QRadioButton(self.tr('No'))

        self.devno.setChecked(True)
        self.configcontainer.addWidget(self.devno)
        self.configcontainer.addWidget(self.adddirectory)
        self.configcontainer.addWidget(self.suppdirectory)
        self.configcontainer.addWidget(self.directories)
        self.devyes.toggled.connect(lambda: self.switch(self.devyes))
        self.devno.toggled.connect(lambda: self.switch(self.devno))

        self.saving=QPushButton()
        self.saving.setText(self.tr('Save'))

        self.configcontainer.addWidget(self.saving)
        self.saving.clicked.connect(self.savingconfig)
        self.config.setStyleSheet('color:white;background-color:#333750;')

        self.stacked.insertWidget(3, self.config)


        #=============================== THE WATCHER ==========================
        self.watcher=QFileSystemWatcher()
        self.configuration.load()
        for i in self.configuration.work:
            self.watcher.addPaths([x[0] for x in os.walk(str(i))])
        QtCore.QObject.connect(self.watcher, QtCore.SIGNAL('directoryChanged()'), self.directory_changed)
        QtCore.QObject.connect(self.watcher, QtCore.SIGNAL('fileChanged()'), self.file_changed)

        self.watcher.directoryChanged.connect(self.directory_changed)
        self.watcher.fileChanged.connect(self.file_changed)
#        self.visit()
        #================================ LAUNCHING ===========================
        self.setCentralWidget(self.stacked)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.show()
        self.stacked.setCurrentIndex(2)
        sys.exit(self.app.exec_())

    def onToggled1(self, checked):
        self.toolButton1.setIcon(QtGui.QIcon(os.path.join('resources','icons','homehover.png')))
        self.toolButton2.setChecked(False)
        self.toolButton2.setIcon(QtGui.QIcon(os.path.join('resources','icons','config.png')))
    def onToggled2(self, checked):
        self.toolButton2.setIcon(QtGui.QIcon(os.path.join('resources','icons','confighover.png')))
        self.toolButton1.setChecked(False)
        self.toolButton1.setIcon(QtGui.QIcon(os.path.join('resources','icons','home.png')))








    def switch(self,b):
        if b.text() == self.tr("Yes"):
            if b.isChecked() == True:
                print
                b.text() + " is selected"
            else:
                print
                b.text() + " is deselected"

        if b.text() == self.tr("No"):
            if b.isChecked() == True:
                print
                b.text() + " is selected"
            else:
                print
                b.text() + " is deselected"

    def menuclick(self, item):
        if item=='Home':
            self.stacked.setCurrentWidget(self.widget)
            self.homebar.setIcon(QtGui.QIcon(os.path.join('resources','icons','homehover.png')))
            self.configbar.setIcon(QtGui.QIcon(os.path.join('resources','icons','config.png')))


        if item=='Configuration':
            self.stacked.setCurrentWidget(self.config)
            self.homebar.setIcon(QtGui.QIcon(os.path.join('resources','icons','home.png')))
            self.configbar.setIcon(QtGui.QIcon(os.path.join('resources','icons','confighover.png')))
        self.menu.update()

    def addfile(self):
        try:
            tom=str(QtGui.QFileDialog.getExistingDirectory(self.widget, self.tr('Choose a Folder'), expanduser("~"),QtGui.QFileDialog.ShowDirsOnly))
        except:
            tom = str(QtGui.QFileDialog.getExistingDirectory(self.widget, self.app.tr('Choose a Folder'), expanduser('C:\ '),QtGui.QFileDialog.ShowDirsOnly))

        if tom!='' and tom!=' ':
            self.directories.addItem(tom)
    def suppressdirectory(self):
        for item in self.directories.selectedItems():
            self.directories.takeItem(self.directories.row(item))

    def savingconfig(self):
        self.configuration.language=self.lang.currentText()
        if self.devno.isChecked():
            self.configuration.developper=False
        else:
            self.configuration.developper=True
        save=[]
        for i in range(self.directories.count()):
            save.append(str(self.directories.item(i).text()))
        for i in save:
            if i not in self.configuration.work:
                self.ht.initialize(i)

        self.configuration.work=save
        self.configuration.save()
        self.ht.verify()
        self.refresh()

    def clicked(self, tree):
        selected = self.tree.selectedItems()
        cat = selected[0].text(0)
        if cat!=self.tr('Categories'):
            for i in reversed(range(self.catcontent.count())):
                self.catcontent.itemAt(i).widget().setParent(None)

            if cat==self.tr('Favorites'):
                self.actualcat = cat

                self.title.setText('        '+self.tr('Favorites'))


                for i in reversed(range(self.favtree.childCount())):
                    self.favtree.removeChild(self.favtree.child(i))
                lise=[]
                for x in self.ht.favoris:
                    if x not in lise:
                        child=QTreeWidgetItem(self.favtree)
                        child.setText(0,x)
                        lise.append(x)

                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.favcontainer)
                self.favcontainer.setFixedSize(600,450)

            elif cat==self.tr('Multimed'):
                cat=self.tr('Multimed')
                self.actualcat=str(cat)

                self.title.setText('        '+self.actualcat)
                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.multcontainer)
                self.multcontainer.setFixedSize(600,450)


            elif cat==self.tr('Recent'):
                self.actualcat = cat
                self.title.setText('        '+self.tr('Recent'))
                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.reccontainer)
                self.reccontainer.setFixedSize(600,450)


            elif cat==self.tr('Tags'):
                self.actualcat=str(cat)

                for i in reversed(range(self.tagtree.childCount())):
                    self.tagtree.removeChild(self.tagtree.child(i))

                self.title.setText('        '+self.actualcat)

                self.catcontent.addWidget(self.title)

                self.catcontent.addWidget(self.tagcontainer)
                self.tagcontainer.setFixedSize(600,450)
                hx=self.ht.gettags()
                for i in hx:
                    child1=QTreeWidgetItem(self.tagtree)
                    child1.setText(0,str(i))
                    for d in hx[i]:
                        child2=QTreeWidgetItem(child1)
                        child2.setText(0,d.justname)

            elif cat==self.tr('Developement'):
                self.actualcat=str(cat)

                self.title.setText('        '+self.actualcat)
                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.devcontainer)
                self.devcontainer.setFixedSize(600,450)

            elif cat==self.tr('Search'):

                self.title.setText('        '+self.tr('Search Results'))
                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.searchcontainer)

            elif cat==self.tr('Highlighted'):
                self.title.setText(self.tr('Highlighted'))
                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.highlightcontainer)
            else:
                self.actualcat=str(cat)

                self.title.setText('        '+self.actualcat)

                self.catcontent.addWidget(self.title)
                self.catcontent.addWidget(self.trou[self.actualcat])
                self.trou[self.actualcat].itemSelectionChanged.connect(lambda: self.newpreview(self.actualcat, dev=True))
                self.trou[self.actualcat].setFixedSize(600,450)



            self.catcontent.update()
            self.widget.update()



    def newpreview(self,tree,dev=False):
#        if tree!='fav' and tree!='rec':
        tree=str(tree)
        selected=self.trou[tree].selectedItems()
        cat = str(selected[0].text(0))

        total=[]
        dom=True
        if cat in self.ht.hiearchy.keys():
            return
        for x in self.ht.gettags():
            if x==cat:
                dom=False
        for x in self.ht.projets:
            if cat==x:
                dom=False
        trim=(cat==self.tr('Tags') or cat==self.tr('Documents') or cat==self.tr('Categories'))
        if cat!=str(self.tr('Favorites')) and cat!=str(self.tr('Recent')) and cat!='' and cat!=self.tr('Multimed') and cat!=self.tr('Developement') and  dom and not trim:
            document=''

            document=self.ht.getdoc(cat)

            self.pic = QtGui.QPlainTextEdit(document.text[:500])
            for i in reversed(range(self.previewbox.count())):
                try:
                    self.previewbox.itemAt(i).widget().setParent(None)
                except:
                    self.previewbox.itemAt(i).layout().setParent(None)
            if document.category!='Img':
#                self.pic.setText()
                self.pic.setReadOnly(True)
                self.pic.setStyleSheet('font-size:10px;color:#1a1c32;background-color:white;')
                    # use full ABSOLUTE path to the image, not relative
            else:
                pixmap = QtGui.QPixmap(document.name)
                self.pic=QLabel()

                self.pic.setPixmap(pixmap.scaled(250,200))
                self.show()


            self.pic.setFixedSize(250, 200)
            self.previewbox.addWidget(self.documenttitle)
            self.previewbox.addWidget(self.pic)

            if cat != 'Default':
                self.documenttitle.setText(cat)
            else:
                self.documenttitle.setText(self.tr('Title'))
#            qna = QNotificationArea(self.widget)
#            qna.display('This is an error notification', 'danger', None)
            #notif.show()

            sub=QHBoxLayout()
            self.previewbox.addLayout(sub)
            lab=QLabel()
            lab.setText(self.tr('Category :'))
            lab.setStyleSheet('color:#15172b;')
            sub.addWidget(lab)
            lab=QLabel()
            lab.setStyleSheet('color:white;')
            if document is not None:
                lab.setText(self.ht.equivalents[self.configuration.language.lower()][document.category])
            else:
                lab.setText('Project')
            sub.addWidget(lab)
            lab=QLabel()
            lab.setText(self.tr('Key Words :'))
            lab.setStyleSheet('color:#15172b;')
            self.previewbox.addWidget(lab)
            s=''
            for i in document.tags:
               s=s+i+','

            lab=QPlainTextEdit(QtCore.QString(s))
            lab.setFixedSize(250,40)
            butsave=QPushButton()
            butsave.setText(self.tr('Save Tags'))
            butsave.setFixedSize(250,40)
            butsave.clicked.connect(lambda :self.savetags(document,str(lab.toPlainText())))

            self.previewbox.addWidget(lab)
            self.previewbox.addWidget(butsave)
            but=QPushButton()
            but.setText(self.tr('Open'))
            but.setFixedSize(250,40)
            but.setStyleSheet('color:white;background-color:#e0a501;')
            but.clicked.connect(lambda: self.open(cat))

            self.previewbox.addWidget(but)
            self.previewbox.update()


    def savetags(self,doc,tags):
        doc.tags=list(filter(None, tags.split(',')))
        self.refresh()

    def open(self,doc):
        if type(doc) is str:
            if doc in self.ht.recents:
                self.ht.recents.pop(self.ht.recents.index(doc))
            self.ht.recents.append(str(doc))
        else:
            if doc.justname in self.ht.recents:
                self.ht.recents.pop(self.ht.recents.index(doc.justname))
            self.ht.recents.append(str(doc.justname))

        for i in reversed(range(self.rectree.childCount())):
            self.rectree.removeChild(self.rectree.child(i))
        for x in reversed(self.ht.recents):
            child = QTreeWidgetItem(self.rectree)
            child.setText(0, str(x))
        self.reccontainer.update()
        self.widget.update()
        document=self.ht.getdoc(doc)
        document.score=(1-0.1)*document.score+0.1
        for i in self.ht.documents:
            if i.justname!=document.justname:
                i.score=(1-0.1)*i.score
        highlighted={}
        for i in self.ht.documents:
            highlighted[i.justname]=i.score
        self.ht.highlighted=dict(sorted(highlighted.items(), key=operator.itemgetter(1)))
        bim=0
        for i in reversed(range(self.highlighttree.childCount())):
            self.highlighttree.removeChild(self.highlighttree.child(i))
        d=[]
        for x in self.ht.highlighted:
            d.append(x)

        for x in reversed(d):
            if True:
                child = QTreeWidgetItem(self.highlighttree)
                child.setText(0, str(x))
                bim=bim+1
        self.highlightcontainer.update()
        self.widget.update()
        try:
            lo=str(pipes.quote(document.name))
        except:
            pass
        try:
            os.popen("xdg-open "+str(lo))
        except:
            os.popen("start "+str(lo))


    def develop(self, cat, tree,limit, suppressed):
        self.notification.setText(self.tr('Initializing'))
        cat=str(cat)
        fav=self.ht.favoris
        ret=False
        calc=0
        if cat=='Multimed':
            if str(self.configuration.language).lower()=='français':
                cat='Multiméd'
            if str(self.configuration.language).lower()=='العربية':
                cat='الوسائط المتعددة'
        if self.ht.nodes[cat].haskids() is False:
            for i in self.ht.nodes[cat].kids:
                l=False
                for j in reversed(range(tree.childCount())):
                    if tree.child(j).text(0)==i:
                        l=True
                if l is False:
                    if self.ht.nodes[i].visible is True and i not in self.cats and i not in suppressed and limit<4:
                        child = QTreeWidgetItem()
                        child.setIcon(0, QtGui.QIcon(os.path.join('resources','icons','folder-orange.png')))
                        child.setFlags(child.flags())
                        child.setText(0, i)
                        child.setForeground(0, QtGui.QBrush(QtGui.QColor("#333750")))

                        b=self.develop(i,child,limit+1,suppressed)
                        if b is False:
                            suppressed.append(i)
                        else:
                            suppressed.append(i)
                            tree.addChild(child)
                            ret=True
                        calc=calc+1
        if self.ht.nodes[cat].empty()==False:

            for i in self.ht.nodes[cat].docs:
                l=False

                for j in reversed(range(tree.childCount())):
                    if tree.child(j).text(0)==i.justname:
                        l=True
                if l is False:
                    d = False
                    r = 0
                    child = QTreeWidgetItem(tree)
                    if i.justname in fav:
                        d=True
                    if d:
                        child.setCheckState(r, Qt.Checked)

                    else:
                        child.setCheckState(r,Qt.Unchecked)
                    ret = True
                    child.setText(0, i.justname)
                    child.setForeground(0, QtGui.QBrush(QtGui.QColor("#a0833f")))

                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    i.visible=True
        self.notification.setText(self.tr(''))
        return ret

    def visit(self):
        lis=[]
        for j in self.ht.documents:
            lis.append(j.justname)
        for i in self.permanent:
            bool = False
            for j in lis:
                deep=self.trou[i].findItems(j, QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)
                deepin=[]
                for bouch in deep:
                    deepin.append(str(bouch.text(0)))
                for j in reversed(range(self.cou[i].childCount())):
                    items=self.get_all_items(self.cou[i].child(j))
                    bim=[]
                    for dom in items:
                        bim.append(str(dom.text(0)))
                    for l in deepin:
                        if l in bim:
                            bool=True
                    if bool is False:
                        self.cou[i].removeChild(self.cou[i].child(j))



    def get_subtree_nodes(self,tree_widget_item):
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
        nodes = []
        nodes.append(tree_widget_item)
        for i in range(tree_widget_item.childCount()):
            nodes.extend(self.get_subtree_nodes(tree_widget_item.child(i)))
        return nodes

    def get_all_items(self,tree_widget):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = []
        for i in range(tree_widget.childCount()):
            top_item = tree_widget.child(i)
            all_items.extend(self.get_subtree_nodes(top_item))
        return all_items


    def search(self):
        self.notification.setText(self.tr('Searching'))
        if self.searchtext.text()!='':
            n = Node(self.tr('Results'), self.ht)
            for i in reversed(range(self.catcontent.count())):
                self.catcontent.itemAt(i).widget().setParent(None)

            results=[]
            self.configuration.search.append(self.searchtext.text())
            self.configuration.search=list(set(self.configuration.search))
            self.configuration.save()
            self.model.setStringList(self.cats + self.configuration.search)
            results=self.ht.search(self.searchtext.text())
            self.actualcat = self.tr('Search')
            if self.searched is False:
                searchchild=QTreeWidgetItem(self.tree)
                searchchild.setText(0,self.tr('Search'))
                self.searched=True

            self.searchcontainer=QTreeWidget()
            self.searchtree=QTreeWidgetItem(self.searchcontainer)
            self.searchcontainer.itemSelectionChanged.connect(lambda: self.newpreview('Search', dev=True))
            self.searchcontainer.setStyleSheet('background-color:#191a2c;')

            self.title.setText('        '+self.tr('Search Results'))
            self.catcontent.addWidget(self.title)
            self.catcontent.addWidget(self.searchcontainer)
            self.searchcontainer.setFixedSize(600, 450)
            self.searchtree.setExpanded(True)
            self.searchcontainer.setHeaderHidden(True)
            self.trou['Search']=self.searchcontainer
            for i in results:
                results[i]=list(set(results[i]))
            try:
                for i in reversed(range(self.searchtree.childCount())):
                    self.searchtree.removeChild(self.searchtree.child(i))
            except:
                pass
            for i in results:
                if len(results[i])!=0:
                    child1 = QTreeWidgetItem(self.searchtree)
                    child1.setExpanded(True)
                    child1.setText(0, i)
                    for d in results[i]:
                        child2 = QTreeWidgetItem(child1)
                        if isinstance(d,Document):
                            child2.setText(0, d.justname)
        self.notification.setText(self.tr(''))


    def handleItemChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            d = True
            for i in self.ht.favoris:
                if str(item.text(0)) == i:
                    d = False

            if d:
                self.ht.favoris.append(str(item.text(0)))
                for i in reversed(range(self.favtree.childCount())):
                    self.favtree.removeChild(self.favtree.child(i))
                x = 0
                lise = []
                for j in self.ht.favoris:
                    if j not in lise:
                        child = QTreeWidgetItem(self.favtree)
                        child.setText(0, j)
                        lise.append(j)

                return
        elif item.checkState(column) == QtCore.Qt.Unchecked:
            for i in reversed(range(self.favtree.childCount())):
                self.favtree.removeChild(self.favtree.child(i))
            x=0
            for j in self.ht.favoris:
                if j==item.text(0):
                    try:
                        self.ht.favoris.pop(x)
                    except:
                        pass
                x=x+1
            lise=[]
            for j in self.ht.favoris:
                if j not in lise:
                    child = QTreeWidgetItem(self.favtree)
                    child.setText(0, j)
                    lise.append(j)
        return




    def refresh(self):
        if True:
            if True:
                #  FAVORIS REFRESH
                self.actualcat = 'Categories'
                for i in reversed(range(self.favtree.childCount())):
                    self.favtree.removeChild(self.favtree.child(i))
                for x in self.ht.favoris:
                    child=QTreeWidgetItem(self.favtree)
                    child.setText(0,x)
                self.loadedfav=True

                # MULTIMEDIA
                self.multcontainer.itemChanged.connect(self.handleItemChanged)
                self.multcontainer.itemSelectionChanged.connect(lambda:self.newpreview('Multimedia'))

                for i in reversed(range(self.multtree.childCount())):
                    self.multtree.removeChild(self.multtree.child(i))
                tro=[]
                self.develop('Multimed', self.multtree,0,tro)


                # RECENTS REFRESH
                if True:
                    for i in reversed(range(self.rectree.childCount())):
                        self.rectree.removeChild(self.rectree.child(i))
                    for x in self.ht.recents:
                        child=QTreeWidgetItem(self.rectree)
                        child.setText(0,str(x.justname))
                    self.loadedrec=True
                self.actualcat=self.tr('Tags')


                # TAG REFRESH
                for i in reversed(range(self.tagtree.childCount())):
                    self.tagtree.removeChild(self.tagtree.child(i))
                self.tagcontainer.itemChanged.connect(self.handleItemChanged)
                self.tagcontainer.itemSelectionChanged.connect(lambda:self.newpreview(self.actualcat))
                hx=self.ht.gettags()
                for i in hx:
                    child1=QTreeWidgetItem(self.tagtree)
                    child1.setText(0,i)
                    for d in hx[i]:
                        child2=QTreeWidgetItem(child1)
                        child2.setText(0,d.justname)

                # DEVELOPPEMENT REFRESH
                self.actualcat=self.tr('Developement')
                self.devcontainer.itemChanged.connect(self.handleItemChanged)
                self.devcontainer.itemSelectionChanged.connect(lambda:self.newpreview(self.actualcat,dev=True))
                hx=self.ht.projets
                for i in reversed(range(self.devtree.childCount())):
                    self.devtree.removeChild(self.devtree.child(i))
                for i in hx:
                    child1=QTreeWidgetItem(self.devtree)
                    child1.setText(0,i)
                    for d in hx[i]:
                        child2=QTreeWidgetItem(child1)
                        child2.setText(0,d.justname)
            for cat in self.cats:
                self.actualcat=str(cat)
                self.trou[self.actualcat].itemChanged.connect(self.handleItemChanged)
                self.trou[self.actualcat].itemSelectionChanged.connect(lambda:self.newpreview(self.actualcat))

                tro=[]
                for i in reversed(range(self.cou[self.actualcat].childCount())):
                    self.rectree.removeChild(self.cou[self.actualcat].child(i))
                self.develop(cat, self.cou[self.actualcat],0,tro)

            self.catcontent.update()
            self.widget.update()
        for i in reversed(range(self.categories.childCount())):
            self.categories.removeChild(self.categories.child(i))
        for item in self.cats:
            if self.ht.nodes[item].visible:
                self.child[item] = QTreeWidgetItem(self.categories)
                self.child[item].setFlags(self.child[item].flags() )
                self.child[item].setText(0, item)
                self.child[item].setForeground(0, QtGui.QBrush(QtGui.QColor("#a0833f")))

            else:
                self.child[item] = QTreeWidgetItem()
                self.child[item].setFlags(self.child[item].flags() )
                self.child[item].setText(0, item)
                self.child[item].setForeground(0, QtGui.QBrush(QtGui.QColor("#a0833f")))

    def closeEvent(self, event):
        self.ht.save()


    def file_changed(self, path):
        print('File changed ')
        self.notification.setText(self.tr('Updating'))
        s=worker(self.app,self.ht,path,self.configuration)
        self.widget.connect(s, s.signal, self.refresh)
        s.start()

    def directory_changed(self, path):
        print('Directory Changed ! ')
        self.notification.setText(self.tr('Updating'))
        s=worker(self.app,self.ht,path,self.configuration)
        self.widget.connect(s, s.signal, self.refresh)
        s.start()


class worker(QtCore.QThread):
    def __init__(self,app,ht,path,config):
        QtCore.QThread.__init__(self, parent=app)
        self.signal = QtCore.SIGNAL("signal")
        self.app=app
        self.ht=ht
        self.path=str(path)
        self.config=config
    def run(self):
        print('New signal received ! PATH :'+str(self.path))

        if os.path.isdir(self.path):
            for i in self.config.work:
                self.ht.initialize(i)
            self.ht.verify()
            self.emit(self.signal, "finished")
        else:
            path = os.path.abspath(str(self.path))
            parent=os.path.abspath(os.path.join(self.path, os.pardir))
            self.ht.initialize(parent)
            if os.path.isfile(path):
                self.ht.add(path)
            else:
                if self.ht.contains(path):
                    self.ht.delete(path)
                    self.ht.verify()

        self.emit(self.signal, "finished")
#        self.visit()



