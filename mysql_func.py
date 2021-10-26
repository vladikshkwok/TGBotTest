import mysql.connector

connection = mysql.connector.connect(host='localhost', user='gigs', password='password', database='tetragigs')


def mysql_exec(db_query, db_connection=connection):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(db_query)
            return cursor.fetchall()
    except Exception as e:
        print(e)


def new_user(user_full_name, tg_username, tg_user_id, tg_chat_id):
    db_query = f"INSERT INTO user (full_name,tg_user_name,register_date,tg_user_id, " \
               f"tg_chat_id) values ('{user_full_name}', '{tg_username}', NOW(), '{tg_user_id}', {tg_chat_id});"
    print(db_query)
    res = mysql_exec(db_query=db_query)
    print(res)


def find_user(tg_user_id):
    db_query = f"select id from user where tg_user_id={tg_user_id};"
    res = mysql_exec(db_query=db_query)
    if res.__len__() == 1:
        return True
    if res.__len__() > 1:
        print("Записей пользователя больше чем одна, что то не так")
    return False
