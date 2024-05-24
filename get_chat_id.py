import asyncio

from aiogram import Bot
from config import BOT_TOKEN


bot = Bot(BOT_TOKEN, parse_mode='HTML')


async def async_get_updates():
    updates = await bot.get_updates()
    print(updates)
    s = await bot.get_session()
    await s.close()


def get_updates():
    asyncio.run(async_get_updates())

get_updates()