from PyQt5 import QtWidgets
from answer_adding_window import Ui_answer_edit_window
import sys, shelve

from global_stuff import PATH_TO_TASK_DB, PATH_TO_ANSWERS_DB, possible_figures, Answer, AnswerFigure


class answer_adding_window(QtWidgets.QDialog):
    def __init__(self, id=None, task_name=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_answer_edit_window()
        self.ui.setupUi(self)
        self.user_id = id
        self.task_name = task_name
        self.figures_to_show = ''
        self.figures_list = []

        tasks_db = shelve.open(PATH_TO_TASK_DB)
        self.task_text = tasks_db[task_name].text
        self.ui.task_text.setPlainText(self.task_text)
        tasks_db.close()
        self.set_default_figure_fields()

        self.ui.button_metaphor.clicked.connect(self.set_figure_type)
        self.ui.button_epithet.clicked.connect(self.set_figure_type)
        self.ui.button_repeat.clicked.connect(self.set_figure_type)
        self.ui.button_add_figure.clicked.connect(self.add_figure)
        self.ui.button_finish_task.clicked.connect(self.complete_task)

    def set_figure_type(self):
        sender = self.sender()
        self.figure_type = possible_figures.index(sender.text())
        self.ui.label_chosen_figure_type.setText(possible_figures[self.figure_type])

    def add_figure(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.figure_symbol_range = [start, end-1]
        print(end - start)

        figure = AnswerFigure(self.figure_type, self.figure_symbol_range)
        self.figures_list.append(figure)
        self.figures_to_show += '%s || %s \n' % (possible_figures[self.figure_type], self.task_text[start: end])
        self.ui.figures_browser.setText(self.figures_to_show)
        print(figure)

        self.set_default_figure_fields()

    def complete_task(self):
        answer = Answer(self.user_id, self.task_name, self.figures_list)
        answers_db = shelve.open(PATH_TO_ANSWERS_DB, writeback=True)
        if answers_db[self.task_name].get(self.user_id) is None:
            answers_db[self.task_name][self.user_id] = [answer]
        else:
            answers_db[self.task_name][self.user_id].append(answer)
        answers_db.close()
        print(answer)

    def set_default_figure_fields(self):
        self.figure_type = None
        self.ui.label_chosen_figure_type.setText(self.user_id + ' ' + self.task_name)  # отладочное
        self.figure_symbol_range = []


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = answer_adding_window(id='5272', task_name='Jack')
    application.show()

    sys.exit(app.exec())