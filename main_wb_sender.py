import requests
from config import TOKEN
from config import GROUP_ID
import time
from bot import send_text_message


LOCAL_TIMEOUT = 5
GLOBAL_TIMEOUT = 15
BASE_URL = 'https://suppliers-api.wildberries.ru/'


headers = {'Authorization': TOKEN}


def get_supply_id(name):
    url = 'api/v3/supplies'
    params = {'limit': 1000, 'next': 0}
    resp = requests.get(BASE_URL + url, headers=headers, params=params)
    supplies = resp.json().get('supplies')
    for supply in supplies:
        if supply.get('name') == name:
            return supply.get('id')


def get_new_orders():
    url = 'api/v3/orders/new'
    try:
        resp = requests.get(BASE_URL + url, headers=headers)
        return resp.json().get('orders')
    except:
        print(resp)
        return []
    

def create_supply(name):
    url = f'api/v3/supplies'
    data = {'name': name}
    resp = requests.post(BASE_URL + url, headers=headers, json=data)
    return resp.json().get('id')


def add_order_to_supply(order_id, supply_id):
    url = f'api/v3/supplies/{supply_id}/orders/{order_id}'
    requests.patch(BASE_URL + url, headers=headers)


def get_qr_id(order_id):
    url = f'api/v3/orders/stickers'
    data = {'orders': [order_id]}
    params = {'type': 'svg', 'width': 40, 'height': 30}
    resp = requests.post(BASE_URL + url, headers=headers, json=data, params=params)
    return resp.json().get('stickers')[0].get('partB')


if __name__ == '__main__':
    supply_id = get_supply_id(name='Авто')
    while True:
        if supply_id is None:
            supply_id = create_supply(name='Авто')
        new_orders = get_new_orders()
        for order in new_orders:
            order_id = order.get('id')
            add_order_to_supply(order_id, supply_id)
            time.sleep(LOCAL_TIMEOUT)
            qr_id = get_qr_id(order_id)
            article = order.get('article')
            send_text_message(GROUP_ID, f"{article} - {qr_id}")
        time.sleep(GLOBAL_TIMEOUT)
