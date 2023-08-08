# import asyncio
import logging

from aiogram import Bot, Dispatcher, executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

# from tgbot.config import load_config
# from tgbot.filters.admin import AdminFilter
# from tgbot.handlers.admin import register_admin
# from tgbot.handlers.echo import register_echo
# from tgbot.handlers.user import register_user
# from tgbot.middlewares.environment import EnvironmentMiddleware

from tgbot.loader import bot, dp, config
# print(config)

logger = logging.getLogger(__name__)

async def start_bot(bot: Bot):
    from tgbot.loader import bot
    from tgbot.keyboards import set_commands
    from tgbot.handlers import send_to_admin
    await send_to_admin("Бот запущен")
    await set_commands(bot)

async def stop_bot(bot: Bot):
    # from tgbot.handlers import send_to_admin_stop
    # await send_to_admin_stop()
    from tgbot.handlers import send_to_admin
    await send_to_admin("--- Stop! ---")


if __name__ == '__main__':
    # from tgbot.handlers import send_to_admin_start
    executor.start_polling(dp, on_startup=start_bot, on_shutdown=stop_bot)



# ===== E N D ===================================================================








# def register_all_middlewares(dp, config):
#     dp.setup_middleware(EnvironmentMiddleware(config=config))


# def register_all_filters(dp):
#     dp.filters_factory.bind(AdminFilter)


# def register_all_handlers(dp):
#     register_admin(dp)
#     register_user(dp)

#     register_echo(dp)


# async def main():
#     logging.basicConfig(
#         level=logging.INFO,
#         format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
#     )
#     logger.info("Starting bot")
#     config = load_config(".env")

#     storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
#     bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
#     dp = Dispatcher(bot, storage=storage)

#     bot['config'] = config

#     register_all_middlewares(dp, config)
#     register_all_filters(dp)
#     register_all_handlers(dp)

#     # start
#     try:
#         await dp.start_polling()
#     finally:
#         await dp.storage.close()
#         await dp.storage.wait_closed()
#         await bot.session.close()


# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         logger.error("Bot stopped!")
