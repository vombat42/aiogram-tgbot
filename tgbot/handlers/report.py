from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta

from tgbot.keyboards import get_markup_report, get_markup_yes_no
from tgbot.utils.states import StatesReport, States
from tgbot.utils.pg_func import db_report
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
        await state.set_state(StatesReport.REP_PERIOD)
        msg = await bot.send_message(chat_id=call.message.chat.id,
                                    text=f"Введите отчетный период\nв формате <b>01.02.2023-15.03.2023</b>")
        await state.update_data(rep_confirm_msg_id=[msg.message_id,])
        await call.answer(f'введите отчетный период')
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


async def report_period(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    msg_list = []
    msg_list.extend(data.get('rep_confirm_msg_id'))
    period_start, period_end = convert_enter_period(message.text)
    if period_start == '0':
        for item in msg_list:
            try:
                await bot.delete_message(message.chat.id, item)
            except:
                pass
        await message.delete()
        msg = await bot.send_message(chat_id=message.chat.id,
                                    text=f"<u>Не корректный ввод! Повторите.</u>\nВведите отчетный период\nв формате <b>01.02.2023-15.03.2023</b>")
        msg_list.append(msg.message_id)
    else:
        msg_list.append(message.message_id)
        await state.update_data(rep_period_start=period_start, rep_period_end=period_end)
        msg = await bot.send_message(chat_id=message.chat.id,
                                    text=f"Получить отчет за период <b>{message.text}</b> ?",
                                    reply_markup=get_markup_yes_no('Получить', 'Отменить', False))
        msg_list.append(msg.message_id)
        await state.set_state(StatesReport.REP_CONFIRM)
    await state.update_data(rep_confirm_msg_id=msg_list)


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
        report = db_report(data.get('rep_period_start'), data.get('rep_period_end'), call.message.chat.id)
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

def convert_date(date: date):
    temp = date.split("-")
    return f"{temp[2]}.{temp[1]}.{temp[0]}"


def convert_enter_period(period: str):
    isValidDate = True
    temp_period = period.split('-')

    try:
        day, month, year = temp_period[0].split('.')
        start_date = datetime.date(int(year), int(month), int(day)).strftime("%Y-%m-%d")
        print('start_date =', start_date)
    except ValueError:
        return '0', '0'

    try:
        day, month, year = temp_period[1].split('.')
        end_date = datetime.date(int(year), int(month), int(day)).strftime("%Y-%m-%d")
        print('end_date =', end_date)
    except ValueError:
        return '0', '0'

    if end_date < start_date:
        return '0', '0'

    return start_date, end_date
