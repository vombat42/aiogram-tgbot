import psycopg2
from datetime import date
from tgbot.loader import config, cur, t_events


def db_events_add(chat_id, ex_id, ex_count, ex_date):
	# conn = psycopg2.connect(f'postgresql://{pg_user}:{pg_userpass}@{pg_host}:{pg_port}/{pg_dbname}')
	# conn.autocommit = True
	# cur = conn.cursor()
	cur.execute(f"SELECT id FROM users WHERE chat_id='{chat_id}';")
	user_id=cur.fetchone()[0]
	cur.execute(
	   f"INSERT INTO {t_events} (date_enent, user_id, ex_id, ex_count) VALUES ('{ex_date}',{user_id},{ex_id},{ex_count});"
	)
	# cur.close()
	# conn.close()