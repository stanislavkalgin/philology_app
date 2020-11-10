from datetime import datetime
from PyQt5 import QtCore

# possible_figures = ('Метафора', 'Эпитет', 'Повтор')
# colors_of_figures = (QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green)
possible_figures = {'Метафора': QtCore.Qt.red, 'Эпитет': QtCore.Qt.blue, 'Повтор': QtCore.Qt.green,
                    'Сравнение': QtCore.Qt.red, 'Эвфемизм': QtCore.Qt.blue, 'Парадокс': QtCore.Qt.green,
                    'Игра слов': QtCore.Qt.red, 'Антитеза': QtCore.Qt.blue, 'Аллюзия': QtCore.Qt.green,
                    'Метонимия': QtCore.Qt.red, 'Параллелизм': QtCore.Qt.blue, 'Ономатопея': QtCore.Qt.green,
                    'Эллипс': QtCore.Qt.red, 'Многосоюзие': QtCore.Qt.blue, 'Графон': QtCore.Qt.green,
                    'Риторический вопрос': QtCore.Qt.red, 'Гипербола': QtCore.Qt.blue, 'Инверсия': QtCore.Qt.green,
                    'Синекдоха': QtCore.Qt.red, 'Ирония': QtCore.Qt.blue, 'Зевгма': QtCore.Qt.green,
                    'Оксюморон': QtCore.Qt.red, 'Антономасия': QtCore.Qt.blue, 'Литота': QtCore.Qt.green,
                    'Перефраз': QtCore.Qt.red}

STUDENT_RIGHTS = 'student'
TEACHER_RIGHTS = 'teacher'


class TaskFigure:
    global possible_figures

    def __init__(self, _type, key_symbols, key_symbols_text, possible_symbols, possible_symbols_text):
        self.figure_type = _type
        self.key_symbols = key_symbols
        self.key_symbols_text = key_symbols_text
        self.possible_symbols = possible_symbols
        self.possible_symbols_text = possible_symbols_text

    def __str__(self):
        return ('[TaskFigure: type - %s, key symbols - %s, possible symbols from %s to %s]'
                % (self.figure_type, self.key_symbols,
                   self.possible_symbols[0], self.possible_symbols[-1]))


class Task:
    def __init__(self, name, text, highlighted_text, figures_list):
        self.name = name
        self.text = text
        self.highlighted_text = highlighted_text
        self.figuresList = figures_list

    def __str__(self):  # Отладочное
        n = (self.name + "\n")
        n += self.text + "\n"
        counter = 1
        for i in self.figuresList:
            n += (str(counter) + " ")
            n += (str(i) + "\n")
            counter += 1
        return n


class AnswerFigure:
    def __init__(self, figure_type, symbols_range, figure_text):
        self.figure_type = figure_type
        self.symbols_range = symbols_range
        self.figure_text = figure_text  # для отображения при проверке и других обращениях

    def __str__(self):  # Отладочное
        return ('[TaskFigure: type - %s, symbols range from %s to %s]'
                % (possible_figures[self.figure_type],
                   self.symbols_range[0], self.symbols_range[-1]))

    def check_figure(self, task_figure):
        if task_figure.figure_type == self.figure_type:  # Тип
            if (min(task_figure.key_symbols) >= self.symbols_range[0] and  # todo отслеживать возможность проблем
                    max(task_figure.key_symbols) <= self.symbols_range[-1]):
                if (task_figure.possible_symbols[0] <= self.symbols_range[0] and
                        task_figure.possible_symbols[-1] >= self.symbols_range[-1]):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


class Answer:
    def __init__(self, student_id, task_name, answer_figures_list, highlighted_text):
        self.student_id = student_id
        self.task_name = task_name
        self.answer_figures_list = answer_figures_list
        self.time = str(datetime.today())[:16]
        self.highlighted_text = highlighted_text

    def __str__(self):
        n = ("id>" + str(self.student_id) + " " + self.task_name + "\n")
        counter = 1
        for i in range(len(self.answer_figures_list)):
            n += (str(counter) + " ")
            n += (str(self.answer_figures_list[i]) + "\n")
            counter += 1
        return n

    def answer_checker(self, task):
        task_figures = task.figuresList[:]
        answer_figures = self.answer_figures_list[:]
        correct, not_found = [], []
        for i in range(len(task_figures)):
            current_task_figure = task_figures.pop(0)
            for j in range(len(answer_figures)):
                if answer_figures[j].check_figure(current_task_figure) is True:
                    correct.append(current_task_figure)
                    answer_figures.remove(answer_figures[j])
                    break
            else:
                not_found.append(current_task_figure)
        not_right = answer_figures[:]
        return correct, not_found, not_right
