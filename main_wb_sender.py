import requests
from config import TOKEN
from config import GROUP_ID
import time
from bot import send_text_message


LOCAL_TIMEOUT = 10
GLOBAL_TIMEOUT = 20
BASE_URL = 'https://suppliers-api.wildberries.ru/'
BASE_QUESTIONS_URL = 'https://feedbacks-api.wildberries.ru/'

SUPPLY_NAME = 'Автобот (НЕ УДАЛЯТЬ НЕ ОТПРАВЛЯТЬ)'


headers = {'Authorization': TOKEN}


# def get_ununswered_questions():
#     url = 'api/v1/questions'
#     params = {'isAnswered': 'false', 'take': 10000, 'skip': 0, 'nmId': 231460239}
#     try:
#         resp = requests.get(BASE_QUESTIONS_URL + url, headers=headers, params=params)
#         question_objects = resp.json()['data']['questions']
#         return question_objects
#     except Exception as e:
#         print(e)


# def unswer_question(id):
#     url = 'api/v1/questions'
#     answer_text = """Здравствуйте. Спасибо за заказ. Ожидайте товар в выбранном Вами пункте выдачи."""
#     data = {'id': id, 'answer': {'text': answer_text}}
#     try:
#         requests.patch(BASE_QUESTIONS_URL + url, headers=headers, json=data)
#     except Exception as e:
#         print(e)


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
                send_text_message(GROUP_ID, f"{article} - {qr_id}")
            except Exception as e:
                print(e)
        time.sleep(GLOBAL_TIMEOUT)
