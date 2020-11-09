import sql_stuff


query_get_tasks = """
SELECT task_name, creator_name, creator from taskbasemarktwo"""
tasks = sql_stuff.get_answer_as_teacher(query_get_tasks)
for task_name, student_name, stud_id in tasks:
    stud_split = student_name.split()
    if len(stud_split) == 3 and stud_id > 10 and stud_split[0] not in task_name:
        new_task_name = stud_split[0] + " " + stud_split[1][:1] + "." + stud_split[2][:1] + ". - " + task_name
        query_task = "UPDATE taskbasemarktwo set task_name = %s where task_name = %s"
        sql_stuff.insert_as_teacher(query_task, (new_task_name, task_name))
        query_answer = "UPDATE answerbasemarktwo set task_name = %s where task_name = %s"
        sql_stuff.insert_as_teacher(query_answer, (new_task_name, task_name))
        a = 5
a = 5