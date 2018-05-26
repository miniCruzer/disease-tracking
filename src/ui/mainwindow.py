# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(822, 658)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/health.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filterEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filterEdit.setText("")
        self.filterEdit.setClearButtonEnabled(True)
        self.filterEdit.setObjectName("filterEdit")
        self.verticalLayout_2.addWidget(self.filterEdit)
        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setObjectName("table")
        self.verticalLayout_2.addWidget(self.table)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.incBtn = QtWidgets.QPushButton(self.centralwidget)
        self.incBtn.setObjectName("incBtn")
        self.verticalLayout.addWidget(self.incBtn)
        self.decBtn = QtWidgets.QPushButton(self.centralwidget)
        self.decBtn.setObjectName("decBtn")
        self.verticalLayout.addWidget(self.decBtn)
        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout.addWidget(self.addBtn)
        self.delBtn = QtWidgets.QPushButton(self.centralwidget)
        self.delBtn.setObjectName("delBtn")
        self.verticalLayout.addWidget(self.delBtn)
        self.saveBtn = QtWidgets.QPushButton(self.centralwidget)
        self.saveBtn.setObjectName("saveBtn")
        self.verticalLayout.addWidget(self.saveBtn)
        self.undoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.undoBtn.setObjectName("undoBtn")
        self.verticalLayout.addWidget(self.undoBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 822, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionLicense)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Disease Tracking"))
        self.filterEdit.setPlaceholderText(_translate("MainWindow", "Filter"))
        self.incBtn.setText(_translate("MainWindow", "++"))
        self.decBtn.setText(_translate("MainWindow", "--"))
        self.addBtn.setText(_translate("MainWindow", "Add Row"))
        self.delBtn.setText(_translate("MainWindow", "Delete Row"))
        self.saveBtn.setText(_translate("MainWindow", "Save"))
        self.undoBtn.setText(_translate("MainWindow", "Undo"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionExport.setText(_translate("MainWindow", "Export"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

