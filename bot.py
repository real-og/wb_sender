import asyncio

from aiogram import Bot
from config import BOT_TOKEN


bot = Bot(BOT_TOKEN, parse_mode='HTML')


async def async_send_message(id, text):
    await bot.send_message(id, text)
    s = await bot.get_session()
    await s.close()


def send_text_message(id, text):
    asyncio.run(async_send_message(id, text))

