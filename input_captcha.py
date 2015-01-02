# -*- coding: utf-8 -*- 
import sys
from PyQt4 import QtGui, QtCore
img = sys.argv[1]
app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget();
text, ok = QtGui.QInputDialog.getText(window, u'http://uh.ru', u'Введите текст с картинки<br><center><img src="'+img+'"></center>')
if ok and str(text) != "":
  sys.stdout.write(str(text))
else:
  sys.stdout.write("None")
  #sys.exit(app.exec_())