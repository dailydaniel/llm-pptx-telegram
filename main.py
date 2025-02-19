from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
import os
from src.telebot.handlers import process_user_prompt
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher(bot)

    dp.register_message_handler(process_user_prompt, content_types=["text"])

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
