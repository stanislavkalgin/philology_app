# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_modify_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(809, 704)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Иконки/icons8-add-book-80.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.button_add_figure = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_figure.sizePolicy().hasHeightForWidth())
        self.button_add_figure.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_add_figure.setFont(font)
        self.button_add_figure.setObjectName("button_add_figure")
        self.verticalLayout_3.addWidget(self.button_add_figure)
        self.button_modify_task = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_modify_task.sizePolicy().hasHeightForWidth())
        self.button_modify_task.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_modify_task.setFont(font)
        self.button_modify_task.setObjectName("button_modify_task")
        self.verticalLayout_3.addWidget(self.button_modify_task)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.task_text = QtWidgets.QTextEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.task_text.setFont(font)
        self.task_text.setReadOnly(True)
        self.task_text.setObjectName("task_text")
        self.gridLayout_2.addWidget(self.task_text, 0, 0, 1, 1)
        self.figure_info = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.figure_info.sizePolicy().hasHeightForWidth())
        self.figure_info.setSizePolicy(sizePolicy)
        self.figure_info.setMaximumSize(QtCore.QSize(16777215, 150))
        self.figure_info.setObjectName("figure_info")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.figure_info)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.figure_info_key_words = QtWidgets.QTextBrowser(self.figure_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.figure_info_key_words.setFont(font)
        self.figure_info_key_words.setAcceptRichText(False)
        self.figure_info_key_words.setObjectName("figure_info_key_words")
        self.horizontalLayout.addWidget(self.figure_info_key_words)
        self.figure_info_type = QtWidgets.QLabel(self.figure_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.figure_info_type.sizePolicy().hasHeightForWidth())
        self.figure_info_type.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.figure_info_type.setFont(font)
        self.figure_info_type.setAlignment(QtCore.Qt.AlignCenter)
        self.figure_info_type.setObjectName("figure_info_type")
        self.horizontalLayout.addWidget(self.figure_info_type)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.figure_info_possible_words = QtWidgets.QTextBrowser(self.figure_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.figure_info_possible_words.setFont(font)
        self.figure_info_possible_words.setAcceptRichText(False)
        self.figure_info_possible_words.setObjectName("figure_info_possible_words")
        self.verticalLayout_2.addWidget(self.figure_info_possible_words)
        self.gridLayout_2.addWidget(self.figure_info, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.figures_buttons_list = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.figures_buttons_list.setFont(font)
        self.figures_buttons_list.setObjectName("figures_buttons_list")
        self.verticalLayout.addWidget(self.figures_buttons_list)
        self.figures_counter_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.figures_counter_label.sizePolicy().hasHeightForWidth())
        self.figures_counter_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.figures_counter_label.setFont(font)
        self.figures_counter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.figures_counter_label.setObjectName("figures_counter_label")
        self.verticalLayout.addWidget(self.figures_counter_label)
        self.button_add_key_words = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_key_words.sizePolicy().hasHeightForWidth())
        self.button_add_key_words.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_add_key_words.setFont(font)
        self.button_add_key_words.setObjectName("button_add_key_words")
        self.verticalLayout.addWidget(self.button_add_key_words)
        self.button_add_possible_words = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_possible_words.sizePolicy().hasHeightForWidth())
        self.button_add_possible_words.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_add_possible_words.setFont(font)
        self.button_add_possible_words.setObjectName("button_add_possible_words")
        self.verticalLayout.addWidget(self.button_add_possible_words)
        self.task_name_input = QtWidgets.QPlainTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task_name_input.sizePolicy().hasHeightForWidth())
        self.task_name_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.task_name_input.setFont(font)
        self.task_name_input.setReadOnly(True)
        self.task_name_input.setObjectName("task_name_input")
        self.verticalLayout.addWidget(self.task_name_input)
        self.button_choose_figure = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_choose_figure.sizePolicy().hasHeightForWidth())
        self.button_choose_figure.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_choose_figure.setFont(font)
        self.button_choose_figure.setObjectName("button_choose_figure")
        self.verticalLayout.addWidget(self.button_choose_figure)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 1)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.list_widget_of_figures = QtWidgets.QListWidget(Dialog)
        self.list_widget_of_figures.setObjectName("list_widget_of_figures")
        self.gridLayout_2.addWidget(self.list_widget_of_figures, 0, 2, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.button_delete_figure = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_delete_figure.sizePolicy().hasHeightForWidth())
        self.button_delete_figure.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_delete_figure.setFont(font)
        self.button_delete_figure.setObjectName("button_delete_figure")
        self.verticalLayout_4.addWidget(self.button_delete_figure)
        self.button_delete_task = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_delete_task.sizePolicy().hasHeightForWidth())
        self.button_delete_task.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_delete_task.setFont(font)
        self.button_delete_task.setObjectName("button_delete_task")
        self.verticalLayout_4.addWidget(self.button_delete_task)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 1, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 10)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 4)
        self.gridLayout_2.setRowStretch(0, 10)
        self.gridLayout_2.setRowStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Редактирование задания"))
        self.button_add_figure.setText(_translate("Dialog", "Добавить оборот"))
        self.button_modify_task.setText(_translate("Dialog", "Завершить\n"
"редактирование\n"
"задания"))
        self.task_text.setPlaceholderText(_translate("Dialog", "Введите текст задания"))
        self.figure_info.setTitle(_translate("Dialog", "Информация о выбранном или добавляемом обороте"))
        self.figure_info_key_words.setPlaceholderText(_translate("Dialog", "Ключевые слова"))
        self.figure_info_type.setText(_translate("Dialog", "Тип оборота"))
        self.figure_info_possible_words.setPlaceholderText(_translate("Dialog", "Диапазон выделения"))
        self.figures_counter_label.setText(_translate("Dialog", "Оборотов добавлено:\n"
"0"))
        self.button_add_key_words.setText(_translate("Dialog", "Добавить\n"
"ключевые слова"))
        self.button_add_possible_words.setText(_translate("Dialog", "Добавить\n"
"диапазон выделения"))
        self.task_name_input.setPlaceholderText(_translate("Dialog", "Название задания"))
        self.button_choose_figure.setText(_translate("Dialog", "Выбрать оборот"))
        self.button_delete_figure.setText(_translate("Dialog", "Удалить\n"
"выбранный оборот"))
        self.button_delete_task.setText(_translate("Dialog", "Удалить задание"))
