import pickle
from global_stuff import possible_figures, Task, TaskFigure
from task_add_form import Ui_Dialog
from checking_answers_form import Ui_check_answers_window
from dialog_text import Ui_Dialog as Ui_text_window  # Иначе конфликт имен, можно переделать в ui файле
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import sql_stuff

# TODO добавить везде предупреждения о потенциальном исключении


class AddTaskForm(QtWidgets.QDialog):
    def __init__(self, parent=None, ui=Ui_Dialog):
        super().__init__(parent)
        self.ui = ui()
        self.ui.setupUi(self)
        self.possible_figures = possible_figures.copy()

        keys = []
        for i in self.possible_figures.keys():
            keys.append(i)
        keys.sort()
        for i in range(len(keys)):
            self.ui.figures_buttons_list.addItem(keys[i])
            self.ui.figures_buttons_list.item(i).setForeground(self.possible_figures[keys[i]])

        # блок полей создаваемого задания
        self.task_text = None
        self.highlighted_task_text = None
        self.task_name = None
        self.task_figures_list = []
        # блок полей создаваемого оборота, все должно быть обнулено после каждого добавления оборота
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_text = ''
        self.edited_figure_possible_symbols_text = ''
        # функционал окна
        self.ui.button_add_key_words.clicked.connect(self.add_key_words)
        self.ui.button_add_possible_words.clicked.connect(self.add_possible_words)
        self.ui.button_add_figure.clicked.connect(self.add_figure_to_list)
        self.ui.figures_buttons_list.itemClicked.connect(self.set_figure_type)
        if ui is Ui_Dialog:
            self.after_init()

    def after_init(self):
        self.ui.button_accept_text.clicked.connect(self.accept_text)
        self.ui.button_add_task.clicked.connect(self.add_task)
        self.ui.button_delete_last_figure.clicked.connect(self.delete_last_figure)

    def _set_window_state(self):
        """Управляет: figures_buttons_list, button_add_key_words,
         button_add_possible_words, button_add_figure
         Симуляция метода суперкласса, однажды можно отрефакторить"""
        if self.task_text is not None:
            self.ui.figures_buttons_list.setEnabled(True)
        else:
            self.ui.figures_buttons_list.setEnabled(False)

        if self.task_text and self.edited_figure_type:
            self.ui.button_add_key_words.setEnabled(True)
            self.ui.button_add_possible_words.setEnabled(True)
        else:
            self.ui.button_add_key_words.setEnabled(False)
            self.ui.button_add_possible_words.setEnabled(False)

        if self.edited_figure_type and self.edited_figure_key_symbols and self.edited_figure_possible_symbols:
            self.ui.button_add_figure.setEnabled(True)
        else:
            self.ui.button_add_figure.setEnabled(False)

    def set_window_state(self):
        """Проверки заполнения полей объекта задания и активация соответствующих кнопок.
        Для каждой кнопки должны быть описаны сценарии ее активации с обязательным else.
        Проверка при любом нажатии чтобы не было фигни"""
        self._set_window_state()
        if self.task_text is not None:
            self.ui.button_accept_text.setEnabled(False)
        else:
            self.ui.button_accept_text.setEnabled(True)

        if len(self.task_figures_list) > 0:
            self.ui.button_delete_last_figure.setEnabled(True)
        else:
            self.ui.button_delete_last_figure.setEnabled(False)

        if self.task_text and self.task_figures_list:
            self.ui.button_add_task.setEnabled(True)
        else:
            self.ui.button_add_task.setEnabled(False)

    def set_default_figure_fields(self):
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_text = ''
        self.edited_figure_possible_symbols_text = ''

        self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_text)
        self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_text)
        self.ui.figure_info_type.setText('Выберите тип оборота')
        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))

    def accept_text(self):
        self.task_text = self.ui.task_text.toHtml()
        self.ui.task_text.setReadOnly(1)
        # UI activation
        self.ui.task_name_input.setEnabled(True)
        self.ui.figures_counter_label.setEnabled(True)
        self.set_window_state()

    def add_key_words(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        if end - start != 0:
            self.edited_figure_key_symbols += range(start, end)  # todo переделать на end + 1 и исправить все что за этим следует
            self.edited_figure_key_symbols_text += cursor.selectedText() + " || "
            # print(sorted(self.edited_figure_key_symbols))
            self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_text)
            char_format = cursor.charFormat()
            char_format.setBackground(self.possible_figures[self.edited_figure_type])
            cursor.setCharFormat(char_format)
        self.set_window_state()

    def add_possible_words(self):  # todo переделать способ задания границ оборотов \\ и вот непонятно, сделано ли уже
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        if end - start != 0:
            self.edited_figure_possible_symbols = [start, end - 1]  # see if causes problems
            self.edited_figure_possible_symbols_text = cursor.selectedText()
            self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_text)
        self.set_window_state()

    def set_figure_type(self, item):
        self.edited_figure_type = item.text()
        self.ui.figure_info_type.setText(self.edited_figure_type)
        self.set_window_state()

    def add_figure_to_list(self):
        figure = TaskFigure(_type=self.edited_figure_type,
                            key_symbols=self.edited_figure_key_symbols,
                            key_symbols_text=self.edited_figure_key_symbols_text,
                            possible_symbols=self.edited_figure_possible_symbols,
                            possible_symbols_text=self.edited_figure_possible_symbols_text)
        self.task_figures_list.append(figure)
        self.set_default_figure_fields()

        self.set_window_state()

    def whiten_text_from_figure(self, deleted_figure):
        start = min(deleted_figure.key_symbols)
        end = max(deleted_figure.key_symbols) + 1
        cursor = self.ui.task_text.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        char_format = cursor.charFormat()
        char_format.setBackground(QtCore.Qt.white)
        cursor.setCharFormat(char_format)
        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))

    def delete_last_figure(self):
        try:
            deleted_figure = self.task_figures_list.pop()
            self.whiten_text_from_figure(deleted_figure)
            self.set_window_state()
        except Exception as exc:
            self.ui.figures_counter_label.setText('Ошибка удаления')
            self.set_window_state()

    def add_task(self):
        self.highlighted_task_text = self.ui.task_text.toHtml()
        self.task_name = self.ui.task_name_input.toPlainText()
        if not self.task_name:
            self.ui.figure_info_type.setText('Название')
        else:
            try:
                task = Task(name=self.task_name,
                            text=self.task_text,
                            highlighted_text=self.highlighted_task_text,
                            figures_list=self.task_figures_list)
                # print(task)
                packed_task = pickle.dumps(task)
                query_add_task = '''INSERT INTO taskbase (`task_name`, `task_object`) VALUES (%s,%s)'''
                insert = (self.task_name, packed_task)
                sql_stuff.insert_as_teacher(query_add_task, insert)
                self.ui.figure_info_type.setText('Задание отправлено')
                self.ui.button_add_task.setEnabled(False)
            except Exception as exc:
                self.ui.figure_info_type.setText('Ошибка отправки задания ')
        self.set_window_state()


class CheckAnswersForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_check_answers_window()
        self.ui.setupUi(self)
        self.task_text_windows = []

        query_get_task_names = '''SELECT DISTINCT task_name FROM answerbase ORDER BY task_name'''
        tasks_tup = sql_stuff.get_answer_as_teacher(query_get_task_names)
        for i in range(len(tasks_tup)):
            self.ui.list_of_tasks.addItem(tasks_tup[i][0])

        self.task_folder = ''
        self.student_folder = ''
        self.current_answer = None
        self.current_answer_highlighted_text = None

        self.ui.list_of_tasks.itemClicked.connect(self.open_tasks_folder)
        self.ui.list_of_students.itemClicked.connect(self.open_students_folder)
        self.ui.list_of_answers.itemClicked.connect(self.check_answer)
        self.ui.button_show_task_text.clicked.connect(self.show_task_text)
        self.ui.button_show_answer_text.clicked.connect(self.show_answer_text)

    def open_tasks_folder(self, item):  # здесь важна адресация по именам и id
        self.task_folder = item.text()
        self.ui.list_of_students.clear()

        query_get_student_names = '''SELECT DISTINCT student_id, student_name FROM answerbase 
        WHERE task_name=\'{}\' ORDER BY student_name'''.format(self.task_folder)
        students_tup = sql_stuff.get_answer_as_teacher(query_get_student_names)
        # print(students_tup)
        student_strings = []
        for i in range(len(students_tup)):
            student_strings.append(students_tup[i][1] + ' || ' + str(students_tup[i][0]))
        for i in student_strings:
            self.ui.list_of_students.addItem(i)

    def open_students_folder(self, item):
        self.student_folder = int(item.text().split()[-1])
        self.ui.list_of_answers.clear()

        query_get_answer_times = '''SELECT completion_date FROM answerbase
        WHERE task_name=\'{}\' AND student_id={} ORDER BY completion_date'''.format(self.task_folder,
                                                                                    self.student_folder)
        times_tup = sql_stuff.get_answer_as_teacher(query_get_answer_times)

        for i in range(len(times_tup)):
            self.ui.list_of_answers.addItem(times_tup[i][0])

    def check_answer(self, item):  # todo перенести запрос задания на уровень выше для избежания повторений
        self.current_answer = item.text()
        query_get_answer = '''SELECT answer_object FROM answerbase WHERE task_name=\'{}\' AND student_id={} 
        AND completion_date=\'{}\''''.format(self.task_folder, self.student_folder, self.current_answer)
        answer_tup = sql_stuff.get_answer_as_teacher(query_get_answer)
        packed_answer = answer_tup[0][0]
        answer = pickle.loads(packed_answer)
        self.current_answer_highlighted_text = answer.highlighted_text

        query_get_task = '''SELECT task_object FROM taskbase WHERE task_name=\'{}\''''.format(self.task_folder)
        task_tup = sql_stuff.get_answer_as_teacher(query_get_task)
        packed_task = task_tup[0][0]
        task = pickle.loads(packed_task)

        correct, not_found, not_right = answer.answer_checker(task)

        self.ui.label_found_correct.setText('Найдено правильно {}'.format(len(correct)))
        self.ui.label_found_wrong.setText('Найдено неправильно {}'.format(len(not_right)))
        self.ui.label_not_found.setText('Не найдено {}'.format(len(not_found)))
        self.ui.label_total_figs_task.setText('Всего оборотов в задании {}'.format(len(task.figuresList)))
        self.ui.label_total_figs_answer.setText('Всего оборотов в ответе {}'.format(len(answer.answer_figures_list)))

        found_correct_text, found_wrong_text, not_found_text = '', '', ''
        for i in correct:
            found_correct_text += i.figure_type + ' || ' + \
                                  i.key_symbols_text + '\n'
        for i in not_right:
            found_wrong_text += i.figure_type + ' || ' + \
                                i.figure_text + '\n'
        for i in not_found:
            not_found_text += i.figure_type + ' || ' + \
                              i.key_symbols_text + '\n'
        self.ui.text_found_correct.setText(found_correct_text)
        self.ui.text_found_wrong.setText(found_wrong_text)
        self.ui.text_not_found.setText(not_found_text)

    def show_task_text(self):
        if not self.current_answer:
            return
        query_get_task = '''SELECT task_object FROM taskbase WHERE task_name=\'{}\''''.format(self.task_folder)
        task_tup = sql_stuff.get_answer_as_teacher(query_get_task)
        packed_task = task_tup[0][0]
        task = pickle.loads(packed_task)
        task_text = task.highlighted_text

        self.task_text_windows.append(TextWindow(text=task_text))
        self.task_text_windows[-1].open()

    def show_answer_text(self):
        if not self.current_answer:
            return
        self.task_text_windows.append(TextWindow(text=self.current_answer_highlighted_text))
        self.task_text_windows[-1].open()


class TextWindow(QtWidgets.QDialog):
    def __init__(self, text):
        super().__init__()
        self.ui = Ui_text_window()
        self.ui.setupUi(self)
        self.ui.text.setText(text)
        self.ui.text.cursorPositionChanged.connect(self.show_type)

    def show_type(self):
        """Способ реализовать отображение типа оборота без раскрашивания в цвета"""
        cursor = self.ui.text.textCursor()
        start = cursor.selectionStart()
        print(start)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = AddTaskForm()
    application.show()

    sys.exit(app.exec())
