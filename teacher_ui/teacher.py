import shelve
from global_stuff import possible_figures, PATH_TO_TASK_DB, \
    PATH_TO_ANSWERS_DB, Task, TaskFigure, PATH_TO_USERS_DB, User, Answer, AnswerFigure
from task_add_form import Ui_Dialog
from checking_answers_form import Ui_check_answers_window
from PyQt5 import QtWidgets
import sys

# TODO добавить везде предупреждения о потенциальном исключении


class AddTaskForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # блок полей создаваемого задания
        self.possible_figures = possible_figures
        self.task_text = None
        self.task_name = None
        self.task_figures_list = []
        # блок полей создаваемого оборота, все должно быть обнулено после каждого добавления оборота
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_to_show = ''
        self.edited_figure_possible_symbols_to_show = ''
        self.edited_figure_type_to_show = None
        # функционал окна
        self.ui.button_accept_text.clicked.connect(self.accept_text)
        self.ui.button_add_key_words.clicked.connect(self.add_key_words)
        self.ui.button_add_possible_words.clicked.connect(self.add_possible_words)
        self.ui.button_metaphor.clicked.connect(self.set_figure_type)
        self.ui.button_epithet.clicked.connect(self.set_figure_type)
        self.ui.button_repeats.clicked.connect(self.set_figure_type)
        self.ui.button_add_figure.clicked.connect(self.add_figure_to_list)
        self.ui.button_add_task.clicked.connect(self.add_task)

    def accept_text(self):
        self.task_text = self.ui.task_text.toPlainText()
        self.ui.task_text.setReadOnly(1)
        # anything else?

    def add_key_words(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.edited_figure_key_symbols += range(start, end)
        self.edited_figure_key_symbols_to_show += self.task_text[start: end] + " || "
        # print(sorted(self.edited_figure_key_symbols))
        self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_to_show)

    def add_possible_words(self):  # todo переделать способ задания границ оборотов
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.edited_figure_possible_symbols += range(start, end)
        self.edited_figure_possible_symbols_to_show += self.task_text[start: end] + " || "
        # print(sorted(self.edited_figure_possible_symbols))
        self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_to_show)

    def set_figure_type(self):
        sender = self.sender()
        self.edited_figure_type = self.possible_figures.index(sender.text())
        self.edited_figure_type_to_show = self.possible_figures[self.edited_figure_type]
        self.ui.figure_info_type.setText(self.edited_figure_type_to_show)

    def add_figure_to_list(self):
        figure = TaskFigure(self.edited_figure_type,
                            self.edited_figure_key_symbols,
                            self.edited_figure_possible_symbols)
        self.task_figures_list.append(figure)
        # Обнуление полей редактируемого оборота
        self.edited_figure_key_symbols = []
        self.edited_figure_possible_symbols = []
        self.edited_figure_type = None
        self.edited_figure_key_symbols_to_show = ''
        self.edited_figure_possible_symbols_to_show = ''
        self.edited_figure_type_to_show = None
        self.ui.figure_info_key_words.setText(self.edited_figure_key_symbols_to_show)
        self.ui.figure_info_possible_words.setText(self.edited_figure_possible_symbols_to_show)
        self.ui.figure_info_type.setText('Тип оборота')

        self.ui.figures_counter_label.setText('Оборотов добавлено\n{}'.format(len(self.task_figures_list)))
        for i in self.task_figures_list:
            print(i)

    def add_task(self):
        self.task_name = self.ui.task_name_input.toPlainText()
        task = Task(self.task_name,
                    self.task_text,
                    self.task_figures_list)
        print(task)
        tasks_db = shelve.open(PATH_TO_TASK_DB)
        tasks_db[task.name] = task
        tasks_db.close()
        answers_db = shelve.open(PATH_TO_ANSWERS_DB)
        answers_db[task.name] = {}
        answers_db.close()


class CheckAnswersForm(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_check_answers_window()
        self.ui.setupUi(self)
        answers_db = shelve.open(PATH_TO_ANSWERS_DB, 'r')
        for i in answers_db.keys():
            self.ui.list_of_tasks.addItem(i)
        answers_db.close()
        self.task_folder = ''
        self.student_folder = ''
        self.current_answer = None

        self.ui.list_of_tasks.itemClicked.connect(self.open_tasks_folder)
        self.ui.list_of_students.itemClicked.connect(self.open_students_folder)
        self.ui.list_of_answers.itemClicked.connect(self.check_answer)

    def open_tasks_folder(self, item):  # здесь важна адресация по именам и id
        self.task_folder = item.text()
        self.ui.list_of_students.clear()
        answers_db = shelve.open(PATH_TO_ANSWERS_DB, 'r')
        users_db = shelve.open(PATH_TO_USERS_DB, 'r')
        for i in answers_db[self.task_folder].keys():
            name = users_db[i].personal_name
            self.ui.list_of_students.addItem(name + ' ' + i)
        answers_db.close()
        users_db.close()

    def open_students_folder(self, item):
        self.student_folder = item.text().split()[-1]
        self.ui.list_of_answers.clear()
        answers_db = shelve.open(PATH_TO_ANSWERS_DB, 'r')
        for i in range(len(answers_db[self.task_folder][self.student_folder])):
            time_tag = answers_db[self.task_folder][self.student_folder][i].time
            self.ui.list_of_answers.addItem(str(i+1) + '. ' + time_tag)
        answers_db.close()

    def check_answer(self, item):
        self.current_answer = int(item.text().split('.')[0]) - 1
        answers_db = shelve.open(PATH_TO_ANSWERS_DB, 'r')
        answer = answers_db[self.task_folder][self.student_folder][self.current_answer]
        answers_db.close()
        tasks_db = shelve.open(PATH_TO_TASK_DB)
        task = tasks_db[self.task_folder]
        tasks_db.close()
        correct, not_found, not_right = answer.answer_checker(task)

        self.ui.label_found_correct.setText('Найдено правильно {}'.format(len(correct)))
        self.ui.label_found_wrong.setText('Найдено неправильно {}'.format(len(not_right)))
        self.ui.label_not_found.setText('Не найдено {}'.format(len(not_found)))
        self.ui.label_total_figs_task.setText('Всего оборотов в задании {}'.format(len(task.figuresList)))
        self.ui.label_total_figs_answer.setText('Всего оборотов в ответе {}'.format(len(answer.answer_figures_list)))

        found_correct_text, found_wrong_text, not_found_text = '', '', ''
        for i in correct:
            found_correct_text += possible_figures[i.type] + ' || ' + \
                                  task.text[i.key_symbols[0]: i.key_symbols[-1]+1] + '\n'
        for i in not_right:
            found_wrong_text += possible_figures[i.figure_type] + ' || ' + \
                                  task.text[i.symbols_range[0]: i.symbols_range[-1]+1] + '\n'
        for i in not_found:
            not_found_text += possible_figures[i.type] + ' || ' + \
                                  task.text[i.key_symbols[0]: i.key_symbols[-1]+1] + '\n'
        self.ui.text_found_correct.setText(found_correct_text)
        self.ui.text_found_wrong.setText(found_wrong_text)
        self.ui.text_not_found.setText(not_found_text)


if __name__=='__main__':
    app = QtWidgets.QApplication([])
    application = CheckAnswersForm()
    application.show()

    sys.exit(app.exec())