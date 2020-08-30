from PyQt5 import QtWidgets, QtGui, QtCore
from answer_adding_window import Ui_answer_edit_window
import sys
import sql_stuff
import pickle
from global_stuff import possible_figures, Answer, AnswerFigure


# todo управление состоянием, если считается нужным, сохранение логов и файла объекта ответа

class answer_adding_window(QtWidgets.QDialog):
    def __init__(self, user_id=None, user_name=None, task_name=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_answer_edit_window()
        self.ui.setupUi(self)
        self.possible_figures = possible_figures.copy()

        keys = []
        for i in self.possible_figures.keys():
            keys.append(i)
        keys.sort()
        for i in range(len(keys)):
            self.ui.figures_buttons_list.addItem(keys[i])
            self.ui.figures_buttons_list.item(i).setForeground(self.possible_figures[keys[i]])

        self.user_id = user_id
        self.user_name = user_name
        self.task_name = task_name
        self.figures_to_show = ''
        self.figures_list = []

        query_get_task = '''SELECT * FROM taskbase WHERE task_name=\'{}\''''.format(self.task_name)
        selected_task = sql_stuff.get_answer_as_student(query_get_task)
        packed_task = selected_task[0][1]
        task = pickle.loads(packed_task)

        self.ui.task_text.setText(task.text)
        self.set_default_figure_fields()

        self.ui.figures_buttons_list.itemClicked.connect(self.set_figure_type)
        self.ui.button_add_figure.clicked.connect(self.add_figure)
        self.ui.button_finish_task.clicked.connect(self.complete_task)
        self.ui.button_delete_last_figure.clicked.connect(self.delete_last_figure)

    def set_figure_type(self, item):
        self.figure_type = item.text()
        self.ui.label_chosen_figure_type.setText(self.figure_type)

        self.ui.button_add_figure.setEnabled(True)

    def add_figure(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        if end - start != 0:
            self.figure_symbol_range = [start, end - 1]
            self.figure_text = cursor.selectedText()

            figure = AnswerFigure(figure_type=self.figure_type,
                                  symbols_range=self.figure_symbol_range,
                                  figure_text=self.figure_text)
            self.figures_list.append(figure)
            self.refresh_figures_to_show()
            self.ui.figures_browser.setText(self.figures_to_show)

            char_format = cursor.charFormat()
            char_format.setBackground(self.possible_figures[self.figure_type])
            cursor.setCharFormat(char_format)

            self.set_default_figure_fields()
            self.ui.button_add_figure.setEnabled(False)

    def complete_task(self):
        answer_highlighted_text = self.ui.task_text.toHtml()
        answer = Answer(self.user_id, self.task_name, self.figures_list, answer_highlighted_text)
        query_save_answer = '''INSERT INTO answerbase
        (`task_name`, `student_id`, `student_name`, `completion_date`, `answer_object`)
         VALUES (%s,%s,%s,%s,%s)'''
        packed_answer = pickle.dumps(answer)
        insert = (self.task_name, self.user_id, self.user_name, answer.time, packed_answer)
        for i in range(3):
            try:
                sql_stuff.insert_as_student(query_save_answer, insert)
                self.ui.label_chosen_figure_type.setText('Отправлено')
            except Exception as exc:
                if i == 2:
                    self.ui.label_chosen_figure_type.setText('Ошибка')
                    with open(self.task_name + '.txt', 'a') as task_file:
                        task_file.write(str(packed_answer))

    def set_default_figure_fields(self):
        self.figure_type = None
        # self.ui.label_chosen_figure_type.setText(self.user_id + ' ' + self.task_name)  # отладочное
        self.figure_symbol_range = []
        self.figure_text = None
        self.ui.label_chosen_figure_type.setText('Выберите тип\n оборота')

    def delete_last_figure(self):
        try:
            deleted_figure = self.figures_list.pop()
            start = deleted_figure.symbols_range[0]
            end = deleted_figure.symbols_range[-1] + 1
            print(self.figures_list, start, end)
            cursor = self.ui.task_text.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            char_format = cursor.charFormat()
            char_format.setBackground(QtCore.Qt.white)
            cursor.setCharFormat(char_format)
            self.refresh_figures_to_show()
            self.ui.figures_browser.setText(self.figures_to_show)
        except:
            self.ui.label_chosen_figure_type.setText('Ошибка удаления')


    def refresh_figures_to_show(self):
        self.figures_to_show = ''
        for i in range(len(self.figures_list)):
            self.figures_to_show += '%s || %s \n' % (self.figures_list[i].figure_type,
                                                     self.figures_list[i].figure_text)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = answer_adding_window(user_id=1, user_name='Преподаватель 1', task_name='Martin Luther King')
    application.show()

    sys.exit(app.exec())