from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import date
from dateutil.relativedelta import relativedelta
import psycopg2

from tgbot.keyboards import get_markup_report, get_markup_yes_no
from tgbot.utils.states import StatesReport, States
# from tgbot.utils.pg_func import db_events_add

# ---------------------------------------------------------------------

async def report_start(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id,
                        text="Выбери отчетный период",
                        reply_markup=get_markup_report())
    await state.update_data(rep_start_msg_id=msg.message_id)
    await state.set_state(StatesReport.REP_SELECT)


async def report_select(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'MM': # выход в главное меню
        data = await state.get_data()
        if data.get('rep_start_msg_id'):
            await bot.delete_message(call.message.chat.id, data.get('rep_start_msg_id'))
        await state.clear()
        await state.set_state(States.MAIN_MENU)
        await call.answer(f'Выход в главное меню')
        return
    if call.data == 'repP': # выбран "выбор периода"
        await state.set_state(StatesReport.REP_START_PERIOD)
        msg = await bot.send_message(chat_id=call.message.chat.id, text="введи начало периода")
        await state.update_data(rep_confirm_msg_id=[msg.message_id,])
        await call.answer(f'введи начало периода')
        return
    if call.data == 'repD': # выбран период День/
        await state.update_data(rep_period_start=str(date.today()),
                                rep_period_end=str(date.today()))
        await call.answer(f'выбран период День')
    if call.data == 'repW': # выбран период Неделя
        await state.update_data(rep_period_start=str(date.today()-relativedelta(days=6)),
                                rep_period_end=str(date.today()))
        await state.set_state(StatesReport.REP_CONFIRM)
        await call.answer(f'выбран период Неделя')
    if call.data == 'repM': # выбран период Месяц
        await state.update_data(rep_period_start=str(date.today()-relativedelta(month=1, days=-1)),
                                rep_period_end=str(date.today()))
        await state.set_state(StatesReport.REP_CONFIRM)
        await call.answer(f'выбран период Месяц')
    data = await state.get_data()
    msg = await bot.send_message(chat_id=call.message.chat.id,
                                text=f"Получить отчет с {convert_date(data.get('rep_period_start'))} по {convert_date(data.get('rep_period_end'))} ?",
                                reply_markup=get_markup_yes_no('Получить', 'Отменить', False))
    await state.update_data(rep_confirm_msg_id=[msg.message_id,])
    await state.set_state(StatesReport.REP_CONFIRM)
    return


async def report_period_start(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    msg_list = []
    msg_list.extend(data.get('rep_confirm_msg_id'))
    msg_list.append(message.message_id)
    await state.update_data(rep_period_start=message.text)
    msg = await bot.send_message(chat_id=message.chat.id, text="введи окончание периода")
    msg_list.append(msg.message_id)
    await state.update_data(rep_confirm_msg_id=msg_list)
    await state.set_state(StatesReport.REP_END_PERIOD)


async def report_period_end(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    msg_list = data.get('rep_confirm_msg_id')
    msg_list.append(message.message_id)
    await state.update_data(rep_period_end=message.text)
    data = await state.get_data()
    msg = await bot.send_message(chat_id=message.chat.id,
                                text=f"Получить отчет с {convert_date(data.get('rep_period_start'))} по {convert_date(data.get('rep_period_end'))} ?",
                                reply_markup=get_markup_yes_no('Получить', 'Отменить', False))
    msg_list.append(msg.message_id)
    await state.update_data(rep_confirm_msg_id=msg_list)
    await state.set_state(StatesReport.REP_CONFIRM)


async def report_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.set_state(StatesReport.REP_SELECT)
    for item in data.get('rep_confirm_msg_id'):
        try:
            await bot.delete_message(call.message.chat.id, item)
        except:
            pass
    if call.data == 'N':
        await call.answer(f'Выбери отчетный период')
        return
    if call.data == 'Y':
        report = db_report(data.get('rep_period_start'), data.get('rep_period_end'))
        start = convert_date(data.get('rep_period_start'))
        end = convert_date(data.get('rep_period_end'))
        msg_text = f"<u>📜 Вот твой отчет с {start} по {end}</u>\n\n"
        for i in report:
            msg_text += f"{i[1]} - {i[2]} {i[3]}\n"
        msg = await bot.send_message(chat_id=call.message.chat.id, text=msg_text)
        await call.answer(f'Отчет готов!')
        return
    else:
        await call.answer(f'Некорректное нажатие!')

def db_report(date_start: date, date_end: date):
    from tgbot.loader import cur, conn
    # SELECT ex_id, SUM(ex_count), exercises.ex_name, exercises.ex_unit FROM events JOIN exercises ON exercises.id=events.ex_id WHERE date_enent > '2023-08-02' AND date_enent < '2023-09-02' GROUP BY ex_id, exercises.ex_name, exercises.ex_unit ORDER BY ex_id;
    cur.execute(
        f"SELECT ex_id, exercises.ex_name, SUM(ex_count), exercises.ex_unit "
        f"FROM events JOIN exercises ON exercises.id=events.ex_id "
        f"WHERE date_enent >= '{date_start}' AND date_enent <= '{date_end}' "
        f"GROUP BY ex_id, exercises.ex_name, exercises.ex_unit "
        f"ORDER BY ex_id;"
    )
    return cur.fetchall()


def convert_date(date: date):
    temp = date.split("-")
    return f"{temp[2]}.{temp[1]}.{temp[0]}"
