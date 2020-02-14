
## MUST BE GITIGNORED for safety reasons!!!!!!!

import pymysql
from sql_links import *

def setup_connection_as_teacher():
    con = pymysql.connect(db_host, db_teacher_username,
                          db_teacher_password, db_database_name)
    cur = con.cursor()
    return con, cur


def setup_connection_as_student():
    con = pymysql.connect(db_host, db_student_username,
                          db_student_password, db_database_name)
    cur = con.cursor()
    return con, cur


def get_answer_as_student(query):
    con, cur = setup_connection_as_student()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_answer_as_teacher(query):
    con, cur = setup_connection_as_teacher()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_new_id():
    con, cur = setup_connection_as_teacher()
    cur.execute('SELECT MAX(user_id) FROM users')
    current_top_id = cur.fetchall()
    cur.close()
    con.close()
    new_id = current_top_id[0][0] + 1
    return new_id
