import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

from tgbot.handlers.user import user_start, user_hello
from tgbot.handlers.exercises import *
from tgbot.handlers.report import *
from tgbot.utils.states import States, StatesExercises, StatesReport
from tgbot.utils.callbackdata import ExInfo

# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

# -----------------------------------------------------------------------------

from tgbot.loader import bot, dp, config, cur, conn
print(config)

logger = logging.getLogger(__name__)

async def start_bot(bot: Bot):
    from tgbot.keyboards import set_commands
    from tgbot.handlers import send_to_admin
    await send_to_admin("Бот запущен")
    await set_commands(bot)

async def stop_bot(bot: Bot):
    from tgbot.handlers import send_to_admin
    await send_to_admin("--- Stop! ---")
    cur.close()
    conn.close()

async def start():
    print(')-----> Start')
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # ----- start, hello -----
    dp.message.register(user_start, Command(commands=["start"]))
    dp.message.register(user_hello, Command(commands=["hello"]))
    # dp.message.register(user_hello, Command(commands=["hello"]), States.MAIN_MENU)
    
    # ----- manage exercises -----
    dp.message.register(exercises_manage_select, Command(commands=["manage_exercise"]))
    dp.callback_query.register(exercises_manage, ExInfo.filter(F.action.in_({'edit_ex', 'new_ex', 'manage_to_main'})))
    dp.callback_query.register(exercises_edit, StatesExercises.EX_EDIT)
    dp.message.register(exercises_edit_name, StatesExercises.EX_EDIT_NAME)
    dp.callback_query.register(exercises_edit_name_confirm, StatesExercises.EX_EDIT_NAME_CONFIRM)
    dp.callback_query.register(exercises_del, StatesExercises.EX_DEL)
    dp.message.register(exercises_new_name, StatesExercises.EX_NEW_NAME)
    dp.message.register(exercises_new_unit, StatesExercises.EX_NEW_UNIT)
    dp.callback_query.register(exercises_new_confirm, StatesExercises.EX_NEW_CONFIRM)
    
    # ----- events exercises -----
    dp.message.register(exercises_start, Command(commands=["exercise"]))
    dp.message.register(exercises_count, StatesExercises.EX_COUNT)
    dp.callback_query.register(exercises_confirm, StatesExercises.EX_CONFIRM)
    dp.callback_query.register(exercises_select, ExInfo.filter(F.action.in_({'select', 'to_main', 'nothing_to_do'})))

    # ----- report -----
    dp.message.register(report_start, Command(commands=["report"]))
    dp.callback_query.register(report_select, StatesReport.REP_SELECT)
    dp.message.register(report_period, StatesReport.REP_PERIOD)
    dp.callback_query.register(report_confirm, StatesReport.REP_CONFIRM)
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())

# ===== E N D ===================================================================
