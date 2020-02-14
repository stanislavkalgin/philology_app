from PyQt5 import QtWidgets
from entrance_form_student import Ui_entrance_form
import sys
import student  # temp
import sql_stuff
# todo наполнение списка заданиями


class entrance_window(QtWidgets.QDialog):
    def __init__(self):
        super(entrance_window, self).__init__()
        self.ui = Ui_entrance_form()
        self.ui.setupUi(self)
        self.ui.entrance_button_enter.clicked.connect(self.check_login_password)
        self.user_id = None
        self.user_name = None
        self.ui.task_list.itemClicked.connect(self.open_add_answer_window)
        self.ui.entrance_button_register.clicked.connect(self.switch_to_register)
        self.ui.register_button_register.clicked.connect(self.register_new_user)

    def check_login_password(self):
        login = self.ui.entrance_login.text()
        password = self.ui.entrance_password.text()

        query_login_student = 'SELECT * FROM users'
        con, cur = sql_stuff.setup_connection_as_student()
        cur.execute(query_login_student)
        students = cur.fetchall()
        cur.close()
        con.close()

        for i in range(len(students)):
            if students[i][1] == login and students[i][2] == password:
                self.user_id = students[i][0]
                self.user_name = students[i][3]
                self.ui.stackedWidget.setCurrentIndex(2)

                # print(self.user_id)
                break
            else:
                self.ui.entrance_label.setText('Неудача')  # todo более цивильный текст

        query_get_task_names = '''SELECT `task_name` FROM taskbase'''
        con, cur = sql_stuff.setup_connection_as_student()
        cur.execute(query_get_task_names)
        tasks = cur.fetchall()
        cur.close()
        con.close()

        for i in range(len(tasks)):
            self.ui.task_list.addItem(tasks[i][0])

    def open_add_answer_window(self, item):
        add_answer_window = student.answer_adding_window(user_id=self.user_id,
                                                         user_name=self.user_name,
                                                         task_name=item.text())
        add_answer_window.exec()

    def switch_to_register(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def register_new_user(self):
        personal_name = self.ui.register_personal_name.text()
        login = self.ui.register_login.text()
        password_1 = self.ui.register_password_1.text()
        password_2 = self.ui.register_password_2.text()
        if password_1 == password_2:
            query_new_student = '''INSERT INTO users(`user_id`, `login`, `password`, `personal_name`, `rights`) 
                        VALUES (%s,%s,%s,%s,%s)'''
            new_id = sql_stuff.get_new_id()
            inserts = (new_id, login, password_1, personal_name, 'student')
            con, cur = sql_stuff.setup_connection_as_student()
            cur.execute(query_new_student, inserts)
            con.commit()
            cur.close()
            con.close()
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.register_label.setText('Пароли не совпадают')


app = QtWidgets.QApplication([])
application = entrance_window()
application.show()

sys.exit(app.exec())