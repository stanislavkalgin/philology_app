from PyQt5 import QtWidgets
from entrance_form_teacher import Ui_entrance_form  # IDE зря ругается
import sys
from teacher import AddTaskForm, CheckAnswersForm
import sql_stuff


class entrance_window(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_entrance_form()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)  # temp todo remove in ui file
        self.ui.entrance_button.clicked.connect(self.check_login_password)
        self.ui.button_add_task.clicked.connect(self.add_task)
        self.ui.button_check_task.clicked.connect(self.check_tasks)
        self.ui.button_new_teacher.clicked.connect(self.go_to_teacher_registration)
        self.ui.button_registration.clicked.connect(self.go_to_student_registration)
        self.ui.reg_teacher_button_register.clicked.connect(self.register_teacher)
        self.ui.reg_student_button_register.clicked.connect(self.register_student)

    def check_login_password(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        query_login_teacher = 'SELECT * FROM users WHERE rights=\'teacher\''
        teachers = sql_stuff.get_answer_as_teacher(query_login_teacher)
        for i in range(len(teachers)):
            if teachers[i][1] == login and teachers[i][2] == password:
                self.ui.stackedWidget.setCurrentIndex(1)
                break
            else:
                self.ui.label.setText('Неудача')  # todo более цивильный текст

    def add_task(self):
        add_task_window = AddTaskForm()
        add_task_window.exec()

    def check_tasks(self):
        check_task_window = CheckAnswersForm()
        check_task_window.exec()

    def go_to_teacher_registration(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_student_registration(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def register_teacher(self):
        personal_name = self.ui.reg_teacher_personal_name_input.text()
        login = self.ui.reg_teacher_login_input.text()
        password_1 = self.ui.reg_teacher_password_1.text()
        password_2 = self.ui.reg_teacher_password_2.text()
        if sql_stuff.check_login_is_available(login):
            if password_1 == password_2:
                query_new_teacher = '''INSERT INTO users(`user_id`, `login`, `password`, `personal_name`, `rights`) 
                VALUES (%s,%s,%s,%s,%s)'''
                new_id = sql_stuff.get_new_id()
                inserts = (new_id, login, password_1, personal_name, 'teacher')
                sql_stuff.insert_as_teacher(query_new_teacher, inserts)
                self.ui.stackedWidget.setCurrentIndex(1)
            else:
                self.ui.teacher_register_label.setText('Пароли не совпадают')
        else:
            self.ui.teacher_register_label.setText('Логин занят')

    def register_student(self):
        personal_name = self.ui.reg_student_personal_name_input.text()
        login = self.ui.reg_student_login_input.text()
        password = self.ui.reg_student_password.text()
        if sql_stuff.check_login_is_available(login):
            new_id = sql_stuff.get_new_id()
            query_new_student = '''INSERT INTO users(`user_id`, `login`, `password`, `personal_name`, `rights`) 
                        VALUES (%s,%s,%s,%s,%s)'''
            inserts = (new_id, login, password, personal_name, 'student')
            sql_stuff.insert_as_teacher(query_new_student, inserts)
            self.ui.student_register_label.setText((personal_name + '\nуспешно зарегестрирован'))
        else:
            self.ui.student_register_label.setText('Логин занят')


app = QtWidgets.QApplication([])
application = entrance_window()
application.show()

sys.exit(app.exec())