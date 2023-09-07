import asyncio
import psycopg2
from datetime import date
from tgbot.loader import config, cur, t_events, t_exercises

# ----------------------------------------------------------------------

def get_userid_from_chatid(chat_id: int):
	cur.execute(f"SELECT id FROM users WHERE chat_id='{chat_id}';")
	return cur.fetchone()[0]


def db_events_add(chat_id, ex_id, ex_count, ex_date):
	user_id = get_userid_from_chatid(chat_id)
	cur.execute(
	   f"INSERT INTO {t_events} (date_enent, user_id, ex_id, ex_count) VALUES ('{ex_date}',{user_id},{ex_id},{ex_count});"
	)


def db_report(date_start: date, date_end: date, chat_id: int):
    # SELECT ex_id, SUM(ex_count), exercises.ex_name, exercises.ex_unit FROM events JOIN exercises ON exercises.id=events.ex_id WHERE date_enent > '2023-08-02' AND date_enent < '2023-09-02' GROUP BY ex_id, exercises.ex_name, exercises.ex_unit ORDER BY ex_id;
    user_id = get_userid_from_chatid(chat_id)
    cur.execute(
        f"SELECT ex_id, exercises.ex_name, SUM(ex_count), exercises.ex_unit "
        f"FROM events JOIN exercises ON exercises.id=events.ex_id "
        f"WHERE date_enent >= '{date_start}' AND date_enent <= '{date_end}' "
        f"AND user_id = {user_id} "
        f"GROUP BY ex_id, exercises.ex_name, exercises.ex_unit "
        f"ORDER BY ex_id;"
    )
    return cur.fetchall()


def db_ex_list():
    cur.execute(
        f"SELECT id, ex_name, ex_unit FROM {t_exercises};"
    )
    return cur.fetchall()


# возвращает количество записей в таблице "events" с указанным упражнением 
async def db_ex_count_events(ex_id):
    cur.execute(
        f"SELECT COUNT(*) FROM {t_events} WHERE ex_id = '{ex_id}';"
    )
    return cur.fetchone()[0]


def db_exercises_add(ex_name, ex_unit):
    cur.execute(
       f"INSERT INTO {t_exercises} (ex_name, ex_unit) VALUES ('{ex_name}', '{ex_unit}');"
    )


async def db_exercises_delete(ex_id):
    cur.execute(
       f"DELETE FROM {t_exercises} WHERE id='{ex_id}';"
    )


def db_exercises_update(ex_name, ex_id):
    cur.execute(
       f"UPDATE {t_exercises} SET ex_name = '{ex_name}' WHERE id='{ex_id}';"
    )

