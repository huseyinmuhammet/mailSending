#Libraries
import sys, os 
from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl, QRect
from Google import Create_Service
from ListBoxWidget import ListBoxWidget
import base64
from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.encoders
import mimetypes
import os

class AppDemo(QtWidgets.QMainWindow):
    def getSelectedItem(self):
        if not self.listbox_view.currentItem():
                msg1 = QMessageBox()
                msg1.setWindowTitle('Hata')
                msg1.setText("Lütfen bir dosya seçiniz! ")
                msg1.setIcon(QMessageBox.Critical)
                x = msg1.exec_() 
                return 
        else:
                self.item = QtWidgets.QListWidgetItem(self.listbox_view.currentItem())
                self.url = self.item.text()
           
                #print(self.url)
                #print(self.mailInput.text())
        
                self.sendMail()
                return self.item.text()
    def sendMail(self):
            CLIENT_SECRET_FILE = 'credentials.json'
            API_NAME = 'gmail'
            API_VERSION = 'v1'
            SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic/']

            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

            emailMsg = 'Ödemeniz için tesekkür ederiz.\n Dekontunuz ektedir.\n Saygilarimizla.'
            mimeMessage = MIMEMultipart()
            #Variable Yollanacak kisi
            if not self.mailInput.text():
                msg = QMessageBox()
                msg.setWindowTitle('Hata')
                msg.setText("Lütfen mail adresini bos birakmayiniz! ")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_() 
            else:
                mimeMessage['to'] = self.mailInput.text()
                mimeMessage['subject'] = 'Dekontunuz'
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))

                file_attachments = [self.url]
                for attachment in file_attachments:
                    content_type, encoding = mimetypes.guess_type(attachment)
                    main_type, sub_type = content_type.split('/',1)
                    file_name = os.path.basename(attachment)

                    f = open(attachment,'rb')

                    myFile = MIMEBase(main_type, sub_type)
                    myFile.set_payload(f.read())
                    myFile.add_header('Content-Disposition','attachment', filename= file_name)
                    email.encoders.encode_base64(myFile)
    
                    f.close()
    
                    mimeMessage.attach(myFile)
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()    
                if message['labelIds'][0] == 'SENT':
                    msgBasarili = QMessageBox()
                    msgBasarili.setWindowTitle('Yollandi')
                    msgBasarili.setText("Basarili bir sekilde yollandi.")
                    x = msgBasarili.exec_()
                else:
                    msgBasarisiz = QMessageBox()
                    msgBasarisiz.setWindowTitle('Basarisiz')
                    msgBasarisiz.setText("Bir aksilik olustu")
                    msgBasarisiz.setIcon(QMessageBox.Critical)
                    x = msgBasarisiz.exec_()
    def _init_(self):
        super()._init_()
        self.resize(500,300)
        self. setWindowTitle('Mail Yollama Programi')
        self.listbox_view = ListBoxWidget(self)

        self.url = str

        self.maiLabel = QtWidgets.QLabel("Mail Adresini Giriniz :", self)
        self.maiLabel.setGeometry(QRect(230, 30, 200, 20))

        self.mailInput = QtWidgets.QLineEdit(self)
        self.mailInput.move(230, 60)
        self.mailInput.resize(200, 30)
        
        
        self.btn = QtWidgets.QPushButton('Yolla', self)
        self.btn.setGeometry(280, 130, 100, 50)
        self.btn.clicked.connect(self.getSelectedItem)