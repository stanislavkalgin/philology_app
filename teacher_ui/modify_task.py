import pickle
from global_stuff import possible_figures, Task, TaskFigure, \
    Answer, AnswerFigure
from task_modify_form import Ui_Dialog as Ui_task_modify_form
from deletion_dialog import Ui_deletion_dialog
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import sql_stuff


# Возможно стоило наследовать от формы добавления задания, но когда это пришло в голову, скопировать было уже проще

class ModifyTaskForm(QtWidgets.QDialog):
    def __init__(self, task):
        super().__init__()
        self.ui = Ui_task_modify_form()
        self.ui.setupUi(self)
        self.possible_figures = possible_figures.copy()
        
        keys = []
        for i in self.possible_figures.keys():
            keys.append(i)
        keys.sort()
        for i in range(len(keys)):
            self.ui.figures_buttons_list.addItem(keys[i])
            self.ui.figures_buttons_list.item(i).setForeground(self.possible_figures[keys[i]])

        self.task_text = task.text
        self.task_name = task.name
        self.highlighted_task_text = task.highlighted_text
        self.task_figures_list = task.figuresList
        # блок полей создаваемого оборота, все должно быть обнулено после каждого добавления оборота
        self.logic_figure_to_delete_is_chosen = False
        self.edited_figure_number = None
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_text = ''
        self.edited_figure_possible_symbols_text = ''

        # Загрузка полей изменяемого задания
        self.ui.task_text.setText(self.highlighted_task_text)
        self.ui.task_name_input.setPlainText(self.task_name)
        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))
        self.refresh_widget_list_of_figures()

        # Функционал окна
        self.ui.button_add_key_words.clicked.connect(self.add_key_words)
        self.ui.button_add_possible_words.clicked.connect(self.add_possible_words)
        self.ui.button_add_figure.clicked.connect(self.add_figure_to_list)
        self.ui.figures_buttons_list.itemClicked.connect(self.set_figure_type)
        self.ui.list_widget_of_figures.itemClicked.connect(self.choose_figure_from_list)
        self.ui.button_delete_figure.clicked.connect(self.delete_figure)
        self.ui.button_choose_figure.clicked.connect(self.choose_figure_from_cursor)
        self.ui.button_modify_task.clicked.connect(self.modify_task)
        self.ui.button_delete_task.clicked.connect(self.delete_task)

    def add_key_words(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.edited_figure_key_symbols += range(start, end)  # todo переделать на end + 1 и исправить все что за этим следует
        self.edited_figure_key_symbols_text += cursor.selectedText() + " || "
        # print(sorted(self.edited_figure_key_symbols))
        self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_text)
        char_format = cursor.charFormat()
        char_format.setBackground(possible_figures[self.edited_figure_type])
        cursor.setCharFormat(char_format)

    def add_possible_words(self):  # todo переделать способ задания границ оборотов \\ и вот непонятно, сделано ли уже
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.edited_figure_possible_symbols = [start, end - 1]  # see if causes problems
        self.edited_figure_possible_symbols_text = cursor.selectedText()
        # print(sorted(self.edited_figure_possible_symbols))
        self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_text)

    def set_figure_type(self, item):
        self.edited_figure_type = item.text()
        self.ui.figure_info_type.setText(self.edited_figure_type)

    def add_figure_to_list(self):
        figure = TaskFigure(type=self.edited_figure_type,
                            key_symbols=self.edited_figure_key_symbols,
                            key_symbols_text=self.edited_figure_key_symbols_text,
                            possible_symbols=self.edited_figure_possible_symbols,
                            possible_symbols_text=self.edited_figure_possible_symbols_text)
        self.task_figures_list.append(figure)
        self.set_default_figure_fields()

        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))
        self.refresh_widget_list_of_figures()

    def refresh_widget_list_of_figures(self):
        self.ui.list_widget_of_figures.clear()
        for i in range(len(self.task_figures_list)):
            figure_item = (str(i) + ' ' +
                           self.task_figures_list[i].type + '\n' +
                           self.task_figures_list[i].key_symbols_text[:50])
            self.ui.list_widget_of_figures.addItem(figure_item)

    def choose_figure_from_list(self, item):
        number = int(item.text().split()[0])
        self.logic_figure_to_delete_is_chosen = True
        self.edited_figure_number = number
        self.ui.figure_info_key_words.setText(self.task_figures_list[number].key_symbols_text)
        self.ui.figure_info_possible_words.setText(self.task_figures_list[number].possible_symbols_text)
        self.ui.figure_info_type.setText(self.task_figures_list[number].type)
        # todo диапазон выделения показывать
        # todo заглушение всего кроме удаления
        self.edited_figure_key_symbols = self.task_figures_list[number].key_symbols[:]

    def choose_figure_from_cursor(self):
        cursor = self.ui.task_text.textCursor()
        position = cursor.selectionStart()
        figures_dict = {}
        for i in range(len(self.task_figures_list)):
            symbols_range = tuple(self.task_figures_list[i].key_symbols[:])
            figures_dict.update({symbols_range: i})
        for key in figures_dict.keys():
            if position in key:
                self.edited_figure_number = figures_dict[key]
                self.logic_figure_to_delete_is_chosen = True
                self.ui.figure_info_key_words.setText(self.task_figures_list[self.edited_figure_number].key_symbols_text)
                self.ui.figure_info_possible_words.setText(
                    self.task_figures_list[self.edited_figure_number].possible_symbols_text)
                self.ui.figure_info_type.setText(self.task_figures_list[self.edited_figure_number].type)
                break

    def delete_figure(self):
        if self.logic_figure_to_delete_is_chosen:
            deleted_figure = self.task_figures_list.pop(self.edited_figure_number)
            start = deleted_figure.key_symbols[0]
            end = deleted_figure.key_symbols[-1] + 1
            # print(self.task_figures_list, start, end)
            cursor = self.ui.task_text.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            char_format = cursor.charFormat()
            char_format.setBackground(QtCore.Qt.white)
            cursor.setCharFormat(char_format)
            self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))

            self.refresh_widget_list_of_figures()
            self.set_default_figure_fields()

    def set_default_figure_fields(self):
        self.logic_figure_to_delete_is_chosen = False
        self.edited_figure_number = None
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_text = ''
        self.edited_figure_possible_symbols_text = ''

        self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_text)
        self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_text)
        self.ui.figure_info_type.setText('Тип оборота')

    def modify_task(self):
        self.highlighted_task_text = self.ui.task_text.toHtml()
        new_task_name = self.ui.task_name_input.toPlainText()
        new_task = Task(name=new_task_name,
                        text=self.task_text,
                        highlighted_text=self.highlighted_task_text,
                        figures_list=self.task_figures_list)
        # print(task)
        packed_task = pickle.dumps(new_task)
        if self.task_name == new_task_name:
            query_add_task = '''UPDATE `taskbase` SET `task_object`=%s WHERE `task_name`=%s'''
            insert = (packed_task, self.task_name)
        else:
            query_add_task = '''INSERT INTO taskbase (`task_name`, `task_object`) VALUES (%s,%s)'''
            insert = (new_task_name, packed_task)
        sql_stuff.insert_as_teacher(query_add_task, insert)

    def delete_task(self):
        dialog = DeletionDialog(task_name=self.task_name)
        dialog.exec()


class DeletionDialog(QtWidgets.QDialog):
    def __init__(self, task_name):
        super().__init__()
        self.ui = Ui_deletion_dialog()
        self.ui.setupUi(self)
        self.task_name = task_name
        # self.ui.label.setText(task_name)
        self.ui.button_delete.clicked.connect(self.delete_task)
        self.ui.button_cancel.clicked.connect(self.cancel)

    def delete_task(self):
        query_deletion = '''DELETE FROM `taskbase` WHERE task_name=%s'''
        insert = (self.task_name, )
        sql_stuff.insert_as_teacher(query_deletion, insert)
        self.ui.label.setText('Удалено')

    def cancel(self):
        self.close()


if __name__ == '__main__':
    task_tup = sql_stuff.get_answer_as_teacher('''SELECT task_object FROM taskbase WHERE task_name=\'Тест 1\'''')
    task_packed = task_tup[0][0]
    task1 = pickle.loads(task_packed)
    app = QtWidgets.QApplication([])
    application = ModifyTaskForm(task1)
    application.show()

    sys.exit(app.exec())
