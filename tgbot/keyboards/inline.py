from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# формируем клавиатуру с упражнениями
from tgbot.loader import but_exercises
markup_ex = InlineKeyboardMarkup(row_width=3)
for i in range(0,len(but_exercises), 3):
    markup_ex.insert(InlineKeyboardButton(text=but_exercises[i][1], callback_data=str(i)))
    if len(but_exercises)-i>=3:
        markup_ex.insert(InlineKeyboardButton(text=but_exercises[i+1][1], callback_data=str(i+1)))
        markup_ex.insert(InlineKeyboardButton(text=but_exercises[i+2][1], callback_data=str(i+2)))
    elif len(but_exercises)-i==2:
        markup_ex.insert(InlineKeyboardButton(text=but_exercises[i+1][1], callback_data=str(i+1)))
        markup_ex.insert(InlineKeyboardButton(text=' ', callback_data='-1'))
    elif len(but_exercises)-i==1:
        markup_ex.insert(InlineKeyboardButton(text=' ', callback_data='-1'))
        markup_ex.insert(InlineKeyboardButton(text=' ', callback_data='-1'))
markup_ex.insert(InlineKeyboardButton(text='В главное меню', callback_data='-2'))

# формируем клавиатуру подтверждения ввода
markup_yes_no = InlineKeyboardMarkup(row_width=2)
markup_yes_no.insert(InlineKeyboardButton(text="Записать", callback_data="Y"))
markup_yes_no.insert(InlineKeyboardButton(text="Отменить", callback_data="N"))
