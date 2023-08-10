from bot import bot, dp
from aiogram.types import Message
from tgbot.config import load_config
# from tgbot.keyboards import markup_ex, markup_yes_no
# from aiogram import Dispatcher

config = load_config(".env")

# async def send_to_admin_start(*args):
#     for i in config.tg_bot.admin_ids:
#         await bot.send_message(chat_id=i, text="Бот запущен")

# async def send_to_admin_stop(*args):
#     for i in config.tg_bot.admin_ids:
#         await bot.send_message(chat_id=i, text="Stop!")

async def send_to_admin(mess_text):
    print(')-----> Admin message')
    for i in config.tg_bot.admin_ids:
        await bot.send_message(chat_id=i, text=mess_text)

# @dp.message_handler(commands='report')
async def echo(message: Message):
    text = f"REPORT"
    # await message.reply(text=text, reply_markup=markup_yes_no)
    await message.reply(text=text)

# @dp.message_handler()
async def echo(message: Message):
    text = f"Привет, ты написал: {message.text}"
    # await message.reply(text=text, reply_markup=markup_ex)
    await message.reply(text=text)


# async def admin_start(message: Message):
#     await message.reply("Hello, admin!")


# def register_admin(dp: Dispatcher):
#     dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)






