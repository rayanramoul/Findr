from PyQt4 import QtCore, QtGui
import sys, time
from QNotifications import QNotificationArea
from BackEnd.Config import Config
import os
from os.path import expanduser

class Asking():
    def __init__(self,app):
        self.configuration=Config()
        self.main_window = QtGui.QMainWindow()
        self.widget=QtGui.QWidget()
        self.but=QtGui.QPushButton()

        self.app = app

        translator = QtCore.QTranslator()
        langue=QtCore.QLocale()
        if 'fr' in langue.name():
            lang = 'Français'
        elif 'ar' in langue.name():
            lang = 'Arabic'
        else:
            lang = 'English'

        translator.load(os.path.join('translate',lang.lower()+'ask.qm'))

        self.app.installTranslator(translator)

        self.but.setText(self.app.tr('Confirm '))
        self.but.setStyleSheet('background-color:#dd6d00;color:white;')
        self.main_window.setCentralWidget(self.widget)
        pic = QtGui.QLabel()
        pic.resize(500, 300)
        pic.setPixmap(QtGui.QPixmap(os.path.join('resources','full.png')))

        self.choice=QtGui.QLabel()
        self.configuration.path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
        self.choice.setText(self.app.tr('Language'))

        self.lang=QtGui.QComboBox()
        self.lang.addItem(lang)
        for i in ['English','Français','العربية']:
            if i!=lang:
                self.lang.addItem(i)
        self.question=QtGui.QLabel()

        self.question.setText(self.app.tr('Are you a developper ?'))
        self.devyes=QtGui.QRadioButton(self.app.tr('Yes'))
        self.devno=QtGui.QRadioButton(self.app.tr('No'))
        self.devno.setChecked(True)

        self.vbox=QtGui.QVBoxLayout()
        self.widget.setLayout(self.vbox)
#        qna = QNotificationArea(self.vbox)
#        qna.display('This is a primary notification', 'primary', 1000)

        self.pick=QtGui.QPushButton(self.app.tr('Choose the folders Findr will consider'))
        self.pick.clicked.connect(self.addfile)
        self.reset=QtGui.QPushButton(self.app.tr('Reset'))
        self.directories=QtGui.QListWidget()
        self.directories.resize(50,100)
        self.reset.clicked.connect(self.directories.clear)

        self.vbox.addWidget(pic)
        self.vbox.addWidget(self.choice)
        self.vbox.addWidget(self.lang)
        self.vbox.addWidget(self.question)
        self.vbox.addWidget(self.devno)
        self.vbox.addWidget(self.devyes)
        self.vbox.addWidget(self.pick)
        self.vbox.addWidget(self.reset)
        self.vbox.addWidget(self.directories)
        self.vbox.addWidget(self.but)
        self.but.clicked.connect(self.savingconfig)
        self.widget.setStyleSheet('background-color:#24263d;')
        self.main_window.setGeometry(400,200,300,600)
        self.main_window.setFixedSize(300,600)

    def addfile(self):
        try:
            tom=str(QtGui.QFileDialog.getExistingDirectory(self.widget, self.app.tr('Choose a Folder'), expanduser("~"),QtGui.QFileDialog.ShowDirsOnly))
        except:
            tom = str(QtGui.QFileDialog.getExistingDirectory(self.widget, self.app.tr('Choose a Folder'), expanduser('C:\ '),QtGui.QFileDialog.ShowDirsOnly))
        if tom!='' and tom!=' ':
            self.directories.addItem(tom)

    def savingconfig(self):
        for i in range(self.directories.count()):
            self.configuration.work.append(str(self.directories.item(i).text()))
        self.configuration.language=self.lang.currentText()
        if self.devno.isChecked():
            self.configuration.developper=False
        else:
            self.configuration.developper=True
        self.configuration.save()
        self.main_window.close()