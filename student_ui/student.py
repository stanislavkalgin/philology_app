from PyQt5 import QtWidgets
from answer_adding_window import Ui_answer_edit_window
import sys
import sql_stuff
import pickle
from global_stuff import possible_figures, Answer, AnswerFigure, colors_of_figures


class answer_adding_window(QtWidgets.QDialog):
    def __init__(self, user_id=None, user_name=None, task_name=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_answer_edit_window()
        self.ui.setupUi(self)
        for i in range(len(possible_figures)):
            self.ui.figures_buttons_list.addItem(possible_figures[i])
            self.ui.figures_buttons_list.item(i).setForeground(colors_of_figures[i])

        self.user_id = user_id
        self.user_name = user_name
        self.task_name = task_name
        self.figures_to_show = ''
        self.figures_list = []

        query_get_task = '''SELECT * FROM taskbase WHERE task_name=\'{}\''''.format(self.task_name)
        con, cur = sql_stuff.setup_connection_as_student()
        cur.execute(query_get_task)
        selected_task = cur.fetchall()
        cur.close()
        con.close()
        packed_task = selected_task[0][1]
        task = pickle.loads(packed_task)

        self.ui.task_text.setText(task.text)
        self.set_default_figure_fields()

        self.ui.figures_buttons_list.itemClicked.connect(self.set_figure_type)
        self.ui.button_add_figure.clicked.connect(self.add_figure)
        self.ui.button_finish_task.clicked.connect(self.complete_task)

    def set_figure_type(self, item):
        self.figure_type = possible_figures.index(item.text())
        self.ui.label_chosen_figure_type.setText(possible_figures[self.figure_type])

    def add_figure(self):
        cursor = self.ui.task_text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        self.figure_symbol_range = [start, end-1]
        self.figure_text = cursor.selectedText()
        print(end - start)

        figure = AnswerFigure(figure_type=self.figure_type,
                              symbols_range=self.figure_symbol_range,
                              figure_text=self.figure_text)
        self.figures_list.append(figure)
        self.figures_to_show += '%s || %s \n' % (possible_figures[self.figure_type], self.figure_text)
        self.ui.figures_browser.setText(self.figures_to_show)
        print(figure)

        char_format = cursor.charFormat()
        char_format.setBackground(colors_of_figures[self.figure_type])
        cursor.setCharFormat(char_format)

        self.set_default_figure_fields()

    def complete_task(self):
        answer = Answer(self.user_id, self.task_name, self.figures_list)
        query_save_answer = '''INSERT INTO answerbase
        (`task_name`, `student_id`, `student_name`, `completion_date`, `answer_object`)
         VALUES (%s,%s,%s,%s,%s)'''
        packed_answer = pickle.dumps(answer)
        insert = (self.task_name, self.user_id, self.user_name, answer.time, packed_answer)
        con, cur = sql_stuff.setup_connection_as_student()
        cur.execute(query_save_answer, insert)
        con.commit()
        cur.close()
        con.close()

        print(answer)

    def set_default_figure_fields(self):
        self.figure_type = None
        # self.ui.label_chosen_figure_type.setText(self.user_id + ' ' + self.task_name)  # отладочное
        self.figure_symbol_range = []
        self.figure_text = None
        self.ui.label_chosen_figure_type.setText('Оборот')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = answer_adding_window(user_id=2, task_name='Тест 0')
    application.show()

    sys.exit(app.exec())