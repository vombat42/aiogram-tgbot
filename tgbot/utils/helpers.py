# import asyncio
from aiogram import Bot

# --------------------------------

async def delete_msg_list(bot: Bot, chat_id: int, msg_list: list):
	for i in msg_list:
		await bot.delete_message(chat_id, i)
	return