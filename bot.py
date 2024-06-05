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


def check_matching_foot(question_text):
    try:
        question_mins = time_extractor.extract_time(question_text)
        with open('feet_json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for element in data:
            if int(element['mins']) + 1 >= int(question_mins) and int(element['mins']) - 1 <= int(question_mins):
                send_reaction(GROUP_ID, element['message_id'])
                reply_message(GROUP_ID, element['message_id'], question_text)
                element['message_id'] = None
        
        data = [item for item in data if item['message_id']]
        with open('feet.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)

    


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

