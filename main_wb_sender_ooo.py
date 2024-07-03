import requests
from config import TOKEN, FOOT_ARTICLE, SUPPLY_NAME, GROUP_ID
import time
from bot import send_text_message
import json
import time_extractor
import json_reader


LOCAL_TIMEOUT = 10
GLOBAL_TIMEOUT = 20
BASE_URL = 'https://suppliers-api.wildberries.ru/'
BASE_QUESTIONS_URL = 'https://feedbacks-api.wildberries.ru/'


FOOT_ARTICLE = 'FOOTимя'
SUPPLY_NAME = 'Автобот (НЕ УДАЛЯТЬ НЕ ОТПРАВЛЯТЬ)'


headers = {'Authorization': TOKEN}


def get_unanswered_questions():
    url = 'api/v1/questions'
    params = {'isAnswered': 'false', 'take': 10000, 'skip': 0, 'nmId': 231460239}
    try:
        resp = requests.get(BASE_QUESTIONS_URL + url, headers=headers, params=params)
        question_objects = resp.json()['data']['questions']
        return question_objects
    except Exception as e:
        print(e)


def answer_question(id):
    url = 'api/v1/questions'
    answer_text = """Здравствуйте. Спасибо за заказ. Ожидайте товар в выбранном Вами пункте выдачи."""
    data = {'id': id, 'answer': {'text': answer_text}, 'state': 'wbRu'}
    try:
        resp = requests.patch(BASE_QUESTIONS_URL + url, headers=headers, json=data)
        print(resp.text)
    except Exception as e:
        print(e)


def get_feet():
    url = 'api/v3/orders'
    from_time = int(time.time()) - 7 * 24 * 60 * 60
    params = {'limit': 1000, 'next': 0, 'dateFrom': from_time}
    try:
        resp = requests.get(BASE_URL + url, headers=headers, params=params)
        orders = resp.json()['orders']
        feet = []
        for order in orders:
            if order['article'] == 'FOOTимя' and order['supplyId']:
                feet.append(order)
        with open('resp.json', 'w') as file:
            json.dump(feet, file, indent=4)
        return feet
    except Exception as e:
        print(e)
        return None




def get_supply_id(name):
    url = 'api/v3/supplies'
    params = {'limit': 1000, 'next': 0}
    try:
        resp = requests.get(BASE_URL + url, headers=headers, params=params)
        supplies = resp.json().get('supplies')
        for supply in supplies:
            if supply.get('name') == name:
                return supply.get('id')
    except Exception as e:
        print(e)
        return None


def get_new_orders():
    url = 'api/v3/orders/new'
    try:
        resp = requests.get(BASE_URL + url, headers=headers)
        return resp.json().get('orders')
    except Exception as e:
        print(e)
        return []
    

def create_supply(name):
    url = f'api/v3/supplies'
    data = {'name': name}
    try:
        resp = requests.post(BASE_URL + url, headers=headers, json=data)
        return resp.json().get('id')
    except Exception as e:
        print(e)
        return None


def add_order_to_supply(order_id, supply_id):
    url = f'api/v3/supplies/{supply_id}/orders/{order_id}'
    try:
        requests.patch(BASE_URL + url, headers=headers)
    except Exception as e:
        print(e)


def get_qr_id(order_id):
    url = f'api/v3/orders/stickers'
    data = {'orders': [order_id]}
    params = {'type': 'svg', 'width': 40, 'height': 30}
    try:
        resp = requests.post(BASE_URL + url, headers=headers, json=data, params=params)
        return resp.json().get('stickers')[0].get('partB')
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    supply_id = get_supply_id(name=SUPPLY_NAME)
    while True:
        if supply_id is None:
            supply_id = create_supply(name=SUPPLY_NAME)
        new_orders = get_new_orders()
        for order in new_orders:
            try:
                order_id = order.get('id')
                add_order_to_supply(order_id, supply_id)
                time.sleep(LOCAL_TIMEOUT)
                qr_id = get_qr_id(order_id)
                article = order.get('article')
                message_id = send_text_message(GROUP_ID, f'{article} - {qr_id}')
                if article == FOOT_ARTICLE:
                    # проверить формат 
                    timestamp = time_extractor.get_unix_from_str(str(order['createdAt']))
                    mins = time_extractor.get_minutes_from_str(str(order['createdAt']))
                    foot_element = {'timestamp': timestamp,
                                    'mins': mins,
                                    'message_id': int(message_id)}
                    json_reader.add_foot_and_update_json('feet.json', foot_element)
            except Exception as e:
                print(e)

        questions = get_unanswered_questions()
        if questions:
            for question in questions:
                question_id = question['id']
                question_text = question['text']
                if time_extractor.extract_time_mins(question_text):
                    answer_question(question_id)
                    json_reader.check_matching_foot(question_text)
                else:
                    send_text_message(GROUP_ID, question_text + "\n\nНе отвечено")

        time.sleep(GLOBAL_TIMEOUT)
