from aiogram import Bot, Dispatcher

from handlers.commands import router as command_router
from handlers.questions import router as question_router


API_TOKEN: str = "PUT_TOKEN_HERE"


bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

dp.include_router(command_router)
dp.include_router(question_router)

if __name__ == "__main__":
    dp.run_polling(bot)
