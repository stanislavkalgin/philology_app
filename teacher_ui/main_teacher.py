from PyQt5 import QtWidgets
from entrance_form_teacher import Ui_entrance_form
import pickle
import sys
import traceback
from datetime import datetime
from teacher import AddTaskForm, CheckAnswersForm
from modify_task import ModifyTaskForm
from global_stuff import STUDENT_RIGHTS, TEACHER_RIGHTS
import sql_stuff

# TODO хеширование отправляемых паролей
# TODO Проверка уникальности имени задания


class EntranceWindow(QtWidgets.QDialog):
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
        self.ui.button_edit_task.clicked.connect(self.go_to_task_modification)
        self.ui.list_of_edited_tasks.itemClicked.connect(self.modify_task)
        self.ui.button_back_choice_of_edited.clicked.connect(self.go_to_menu)
        self.ui.button_back_teacher_reg.clicked.connect(self.go_to_menu)
        self.ui.button_back_student_reg.clicked.connect(self.go_to_entrance)

        self.creator_name = None
        self.creator_id = None
        self.user_rights = None

    def check_login_password(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        query_login_teacher = 'SELECT * FROM users'
        teachers = sql_stuff.get_answer_as_teacher(query_login_teacher)
        for i in range(len(teachers)):
            if teachers[i][1] == login and teachers[i][2] == password:
                self.creator_name = teachers[i][3]
                self.creator_id = teachers[i][0]
                self.user_rights = teachers[i][4]
                self.ui.stackedWidget.setCurrentIndex(1)
                break
            else:
                self.ui.label.setText('Неудача')  # todo более цивильный текст

    def add_task(self):
        add_task_window = AddTaskForm(creator_id=self.creator_id, creator_name=self.creator_name)
        add_task_window.exec()

    def check_tasks(self):
        if self.user_rights == TEACHER_RIGHTS:
            check_task_window = CheckAnswersForm()
            check_task_window.exec()


    def go_to_teacher_registration(self):
        if self.user_rights == TEACHER_RIGHTS:
            self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_student_registration(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def register_teacher(self):
        personal_name = self.ui.reg_teacher_personal_name_input.text()
        login = self.ui.reg_teacher_login_input.text()
        password_1 = self.ui.reg_teacher_password_1.text()
        password_2 = self.ui.reg_teacher_password_2.text()
        if personal_name and login and password_1 and password_2:
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
        else:
            self.ui.teacher_register_label.setText('Заполните все поля')

    def register_student(self):
        personal_name = self.ui.reg_student_personal_name_input.text()
        login = self.ui.reg_student_login_input.text()
        password = self.ui.reg_student_password.text()
        if personal_name != "" and login != "" and password != "":
            if sql_stuff.check_login_is_available(login):
                new_id = sql_stuff.get_new_id()
                query_new_student = '''INSERT INTO users(`user_id`, `login`, `password`, `personal_name`, `rights`) 
                            VALUES (%s,%s,%s,%s,%s)'''
                inserts = (new_id, login, password, personal_name, 'student')
                sql_stuff.insert_as_teacher(query_new_student, inserts)
                self.ui.student_register_label.setText((personal_name + '\nуспешно зарегистрирован'))
            else:
                self.ui.student_register_label.setText('Логин занят')
        else:
            self.ui.student_register_label.setText('Заполните все поля')

    def go_to_task_modification(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        if self.user_rights == TEACHER_RIGHTS:
            query_get_task_names = '''SELECT task_name FROM taskbasemarktwo WHERE mark_del = false'''
        else:
            query_get_task_names = '''SELECT task_name FROM taskbasemarktwo 
            WHERE creator = {} AND mark_del = false'''.format(self.creator_id)
        task_names_tuple = sql_stuff.get_answer_as_teacher(query_get_task_names)
        self.ui.list_of_edited_tasks.clear()
        for i in task_names_tuple:
            self.ui.list_of_edited_tasks.addItem(i[0])

    def modify_task(self, item):
        task_name = item.text()
        query_get_task_objects = '''SELECT task_object FROM taskbasemarktwo 
        WHERE task_name=\'{}\' AND mark_del = false'''.format(task_name)
        task_tuple = sql_stuff.get_answer_as_teacher(query_get_task_objects)
        packed_task = task_tuple[0][0]
        task = pickle.loads(packed_task)
        edit_window = ModifyTaskForm(task, creator_id=self.creator_id, creator_name=self.creator_name)
        edit_window.exec()

    def go_to_menu(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_entrance(self):
        self.ui.stackedWidget.setCurrentIndex(0)

def excepthook(exc_type, exc_value, exc_tb):
    tb = str(datetime.now()) + "".join(traceback.format_exception(exc_type, exc_value, exc_tb)) + "\n"
    with open('log.txt', 'a') as log_file:
        log_file.write(tb)
    QtWidgets.QApplication.quit()


sys.excepthook = excepthook
app = QtWidgets.QApplication([])
application = EntranceWindow()
application.show()

sys.exit(app.exec())
