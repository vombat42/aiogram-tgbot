import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from tgbot.config import load_config

config = load_config(".env")
bot = Bot(config.tg_bot.token, parse_mode="HTML")
dp = Dispatcher(bot)

t_exercises = 'exercises' # таблица БД "список упражнений"
t_events = 'events' # таблица БД "события (выполненные упражнения)"

conn = psycopg2.connect(f'postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.name}')
conn.autocommit = True
cur = conn.cursor()
cur.execute(
   f"SELECT id, ex_name, ex_unit FROM {t_exercises};"
)
but_exercises=cur.fetchall()

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )