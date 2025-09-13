#Gfhdthev
#Логированием телеграмм бота

import os
import csv
import datetime

# Названия колонок для CSV-файла
COLUMNS = [
    "ID",        
    "User_id",   
    "Motion", #действие
    "Message_text", #если сообщение, то его текст
    "API",
    "API_answer", #ответ от апи
    "Date",
    "Time"
]

def now_time():
    return datetime.datetime.now().strftime('%d.%m.%Y')

def sec():
    return datetime.datetime.now().strftime('%H:%M:%S')

def logging(func):
    def wrapper(message, *args, **kwargs):
        result = func(message, *args, **kwargs)

        user_id = message.from_user.id
        text = message.text

        #проверяем, что нам надо записать
        if text in ['/start', 'СТАРТ']:
            motion = 'Command: start'
            message_text = 'None'
            api, api_answer = 'None', 'None'
        elif text in ['Weather', 'Dogs', 'Space']:
            motion = f'Button: {text}'
            message_text = 'None'
            api, api_answer = result
        else:
            motion = 'Keyboard typing'
            message_text = text
            api, api_answer = 'None', 'None'

        #смотрим нашу дирректорию на наличие файла
        log_path = 'logs.csv'
        file_exists = os.path.exists(log_path)

        #если файл есть, то смотрим id следующего лога
        if file_exists:
            with open(log_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # пропускаем заголовок
                last_id = sum(1 for _ in reader)
            record_id = last_id + 1
        else: #если нету, то 1
            record_id = 1

        with open(log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            #если файла не было, то добавляем заголовок
            if not file_exists:
                writer.writerow(COLUMNS)
            #записываем строку со значениями
            writer.writerow([
                record_id,
                user_id,
                motion,
                message_text,
                api,
                api_answer,
                now_time(),
                sec()
            ])

        return result

    return wrapper