from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.utils.callbackdata import ExInfo

# ----------------------------------------------------------

# формируем клавиатуру с упражнениями
def get_markup_ex():
    markup_ex = InlineKeyboardBuilder()
    from tgbot.loader import but_exercises
    for i in but_exercises:
        markup_ex.button(text=i[1], callback_data=ExInfo(action='select',ex_id=i[0], name=i[1], unit=i[2]))
    if len(but_exercises)%3 != 0:
        for i in range(3-len(but_exercises)%3):
            markup_ex.button(text=' ', callback_data=ExInfo(action='nothing_to_do',ex_id=-1, name='', unit=''))
    markup_ex.button(text='В главное меню', callback_data=ExInfo(action='to_main',ex_id=-2, name='', unit=''))
    markup_ex.adjust(3)
    return markup_ex.as_markup()

# формируем клавиатуру подтверждения ввода
# (text_yes: Текст на кнопке ДА, text_no: Текст на кнопке НЕТ, mmenu: Наличие конки В ГЛАВНОЕ МЕНЮ)
def get_markup_yes_no(text_yes: str, text_no: str, mmenu: bool):
    markup_yes_no = InlineKeyboardBuilder()
    markup_yes_no.button(text=text_yes, callback_data="Y")
    markup_yes_no.button(text=text_no, callback_data="N")
    if mmenu:
        markup_yes_no.button(text="В главное меню", callback_data="MM")
    markup_yes_no.adjust(2)
    return markup_yes_no.as_markup()

# формируем клавиатуру диалога "report"
def get_markup_report():
    markup_report = InlineKeyboardBuilder()
    markup_report.button(text="День", callback_data='repD')
    markup_report.button(text="Неделя", callback_data='repW')
    markup_report.button(text="Месяц", callback_data='repM')
    markup_report.button(text="Выбрать период", callback_data='repP')
    markup_report.button(text="В главное меню", callback_data='MM')
    markup_report.adjust(2)
    return markup_report.as_markup()


# ----- END -----

# def get_markup_yes_no():
#     markup_yes_no = InlineKeyboardBuilder()
#     markup_yes_no.button(text="Записать", callback_data="Y")
#     markup_yes_no.button(text="Отменить", callback_data="N")
#     markup_yes_no.button(text="В главное меню", callback_data="MM")
#     markup_yes_no.adjust(2)
#     return markup_yes_no.as_markup()