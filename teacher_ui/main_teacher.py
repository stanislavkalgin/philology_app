from PyQt5 import QtWidgets
from entrance_form_teacher import Ui_entrance_form  # IDE зря ругается
import sys
import shelve
from global_stuff import PATH_TO_USERS_DB, User
from teacher import AddTaskForm, CheckAnswersForm


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
        user_db = shelve.open(PATH_TO_USERS_DB, 'r')
        for i in user_db.keys():
            if user_db[i].login == login:
                user = user_db[i]
                user_db.close()
                break
        else:
            self.ui.label.setText('Неправильный логин')
            user_db.close()
            return
        if user.password == password:
            if user.rights == 'admin':
                self.ui.stackedWidget.setCurrentIndex(1)
            else:
                self.ui.label.setText('Недостаточно прав')
        else:
            self.ui.label.setText('Неправильный пароль')
        user_db.close()

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
        login = self.ui.regidtration_login_input.text()
        password_1 = self.ui.regitration_password_1.text()
        password_2 = self.ui.registration_password_2.text()
        if password_1 == password_2:
            new_teacher = User(personal_name, login, password_1, rights='admin')
            users_db = shelve.open(PATH_TO_USERS_DB)
            users_db[new_teacher.id] = new_teacher
            users_db.close()
        else:
            print('Пароли не совпадают')  # todo remake with label


app = QtWidgets.QApplication([])
application = entrance_window()
application.show()

sys.exit(app.exec())