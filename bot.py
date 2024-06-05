import asyncio
from aiogram import Bot
from config import BOT_TOKEN, GROUP_ID
import requests
import json
import time_extractor


bot = Bot(BOT_TOKEN, parse_mode='HTML')


async def async_reply_message(group_id, message_id, text):
    try:
        await bot.send_message(group_id, text, reply_to_message_id=message_id)
        s = await bot.get_session()
        await s.close()
    except Exception as e:
        print(e)


def reply_message(group_id, message_id, text):
    asyncio.run(async_reply_message(group_id, message_id, text))



def send_reaction(chat_id, message_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction'
    reaction = json.dumps([{'type': 'emoji', 'emoji': '💯'}], ensure_ascii=False)
    params = {'chat_id': chat_id, 'message_id': message_id, 'reaction': reaction}
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(e)


async def async_send_message(id, text):
    try:
        mes = await bot.send_message(id, text)
        s = await bot.get_session()
        await s.close()
        return mes.message_id
    except Exception as e:
        print(e)



def send_text_message(id, text):
    message_id = asyncio.run(async_send_message(id, text))
    return message_id

