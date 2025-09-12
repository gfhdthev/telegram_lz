#Gfhdthev
#Логирование


#импортируем библиотеки
import os
import datetime
import pandas as pd

#берем имя пользователя компьютера
user=os.getlogin()

#работа с временем
def now_time():
    now_date=datetime.datetime.now().strftime('%d.%m.%Y') #полное время, включая год, месяц и т.д.
    return now_date
def sec():
    now_datetime=str(datetime.datetime.now()).split() #разделяем на дату и время
    current_time= now_datetime[1] #берем только время
    return current_time


def logging(func):
    def wrapper(message, *args, **kwargs):
        result = func(*args, **kwargs)

        if message.text not in ['Cosmos', 'Dogs', 'Weather']:
            motion = 'Keyboard typing'
            message_text = message.text
            api = 'NONE'
            api_answer = 'NONE'

        elif message.text in ['start']:
            motion = f'Button: {message.text}'
            message_text = 'NONE'
            api = 'NONE'
            api_answer = 'NONE'

        else:
            motion = f'Button: {message.text}'
            message_text = 'NONE'
            api = result[0]
            api_answer = result[1]

        if os.path.isfile('logs.csv'):#проверяем, существует ли файл
            file_df = pd.read_csv('logs.csv')
            data = {'': [len(file_df)], "User_id": [message.user.id], "Motion": motion, 'Message_text': message_text, 'API': api, 'API_answer': api_answer, "Date": [now_time()],"Time":[sec()]} #создаем столбцы
            df = pd.DataFrame(data) #создаем сам датафрейм
            df.to_csv('logs.csv', mode='a', index=False, header=False)
        else:
            data = {"User_id": [message.user.id], "Motion": motion, 'Message_text': message_text, 'API': api, 'API_answer': api_answer, "Date": [now_time()],"Time":[sec()]} #создаем столбцы
            df = pd.DataFrame(data) #создаем сам датафрейм
            df.to_csv('logs.csv')

        return result
    return wrapper