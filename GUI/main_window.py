# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WIndowTopUI_2OpbCfJ.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(487, 300)
        MainWindow.setAnimated(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 20, 181, 51))
        self.pushButton.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";\n"
"")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 90, 181, 51))
        self.pushButton_2.setStyleSheet(u"\n"
"font: 11pt \"Microsoft YaHei UI\";")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 160, 181, 51))
        self.pushButton_3.setStyleSheet(u"\n"
"font: 11pt \"Microsoft YaHei UI\";")
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 230, 181, 51))
        self.pushButton_4.setStyleSheet(u"\n"
"font: 11pt \"Microsoft YaHei UI\";")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(240, 40, 161, 19))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(240, 80, 211, 31))
        self.comboBox.setEditable(False)
        self.comboBox.setFrame(True)
        self.comboBox.setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.checkBox.clicked["bool"].connect(self.comboBox.setVisible)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WindowTop", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"窗口置顶", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"取消窗口置顶", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"运行", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"打开文件所在的位置", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"使用 Z-order 进行置顶", None))
       
    # retranslateUi


if __name__ == '__main__':
    # test
    import sys
    from PySide6 import QtWidgets

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())