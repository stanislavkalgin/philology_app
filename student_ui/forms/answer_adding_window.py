# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'answer_adding_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_answer_edit_window(object):
    def setupUi(self, answer_edit_window):
        answer_edit_window.setObjectName("answer_edit_window")
        answer_edit_window.resize(976, 694)
        self.gridLayout = QtWidgets.QGridLayout(answer_edit_window)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.figures_buttons_list = QtWidgets.QListWidget(answer_edit_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.figures_buttons_list.setFont(font)
        self.figures_buttons_list.setObjectName("figures_buttons_list")
        self.verticalLayout.addWidget(self.figures_buttons_list)
        self.label_chosen_figure_type = QtWidgets.QLabel(answer_edit_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_chosen_figure_type.sizePolicy().hasHeightForWidth())
        self.label_chosen_figure_type.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_chosen_figure_type.setFont(font)
        self.label_chosen_figure_type.setAlignment(QtCore.Qt.AlignCenter)
        self.label_chosen_figure_type.setObjectName("label_chosen_figure_type")
        self.verticalLayout.addWidget(self.label_chosen_figure_type)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.figures_browser = QtWidgets.QTextBrowser(answer_edit_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.figures_browser.setFont(font)
        self.figures_browser.setObjectName("figures_browser")
        self.gridLayout.addWidget(self.figures_browser, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_add_figure = QtWidgets.QPushButton(answer_edit_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_figure.sizePolicy().hasHeightForWidth())
        self.button_add_figure.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_add_figure.setFont(font)
        self.button_add_figure.setObjectName("button_add_figure")
        self.verticalLayout_2.addWidget(self.button_add_figure)
        self.button_finish_task = QtWidgets.QPushButton(answer_edit_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_finish_task.sizePolicy().hasHeightForWidth())
        self.button_finish_task.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_finish_task.setFont(font)
        self.button_finish_task.setObjectName("button_finish_task")
        self.verticalLayout_2.addWidget(self.button_finish_task)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.task_text = QtWidgets.QTextEdit(answer_edit_window)
        self.task_text.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.task_text.setObjectName("task_text")
        self.gridLayout.addWidget(self.task_text, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(answer_edit_window)
        QtCore.QMetaObject.connectSlotsByName(answer_edit_window)

    def retranslateUi(self, answer_edit_window):
        _translate = QtCore.QCoreApplication.translate
        answer_edit_window.setWindowTitle(_translate("answer_edit_window", "Составление ответа на задание"))
        self.label_chosen_figure_type.setText(_translate("answer_edit_window", "Оборот"))
        self.figures_browser.setPlaceholderText(_translate("answer_edit_window", "Добавленные обороты"))
        self.button_add_figure.setText(_translate("answer_edit_window", "Добавить\n"
"оборот"))
        self.button_finish_task.setText(_translate("answer_edit_window", "Готово"))