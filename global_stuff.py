import shelve
from random import randint
from datetime import datetime
from PyQt5 import QtCore

PATH_TO_TASK_DB = '../project_data/database/tasks'
PATH_TO_ANSWERS_DB = '../project_data/database/answers'
PATH_TO_USERS_DB = '../project_data/users_database/users'
possible_figures = ('Метафора', 'Эпитет', 'Повтор')
colors_of_figures = (QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green)


class TaskFigure:
    global possible_figures

    def __init__(self, type, key_symbols, key_symbols_text, possible_symbols, possible_symbols_text):
        self.type = type  # todo refactor as figure_type
        self.key_symbols = key_symbols
        self.key_symbols_text = key_symbols_text  # для отображения при проверке и других обращениях
        self.possible_symbols = possible_symbols
        self.possible_symbols_text = possible_symbols_text  # для отображения при проверке и других обращениях

    def __str__(self):  # отладочное
        return ('[TaskFigure: type - %s, key symbols - %s, possible symbols from %s to %s]'
                % (possible_figures[self.type], self.key_symbols,
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


class User:
    def __init__(self, personal_name, login, password, rights='user'):
        id_db = shelve.open(PATH_TO_USERS_DB, 'r')
        existing_ids = id_db.keys()
        while 1:
            new_id = str(randint(0, 10000))
            if new_id not in existing_ids:
                break
        id_db.close()
        self.id = new_id
        self.personal_name = personal_name
        self.login = login
        self.password = password
        self.rights = rights


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
        if task_figure.type == self.figure_type:  # Тип
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
    def __init__(self, student_id, task_name, answer_figures_list):
        self.student_id = student_id
        self.task_name = task_name
        self.answer_figures_list = answer_figures_list
        self.time = str(datetime.today())[:16]

    def __str__(self):
        n = ("id>" + self.student_id + " " + self.task_name + "\n")
        counter = 1
        for i in range(len(self.answer_figures_list)):
            n += (str(counter) + " ")
            n += (str(self.answer_figures_list[i]) + "\n")
            counter += 1
        return n

    def answer_checker(self, task):  # O(n*m), возможно упростить, если нужно, принимает объект задания
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
