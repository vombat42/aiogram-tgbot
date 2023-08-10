from aiogram import Bot
from aiogram.types import Message

async def user_start(message: Message, bot: Bot):
    # await message.reply("Приступим :)")
    # await bot.send_message(chat_id=message.from_user.id, text="Приступим :)")
    await bot.send_message(chat_id=message.chat.id, text="Приступим :)")

async def user_hello(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text="Уверен?")


