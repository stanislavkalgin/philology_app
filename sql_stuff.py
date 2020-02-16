
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


def insert_as_student(query, insert):
    con, cur = setup_connection_as_student()
    cur.execute(query, insert)
    con.commit()
    cur.close()
    con.close()


def insert_as_teacher(query, insert):
    con, cur = setup_connection_as_teacher()
    cur.execute(query, insert)
    con.commit()
    cur.close()
    con.close()


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


def check_login_is_available(login):
    query_check_login = '''SELECT login FROM users'''
    logins_tuple = get_answer_as_teacher(query_check_login)
    logins = []
    for i in logins_tuple:
        logins.append(i[0])
    if login in logins:
        return False
    else:
        return True
