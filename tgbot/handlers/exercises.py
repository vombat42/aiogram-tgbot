from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import date
from tgbot.keyboards.inline import get_markup_ex, get_markup_yes_no, get_markup_manage_ex_list, get_markup_manage_ex
from tgbot.utils.states import StatesExercises
from tgbot.utils.callbackdata import ExInfo
from tgbot.utils.pg_func import db_events_add

# ---------------------------------------------------------------------
# async def exercises_wrong_message(message: Message):
#     print(')-----> wrong message? deleting...')
#     await message.delete()


# ----------------------------
# ----- Events Exercises -----
# ----------------------------

async def exercises_start(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id,
                        text="Выберите упражнение и потом введите количество",
                        reply_markup=get_markup_ex())
    await state.update_data(ex_start_msg_id=msg.message_id)
    await state.set_state(StatesExercises.EX_SELECT)


async def exercises_select(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data=ExInfo):
    data = await state.get_data()
    if callback_data.action == 'to_main': # выход в главное меню
        if data.get('ex_start_msg_id'):
            await bot.delete_message(call.message.chat.id, data.get('ex_start_msg_id'))
        if data.get('ex_select_msg_id'):
            await bot.delete_message(call.message.chat.id, data.get('ex_select_msg_id'))
        # await bot.send_message(chat_id=call.message.chat.id, text="главное меню")
        await state.clear()
        await call.answer(f'Выход в главное меню')
        return
    if callback_data.action == 'nothing_to_do': # выходим, если нажата пустая кнопка
        await call.answer(f'Нажата пустая кнопка')
        return
    if data.get('ex_select_msg_id'):
        await bot.delete_message(call.message.chat.id, data.get('ex_select_msg_id'))
    msg_text = f'Введите количество {callback_data.name}'
    msg = await bot.send_message(chat_id=call.message.chat.id, text=msg_text)
    await state.set_state(StatesExercises.EX_COUNT)
    await state.update_data(ex_id=callback_data.ex_id,
                            ex_name=callback_data.name,
                            ex_unit=callback_data.unit,
                            ex_select_msg_id=msg.message_id)
    await call.answer(f'Вы выбрали {callback_data.name}')


async def exercises_count(message: Message, bot: Bot, state: FSMContext):
    if message.text.isdigit(): #проверяем, что введено число
        count = int(message.text)
        if count > 0:
            data = await state.get_data()
            await bot.delete_message(message.chat.id, data.get('ex_select_msg_id'))
            msg_text = f"Записать <b><u> {data.get('ex_name')} - {count} {data.get('ex_unit')}</u></b> ?"
            msg = await bot.send_message(chat_id=message.chat.id,
                                        text=msg_text,
                                        reply_markup=get_markup_yes_no('Записать', 'Отменить', True))
            await state.set_state(StatesExercises.EX_CONFIRM)
            await state.update_data(ex_count=count,
                                    ex_select_msg_id=msg.message_id)
    await message.delete()


# async def exercises_confirm(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data=ExInfo):
async def exercises_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if not (call.data in ['MM','Y','N']): # выходим, если нажата пустая кнопка
        await call.answer(f'Нажата неверная кнопка')
        return    
    if call.data == 'MM': # выход в главное меню
        await bot.delete_message(call.message.chat.id, data.get('ex_start_msg_id'))
        await bot.delete_message(call.message.chat.id, data.get('ex_select_msg_id'))
        # await bot.send_message(chat_id=call.message.chat.id, text="выход в главное меню")
        await state.clear()
        await call.answer(f'выход в главное меню')
        return
    if call.data == 'N':
        await bot.delete_message(call.message.chat.id, data.get('ex_select_msg_id'))
        msg_text = f"Введите количество {data.get('ex_name')}"
        msg = await bot.send_message(chat_id=call.message.chat.id, text=msg_text)
        await state.update_data(ex_select_msg_id=msg.message_id)
        await state.set_state(StatesExercises.EX_COUNT)
        await call.answer(f'Cancel')
        return
    else:
        await bot.delete_message(call.message.chat.id, data.get('ex_select_msg_id'))
        msg_text = f"Записано <b><u> {data.get('ex_name')} - {data.get('ex_count')} {data.get('ex_unit')}</u></b> !"
        await bot.send_message(chat_id=call.message.chat.id, text=msg_text)
        # await exercises_record(data('ex_id'),data('ex_count'))
        temp = data.get('ex_start_msg_id')
        # db_events_add(chat_id, ex_id, ex_count, ex_date)
        db_events_add(call.message.chat.id, data.get('ex_id'), data.get('ex_count'), str(date.today()))
        await state.clear()
        await state.set_state(StatesExercises.EX_SELECT)
        await state.update_data(ex_start_msg_id=temp)
        await call.answer(f'Записано в базу')


# ----------------------------
# ----- Manage Exercises -----
# ----------------------------

async def exercises_manage_select(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id,
                    text=f"Выберите упражнение для редактирования или нажми <b>'Добавить'</b>",
                    reply_markup=get_markup_manage_ex_list())
    await state.update_data(ex_manage_msg_id=msg.message_id)
    await state.set_state(StatesExercises.EX_MANAGE_SELECT)


async def exercises_manage(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data=ExInfo):
    data = await state.get_data()
    if callback_data.action == 'manage_to_main': # выход в главное меню
        if data.get('ex_manage_msg_id'):
            await bot.delete_message(call.message.chat.id, data.get('ex_manage_msg_id'))
        await state.clear()
        await call.answer(f'Выход в главное меню')
        return
    if callback_data.action == 'edit_ex': # редактировать запись "упражнение"
        msg = await bot.send_message(chat_id=call.message.chat.id,
                 text=f"Выберите действие над <b><u> {callback_data.name} ({callback_data.unit})</u></b> ",
                 reply_markup=get_markup_manage_ex())
        await state.update_data(ex_edit_msg_id=msg.message_id,
                                ex_name=callback_data.name,
                                ex_unit=callback_data.unit)
        await state.set_state(StatesExercises.EX_EDIT)
        await call.answer(f'редактировать запись "упражнение"')
        return
    if callback_data.action == 'new_ex': # создать запись "упражнение"
        msg = await bot.send_message(chat_id=call.message.chat.id, text=f"Введите наименование нового упражнения")
        await state.set_state(StatesExercises.EX_NEW_NAME)
        await call.answer(f'Введите наименование нового упражнения')
        return


async def exercises_edit(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('ex_edit_msg_id'):
        await bot.delete_message(call.message.chat.id, data.get('ex_edit_msg_id'))
    if call.data == 'exManageSelect':
        await state.set_state(StatesExercises.EX_MANAGE_SELECT)
        await call.answer(f'Назад')
        return
    if call.data == 'exDel':
        msg = await bot.send_message(chat_id=call.message.chat.id,
            text=f"Удалить <b><u> {data.get('ex_name')} ({data.get('ex_unit')})</u></b> ?\n"
                f"ВНИМАНИЕ! При этом удаляться все записанные ранее выполненные такие упражнения!",
            reply_markup=get_markup_yes_no('Удалить', 'Отменить', False))
        await state.update_data(ex_del_msg_id=msg.message_id)
        await state.set_state(StatesExercises.EX_DEL)
        await call.answer(f'Подтвердите удаление')
        return
    if call.data == 'exName':
        msg = await bot.send_message(chat_id=call.message.chat.id,
            text=f"Введите новое наименование упражнения <b>'{data.get('ex_name')}'</b>")
        await state.update_data(ex_edit_msg_id=msg.message_id)
        await state.set_state(StatesExercises.EX_EDIT_NAME)
        await call.answer(f"Введите новое наименование упражнения")
        return


async def exercises_edit_name(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('ex_edit_msg_id'):
        await bot.delete_message(message.chat.id, data.get('ex_edit_msg_id'))    
    msg = await bot.send_message(chat_id=message.chat.id,
                    text=f"Изменить <b>'{data.get('ex_name')}'</b> на <b>'{message.text}'</b>?",
                    reply_markup=get_markup_yes_no('Изменить', 'Отменить', False))
    tmp=data.get('ex_name')
    await state.update_data(ex_edit_msg_id=msg.message_id,
                            ex_name=message.text,
                            ex_old_name=tmp)
    await message.delete()
    await state.set_state(StatesExercises.EX_EDIT_NAME_CONFIRM)
    return


async def exercises_edit_name_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('ex_edit_msg_id'):
        await bot.delete_message(call.message.chat.id, data.get('ex_edit_msg_id'))
    if call.data == 'N':
        await state.set_state(StatesExercises.EX_MANAGE_SELECT)
        await call.answer(f'Отмена')
        return
    msg = await bot.send_message(chat_id=call.message.chat.id,
        text=f"<b><u> {data.get('ex_old_name')} переименовано  в {data.get('ex_name')}</u></b>!")
    await state.set_state(StatesExercises.EX_MANAGE_SELECT)
    await call.answer(f'Переименовано!')
    return


async def exercises_del(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('ex_del_msg_id'):
        await bot.delete_message(call.message.chat.id, data.get('ex_del_msg_id'))
    if call.data == 'N':
        await state.set_state(StatesExercises.EX_MANAGE_SELECT)
        await call.answer(f'Отмена')
        return
    msg = await bot.send_message(chat_id=call.message.chat.id,
        text=f"Удалены записи с <b><u> {data.get('ex_name')} ({data.get('ex_unit')})</u></b>!")
    await state.set_state(StatesExercises.EX_MANAGE_SELECT)
    await call.answer(f'Записи удалены!')
    return


async def exercises_new_name(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id,
                    text=f"Введите единицу измерения")
    # await state.update_data(ex_manage_msg_id=msg.message_id)
    await state.update_data(ex_name=message.text)
    await state.set_state(StatesExercises.EX_NEW_UNIT)
    return


async def exercises_new_unit(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    msg = await bot.send_message(chat_id=message.chat.id,
                    text=f"Создать упражнение <b>{data.get('ex_name')} ({message.text})</b>?",
                    reply_markup=get_markup_yes_no('Создать', 'Отменить', False))
    # await state.update_data(ex_manage_msg_id=msg.message_id)
    await state.update_data(ex_unit=message.text)
    await state.set_state(StatesExercises.EX_NEW_CONFIRM)
    return


async def exercises_new_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    # if data.get('ex_del_msg_id'):
    #     await bot.delete_message(call.message.chat.id, data.get('ex_del_msg_id'))
    if call.data == 'N':
        await state.set_state(StatesExercises.EX_MANAGE_SELECT)
        await call.answer(f'Отмена')
        return
    msg = await bot.send_message(chat_id=call.message.chat.id,
        text=f"Создано <b><u> {data.get('ex_name')} ({data.get('ex_unit')})</u></b>!")
    await state.set_state(StatesExercises.EX_MANAGE_SELECT)
    await call.answer(f'Создано новое упражнение')
    return