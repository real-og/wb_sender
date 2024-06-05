import json
from time_extractor import current_unix_timestamp, extract_time_mins
from config import GROUP_ID
import bot

def add_foot_and_update_json(file_path, new_element):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        data = [item for item in data if int(item['timestamp']) + 2 * 24 * 60 * 60 < current_unix_timestamp()]
        data.append(new_element)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)


def check_matching_foot(question_text):
    try:
        question_mins = extract_time_mins(question_text)
        with open('feet.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        isFound = False

        for element in data:
            if int(element['mins']) + 1 >= int(question_mins) and int(element['mins']) - 1 <= int(question_mins):
                bot.send_reaction(GROUP_ID, element['message_id'])
                bot.reply_message(GROUP_ID, element['message_id'], question_text)
                element['message_id'] = None
                isFound = True
                break

        if not isFound:
            bot.send_text_message(GROUP_ID, question_text)

        
        data = [item for item in data if item['message_id']]
        with open('feet.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)







