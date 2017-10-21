# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fin.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Allows QLineEdit to have a clicked event.
class ClickLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)

class Ui_Form(QDialog):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.setFixedSize(756, 182)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        Form.setWindowIcon(QtGui.QIcon('assets\icon.png'))
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(14, 25, 511, 61))
        self.label_1.setMaximumSize(QtCore.QSize(511, 61))
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap("assets\image_box.png"))
        self.label_1.setObjectName("label_1")
        self.addressBox = ClickLineEdit(Form)
        self.addressBox.setGeometry(QtCore.QRect(20, 40, 492, 35))
        self.addressBox.setMaximumSize(QtCore.QSize(492, 35))
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(14)
        self.addressBox.setFont(font)
        self.addressBox.setStyleSheet("border: none;\n""color: rgb(46, 169, 211);\n""font: 14pt Open Sans Light;")
        self.addressBox.setObjectName("addressBox")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(14, 97, 511, 61))
        self.label_2.setMaximumSize(QtCore.QSize(511, 61))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets\image_box.png"))
        self.label_2.setObjectName("label_2")
        self.nameBox = ClickLineEdit(Form)
        self.nameBox.setGeometry(QtCore.QRect(20, 111, 492, 35))
        self.nameBox.setMaximumSize(QtCore.QSize(492, 35))
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(14)
        self.nameBox.setFont(font)
        self.nameBox.setStyleSheet("border: none;\n""color: rgb(46, 169, 211);\n""font: 14pt Open Sans Light;")
        self.nameBox.setObjectName("nameBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(530, 30, 211, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.updateButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.updateButton.setMaximumSize(QtCore.QSize(209, 45))

        self.updateButton.setStyleSheet("QPushButton{border-image: url(assets/button_update_data.png);}" + 
        								"QPushButton:pressed {border-image: url(assets/between_update.png)}" +
        								"QPushButton:!enabled {border-image: url(assets/disabled_update_data.png)}")
        self.updateButton.setText("")
        icon = QtGui.QIcon()
        self.updateButton.setIcon(icon)
        self.updateButton.setIconSize(QtCore.QSize(240, 800))
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)
        self.createButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.createButton.setMaximumSize(QtCore.QSize(209, 45))
        self.createButton.setStyleSheet("QPushButton{border-image: url(assets/button_create_report.png);}" +
        								"QPushButton:pressed {border-image: url(assets/between_create.png)}" +
        								"QPushButton:!enabled {border-image: url(assets/disabled_create_report.png)}")
        self.createButton.setText("")
        icon1 = QtGui.QIcon()
        self.createButton.setIcon(icon1)
        self.createButton.setIconSize(QtCore.QSize(240, 800))
        self.createButton.setObjectName("createButton")
        self.verticalLayout.addWidget(self.createButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Weather Data Analysis Application"))
        self.addressBox.setText("Enter your address for a weather update") 
        self.nameBox.setText("Enter a name for the weather report file")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())