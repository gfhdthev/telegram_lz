import os
import datetime
import pandas as pd
from functools import wraps

COLUMNS = [
    "ID",        # номер записи
    "User_id",   # id пользователя
    "Motion",
    "Message_text",
    "API",
    "API_answer",
    "Date",
    "Time"
]

def now_time():
    return datetime.datetime.now().strftime('%d.%m.%Y')

def sec():
    return datetime.datetime.now().strftime('%H:%M:%S')

def logging(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        # вызываем оригинальный хендлер
        result = func(message, *args, **kwargs)
        user_id = message.from_user.id

        text = getattr(message, 'text', '')
        api = 'None'
        api_answer = 'None'

        if text in ['/start', 'СТАРТ']:
            motion = 'Command: start'
            message_text = 'None'
        elif text in ['Weather', 'Dogs', 'Cosmos']:
            motion = f'Button: {text}'
            message_text = 'None'
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                api = result[0] or 'none'
                api_answer = result[1] or 'none'
        else:
            motion = 'Keyboard typing'
            message_text = text

        # формируем словарь для одной строки лога
        log_entry = {
            "ID":           None,
            "User_id":      user_id,
            "Motion":       motion,
            "Message_text": message_text,
            "API":          api,
            "API_answer":   api_answer,
            "Date":         now_time(),
            "Time":         sec()
        }

        log_path = os.path.join(os.getcwd(), 'logs.csv')

        if os.path.exists(log_path):
            # читаем существующий лог, чтобы узнать последний номер
            existing = pd.read_csv(log_path)
            last_no = existing['Id'].max() if 'Id' in existing.columns else len(existing)
            log_entry['Id'] = int(last_no) + 1

            # создаём DataFrame с заданным порядком колонок и дописываем
            pd.DataFrame([log_entry], columns=COLUMNS)\
                .to_csv(log_path, mode='a', index=False, header=False)
        else:
            # первый лог, номер = 1
            log_entry['Id'] = 1

            # создаём новый CSV с хедером и нужным порядком колонок
            pd.DataFrame([log_entry], columns=COLUMNS)\
                .to_csv(log_path, mode='w', index=False)

        return result

    return wrapper
