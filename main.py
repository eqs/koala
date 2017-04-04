# -*- coding: utf-8 -*-
"""
Created on 04/04/17 17:17:41

Lite Image Annotation Tool : koala

@author: eqs
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, 
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QAction)
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Initialize main-widget
        self.prevButton = QPushButton('&Prev')
        self.prevButton.clicked.connect(self.showPrevImage)
        self.prevButton.setShortcut('H')
        
        self.nextButton = QPushButton('&Next')
        self.nextButton.clicked.connect(self.showNextImage)
        self.nextButton.setShortcut('L')
        
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.prevButton, 0, 0)
        buttonLayout.addWidget(self.nextButton, 0, 1)
        
        pictureLabel = QLabel()
        pictureLabel.setPixmap(QPixmap('usagi.jpg'))
        pictureLabel.show()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(pictureLabel)
        mainLayout.addLayout(buttonLayout)
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle('koala')
        
        # Initialize menu bar and status bar
        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open annotation file')
        openAction.triggered.connect(self.openAnnotationFile)
        
        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save annotation file')
        saveAction.triggered.connect(self.saveAnnotationFile)
        
        addImageAction = QAction('&Add Image', self)
        addImageAction.setShortcut('Ctrl+I')
        addImageAction.setStatusTip('Add image files')
        addImageAction.triggered.connect(self.addImageFile)
        
        self.statusBar()
        
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(addImageAction)

    def showPrevImage(self):
        print('Prev')
    
    def showNextImage(self):
        print('Next')
        
    def openAnnotationFile(self):
        print(QFileDialog.getOpenFileName(parent=self, filter='*.json'))
    
    def saveAnnotationFile(self):
        print('Save')
    
    def addImageFile(self):
        print(QFileDialog.getOpenFileNames(parent=self, filter='*.png *.jpg *.jpeg *.bmp'))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
    