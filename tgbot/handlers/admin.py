from bot import bot, dp
from aiogram.types import Message
from tgbot.config import load_config
# from aiogram import Dispatcher

config = load_config(".env")

async def send_to_admin(*args):
    for i in config.tg_bot.admin_ids:
        await bot.send_message(chat_id=i, text="Бот запущен")


@dp.message_handler()
async def echo(message: Message):
    text = f"Привет, ты написал: {message.text}"
    await message.reply(text=text)




# async def admin_start(message: Message):
#     await message.reply("Hello, admin!")


# def register_admin(dp: Dispatcher):
#     dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)






