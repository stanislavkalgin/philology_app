# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deletion_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_deletion_dialog(object):
    def setupUi(self, deletion_dialog):
        deletion_dialog.setObjectName("deletion_dialog")
        deletion_dialog.resize(308, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(deletion_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(deletion_dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_delete = QtWidgets.QPushButton(deletion_dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_delete.setFont(font)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        self.button_cancel = QtWidgets.QPushButton(deletion_dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_cancel.setFont(font)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(deletion_dialog)
        QtCore.QMetaObject.connectSlotsByName(deletion_dialog)

    def retranslateUi(self, deletion_dialog):
        _translate = QtCore.QCoreApplication.translate
        deletion_dialog.setWindowTitle(_translate("deletion_dialog", "Точно-точно?"))
        self.label.setText(_translate("deletion_dialog", "Удалить задание и все ответы на него?"))
        self.button_delete.setText(_translate("deletion_dialog", "Удалить"))
        self.button_cancel.setText(_translate("deletion_dialog", "Отменить"))