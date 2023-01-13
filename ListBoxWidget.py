from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl, QRect
import base64
from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.encoders
import mimetypes
import os

class ListBoxWidget(QtWidgets.QListWidget):
    ''' Methods of ListBoxWidget
    Args:
        QListWidget: A class that allows to drag file to this box and temporarily save its File root.
    '''
    def _init_(self, parent = None):
        super()._init_(parent)
        self.setAcceptDrops(True)
        self.resize(200,200)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)          
        else:
            event.ignore()