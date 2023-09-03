from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
	commands = [
		BotCommand(command="/start", description= "Перезапуск бота"),
		BotCommand(command="/exercise", description= "🏋 упражнения"),
		BotCommand(command="/report", description= "📜 отчет"),
		# BotCommand(command="/graph", description= "📊 график"),
		BotCommand(command="/hello", description= "✋ приветствие"),
		# BotCommand(command="/help", description= "Помощь"),
		BotCommand(command="/manage_exercise", description= "✏️🏋 управление упражнениями"),
	]
	await bot.set_my_commands(commands, BotCommandScopeDefault())
	print(')-----> set_commands DONE!')