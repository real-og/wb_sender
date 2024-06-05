# import main_wb_sender
# import datetime
# import requests
# import bot
# import asyncio

# def get_hours_and_minutes_msk(iso_string):
#     # Парсим строку в объект datetime
#     dt = datetime.datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
    
#     # Извлекаем часы и минуты
#     hours = dt.hour + 3
#     minutes = dt.minute
    
#     return hours, minutes
# print(main_wb_sender.get_feet())
# print(main_wb_sender.get_unanswered_questions())

# print(main_wb_sender.answer_question('3mwE4o8BVtRu7cDDGJZI'))

# print(bot.send_text_message(-1002196923729, 'y', 'i', 'f', 'f'))
# print(bot.send_reaction(-1002196923729, 5))
# print(bot.send_text_message(-1002196923729, 'y'))
# original_array = [1, 2, 3, 4, 5]

# reversed_array = original_array[::-1]
# print(reversed_array)

# import time_extractor
# print(time_extractor.current_unix_timestamp())
# print(time_extractor.get_minutes_from_str('2022-05-04T07:56:29Z'))
# print(time_extractor.get_unix_from_str('2022-05-04T07:56:29Z'))
# print(time_extractor.extract_time_mins('Время заказа 10:34,девочка, Степанида.'))
# print(time_extractor.extract_time_mins('04.06.2024 время заказа 9:49; мальчик Ярослав'))
# print(time_extractor.extract_time_mins('3 июня, 12:16, девочка Доминика'))
# print(time_extractor.extract_time_mins('Время заказа 13:11, мальчик, Марк'))
# print(time_extractor.extract_time_mins('15:19 мальчик,Руслан'))
# print(time_extractor.extract_time_mins('20.46 девочка Таисия'))

# import bot

# print(bot.send_text_message(-1002196923729, 'u'))
# bot.send_reaction(-1002196923729, 21)
# bot.reply_message(-1002196923729, 22, 'ff')

import json_reader

json_reader.check_matching_foot('vfkmxbr слава 20:35')
