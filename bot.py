import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

WEBAPP_URL = "https://ddorogoff.github.io/magic/magic.html"

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


def webapp_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Открыть мини-апп",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])


@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Нажми кнопку — откроется мини-апп с предсказанием.",
        reply_markup=webapp_kb()
    )


@dp.message(F.web_app_data)
async def on_webapp_data(message: Message):
    try:
        payload = json.loads(message.web_app_data.data)
        logging.info(payload)
    except Exception:
        payload = {"action": "opened"}

    await message.answer("Готово. Заходи в мини-апп снова, когда захочешь новое предсказание.")


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не найден")

    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
