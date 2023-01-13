''' Main Class
Running Program
'''
#Libraries
from AppDemo import AppDemo
from PyQt5 import  QtGui, QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())