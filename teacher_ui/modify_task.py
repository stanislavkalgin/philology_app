import pickle
from global_stuff import Task
from task_modify_form import Ui_Dialog as Ui_task_modify_form
from teacher import AddTaskForm
from deletion_dialog import Ui_deletion_dialog
from PyQt5 import QtWidgets
import sys
import sql_stuff


class ModifyTaskForm(AddTaskForm):
    def __init__(self, task):
        super().__init__(ui=Ui_task_modify_form)

        # Здесь блок полей создаваемого задания берется из объекта
        self.task_text = task.text
        self.task_name = task.name
        self.highlighted_task_text = task.highlighted_text
        self.task_figures_list = task.figuresList

        # Переменные состояния для удаления оборотов, todo сделать умнее и лучше
        self.figure_to_delete_is_chosen = False
        self.deletion_figure_number = None

        # Загрузка полей изменяемого задания
        self.ui.task_text.setText(self.highlighted_task_text)
        self.ui.task_name_input.setPlainText(self.task_name)
        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))
        self.refresh_widget_list_of_figures()

        # Расширение функционала окна
        self.ui.list_widget_of_figures.itemClicked.connect(self.choose_figure_from_list)
        self.ui.button_delete_figure.clicked.connect(self.delete_figure)
        self.ui.button_choose_figure.clicked.connect(self.choose_figure_from_cursor)
        self.ui.button_modify_task.clicked.connect(self.modify_task)
        self.ui.button_delete_task.clicked.connect(self.delete_task)

        self.set_window_state()

    def set_window_state(self):
        self._set_window_state()

        if self.figure_to_delete_is_chosen:
            self.ui.button_delete_figure.setEnabled(True)
        else:
            self.ui.button_delete_figure.setEnabled(False)

    def add_figure_to_list(self):
        AddTaskForm.add_figure_to_list(self)
        self.refresh_widget_list_of_figures()

    def refresh_widget_list_of_figures(self):
        self.ui.list_widget_of_figures.clear()
        for i in range(len(self.task_figures_list)):
            figure_item = (str(i) + ' ' +
                           self.task_figures_list[i].figure_type + '\n' +
                           self.task_figures_list[i].key_symbols_text[:50])
            self.ui.list_widget_of_figures.addItem(figure_item)

    def choose_figure_from_list(self, item):
        number = int(item.text().split()[0])
        self.figure_to_delete_is_chosen = True
        self.deletion_figure_number = number
        self.ui.figure_info_key_words.setText(self.task_figures_list[number].key_symbols_text)
        self.ui.figure_info_possible_words.setText(self.task_figures_list[number].possible_symbols_text)
        self.ui.figure_info_type.setText(self.task_figures_list[number].figure_type)
        # todo диапазон выделения показывать
        # todo заглушение всего кроме удаления
        self.edited_figure_key_symbols = self.task_figures_list[number].key_symbols[:]
        self.set_window_state()

    def choose_figure_from_cursor(self):
        cursor = self.ui.task_text.textCursor()
        position = cursor.selectionStart()
        figures_dict = {}
        for i in range(len(self.task_figures_list)):
            symbols_range = tuple(self.task_figures_list[i].key_symbols[:])
            figures_dict.update({symbols_range: i})
        for key in figures_dict.keys():
            if position in key:
                self.deletion_figure_number = figures_dict[key]
                self.figure_to_delete_is_chosen = True
                self.ui.figure_info_key_words.setText(self.task_figures_list[self.deletion_figure_number].key_symbols_text)
                self.ui.figure_info_possible_words.setText(
                    self.task_figures_list[self.deletion_figure_number].possible_symbols_text)
                self.ui.figure_info_type.setText(self.task_figures_list[self.deletion_figure_number].figure_type)
                break
        self.set_window_state()

    def delete_figure(self):
        if self.figure_to_delete_is_chosen:
            deleted_figure = self.task_figures_list.pop(self.deletion_figure_number)
            self.whiten_text_from_figure(deleted_figure)
            self.refresh_widget_list_of_figures()
            self.set_default_figure_fields()
        self.set_window_state()

    def set_default_figure_fields(self):
        AddTaskForm.set_default_figure_fields(self)
        self.figure_to_delete_is_chosen = False
        self.deletion_figure_number = None

    def modify_task(self):
        self.highlighted_task_text = self.ui.task_text.toHtml()
        new_task_name = self.ui.task_name_input.toPlainText()
        new_task = Task(name=new_task_name,
                        text=self.task_text,
                        highlighted_text=self.highlighted_task_text,
                        figures_list=self.task_figures_list)
        packed_task = pickle.dumps(new_task)
        if self.task_name == new_task_name:
            query_add_task = '''UPDATE `taskbase` SET `task_object`=%s WHERE `task_name`=%s'''
            insert = (packed_task, self.task_name)
        else:
            query_add_task = '''INSERT INTO taskbase (`task_name`, `task_object`) VALUES (%s,%s)'''
            insert = (new_task_name, packed_task)
        try:
            sql_stuff.insert_as_teacher(query_add_task, insert)
            self.ui.figure_info_type.setText('Задание отредактировано')
        except Exception as exc:
            self.ui.figure_info_type.setText('Ошибка базы данных')
            filename = (new_task_name or packed_task) + '.txt'
            with open(filename, 'a') as task_object_file:
                task_object_file.write(str(packed_task))

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
