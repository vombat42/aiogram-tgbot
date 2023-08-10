from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from tgbot.keyboards import get_markup_ex, get_markup_yes_no
from tgbot.utils.states_exercises import StatesExercises
from tgbot.utils.callbackdata import ExInfo

# ---------------------------------------------------------------------

async def exercises_start(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.chat.id,
                        text="Выбери упражнение и потом введи количество",
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
            msg = await bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=get_markup_yes_no())
            await state.set_state(StatesExercises.EX_CONFIRM)
            await state.update_data(ex_count=count,
                                    ex_select_msg_id=msg.message_id)
    await message.delete()


async def exercises_confirm(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data=ExInfo):
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
        await state.clear()
        await state.set_state(StatesExercises.EX_SELECT)
        await state.update_data(ex_start_msg_id=temp)
        await call.answer(f'Записано в базу')

async def exercises_wrong_message(message: Message):
    print(')-----> wrong message? deleting...')
    await message.delete()