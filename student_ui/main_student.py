from global_stuff import PATH_TO_USERS_DB, User, PATH_TO_TASK_DB
from PyQt5 import QtWidgets
from entrance_form_student import Ui_entrance_form
import sys
import shelve
import student  # temp


class entrance_window(QtWidgets.QDialog):
    def __init__(self):
        super(entrance_window, self).__init__()
        self.ui = Ui_entrance_form()
        self.ui.setupUi(self)
        self.ui.entrance_button_enter.clicked.connect(self.check_login_password)
        self.user_id = None
        self.ui.task_list.itemClicked.connect(self.open_add_answer_window)
        self.ui.entrance_button_register.clicked.connect(self.switch_to_register)
        self.ui.register_button_register.clicked.connect(self.register_new_user)

    def check_login_password(self):
        login = self.ui.entrance_login.text()
        password = self.ui.entrance_password.text()
        user_db = shelve.open(PATH_TO_USERS_DB, 'r')
        for i in user_db.keys():
            if user_db[i].login == login:
                user = user_db[i]
                user_db.close()
                break
        else:
            self.ui.entrance_label.setText('Неправильный логин')
            user_db.close()
            return
        if user.password == password:
            self.user_id = user.id  # Может быть не нужно
            self.ui.stackedWidget.setCurrentIndex(2)
            task_db = shelve.open(PATH_TO_TASK_DB, 'r')
            for i in task_db.keys():
                self.ui.task_list.addItem(i)
            task_db.close()
        else:
            self.ui.entrance_label.setText('Неправильный пароль')
        user_db.close()

    def open_add_answer_window(self, item):
        add_answer_window = student.answer_adding_window(id=self.user_id, task_name=item.text())
        add_answer_window.exec()

    def switch_to_register(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def register_new_user(self):
        personal_name = self.ui.register_personal_name.text()
        login = self.ui.register_login.text()
        password1 = self.ui.register_password_1.text()
        password2 = self.ui.register_password_2.text()
        if password1 == password2:
            new_user = User(personal_name, login, password1)
            users_db = shelve.open(PATH_TO_USERS_DB)
            users_db[new_user.id] = new_user
            users_db.close()
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.register_label.setText('Пароли не совпадают')


app = QtWidgets.QApplication([])
application = entrance_window()
application.show()

sys.exit(app.exec())