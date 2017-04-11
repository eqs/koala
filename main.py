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
from PyQt5 import QtCore 

BUTTON_CONFIG = [
    {
         'key' : 'A', 
         'class' : 'dipping_gestures'
    }, 
    {
         'key' : 'S', 
         'class' : 'other_gestures'
    },
    {
         'key' : 'D',
         'class' : 'other_things'
    }
]

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # Initialize main-widgets
        
        # 画像をスライドするボタンの設定
        self.prevButton = QPushButton('&Prev')
        self.prevButton.clicked.connect(self.showPrevImage)
        self.prevButton.setShortcut(QtCore.Qt.Key_Left)
        
        self.nextButton = QPushButton('&Next')
        self.nextButton.clicked.connect(self.showNextImage)
        self.nextButton.setShortcut(QtCore.Qt.Key_Right)
        
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.prevButton, 0, 0)
        buttonLayout.addWidget(self.nextButton, 0, 1)
        
        # 画像を表示するラベルの設定
        self.pictureLabel = QLabel()
        self.pictureLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.putPixmap('usagi.jpg')
        
        self.pathLabel = QLabel('')
        self.pathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.classLabel = QLabel('')
        self.classLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        pictureLayout = QGridLayout()
        pictureLayout.addWidget(self.pictureLabel, 0, 0)
        pictureLayout.addWidget(self.pathLabel, 1, 0)
        pictureLayout.addWidget(self.classLabel, 2, 0)
        
        # アノテーションをするためのボタンの設定
        annotationButtonLayout = QGridLayout()
        for k, conf in enumerate(BUTTON_CONFIG):
            button = QPushButton('&{0} : {1}'.format(conf['class'], conf['key']))
            button.clicked.connect(self.anotateClass)
            button.setShortcut(conf['key'])
            annotationButtonLayout.addWidget(button, 0, k)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(pictureLayout)
        mainLayout.addLayout(annotationButtonLayout)
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
        
        # Initialize image annotation infomation list
        self.imageDataList = []
        self.imageIndex = 0
    
    def putPixmap(self, filepath):
        # Pixmapをパスから読み込んでラベルにセットする
        pixmap = QPixmap(filepath)
        self.pictureLabel.setPixmap(pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio))
        self.pictureLabel.show()
    
    def anotateClass(self):
        # 押されたボタンの情報から，ラベリングを行う
        if len(self.imageDataList) > 0:
            text = self.sender().text()
            dataClass = text[1:text.index(':')-1].strip()
            self.imageDataList[self.imageIndex]['class'] = dataClass
            self.updateDataInformation()
    
    def updateDataInformation(self):
        # 現在選択しているデータのパスとクラスをラベルに表示する
        if len(self.imageDataList) > 0:
            self.pathLabel.setText(self.imageDataList[self.imageIndex]['filepath'])
            self.classLabel.setText(self.imageDataList[self.imageIndex]['class'])
    
    def showPrevImage(self):
        if len(self.imageDataList) > 0:
            self.imageIndex = (self.imageIndex - 1) % len(self.imageDataList)
            self.putPixmap(self.imageDataList[self.imageIndex]['filepath'])
            self.updateDataInformation()
    
    def showNextImage(self):
        if len(self.imageDataList) > 0:
            self.imageIndex = (self.imageIndex + 1) % len(self.imageDataList)
            self.putPixmap(self.imageDataList[self.imageIndex]['filepath'])
            self.updateDataInformation()
        
    def openAnnotationFile(self):
        QFileDialog.getOpenFileName(parent=self, filter='*.json')
    
    def saveAnnotationFile(self):
        print('Save')
        print(self.imageDataList)
    
    def addImageFile(self):
        # Open file dialog for adding images
        selectedImagePathList = QFileDialog.getOpenFileNames(parent=self, filter='*.png *.jpg *.jpeg *.bmp')[0]
        # Image path list
        imagePathList = [imageData['filepath'] for imageData in self.imageDataList]
        # Add selected images to imagePathList 
        for imagePath in selectedImagePathList:
            # まだ追加されていない画像ならリストに追加する
            if not (imagePath in imagePathList):
                self.imageDataList.append({'filepath' : imagePath, 'class' : None})
        
        # 画像があるなら開く
        if len(self.imageDataList) > 0:
            self.imageIndex = len(self.imageDataList) - 1
            self.putPixmap(self.imageDataList[self.imageIndex]['filepath'])
            self.updateDataInformation()
            
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    app.exec_()
    