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
        self.ui.button_new_teacher.clicked.connect(self.go_to_registration)
        self.ui.registration_button_register.clicked.connect(self.register_teacher)

    def check_login_password(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        query_login_teacher = 'SELECT * FROM users WHERE rights=\'teacher\''
        con, cur = sql_stuff.setup_connection_as_teacher()
        cur.execute(query_login_teacher)
        teachers = cur.fetchall()
        cur.close()
        con.close()
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

    def go_to_registration(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def register_teacher(self):
        personal_name = self.ui.registration_personal_name_input.text()
        login = self.ui.regidtration_login_input.text()  # todo fix those names in ui file
        password_1 = self.ui.regitration_password_1.text()
        password_2 = self.ui.registration_password_2.text()
        if password_1 == password_2:
            query_new_teacher = '''INSERT INTO users(`user_id`, `login`, `password`, `personal_name`, `rights`) 
            VALUES (%s,%s,%s,%s,%s)'''
            new_id = sql_stuff.get_new_id()
            inserts = (new_id, login, password_1, personal_name, 'teacher')
            con, cur = sql_stuff.setup_connection_as_teacher()
            cur.execute(query_new_teacher, inserts)
            con.commit()
            cur.close()
            con.close()
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            print('Пароли не совпадают')  # todo remake with label


app = QtWidgets.QApplication([])
application = entrance_window()
application.show()

sys.exit(app.exec())