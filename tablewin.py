# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablewin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Table")
        Table.resize(547, 867)
        font = QtGui.QFont()
        font.setPointSize(11)
        Table.setFont(font)
        self.tableWidget = QtWidgets.QTableWidget(Table)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 531, 781))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.pushButton = QtWidgets.QPushButton(Table)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Table)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 20, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Table)
        self.label.setGeometry(QtCore.QRect(190, 20, 211, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "表格"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Table", "序号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Table", "面积"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Table", "平均荧光"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Table", "最小荧光"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Table", "最大荧光"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Table", "总荧光"))
        self.pushButton.setText(_translate("Table", "全选"))
        self.pushButton_2.setText(_translate("Table", "全不选"))
        self.label.setText(_translate("Table", "总共有细胞核个数"))
