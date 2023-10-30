from aiogram import Bot, Dispatcher
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_wb.handlers import register_user_handlers
from bot_wb.configuration import load_config
storage = MemoryStorage()



async def main() -> None:
    config = load_config(".env")
    bot = Bot(token = config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)
    register_user_handlers(dp)
    try:  
        await dp.start_polling()
    except Exception as _ex:
        print(f"{_ex}")


        
if __name__ == '__main__':
    asyncio.run(main())
