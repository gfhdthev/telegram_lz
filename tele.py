#Gfhdthev
#Лабораторная работа 1

import requests
from telebot import TeleBot, types

from secret import secrets
from logs import logging

bot = TeleBot(secrets['telegram_bot_token'])

@bot.message_handler(commands=['start'])
@logging
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Weather")
    btn2 = types.KeyboardButton("Dogs")
    btn3 = types.KeyboardButton("Space")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

@bot.message_handler(func=lambda msg: True, content_types=['text'])
@logging
def handle_buttons(message):
    text = message.text

    if text == "Weather":
        city = "Minsk"
        url = f"http://api.weatherapi.com/v1/current.json?key={secrets['weatherapi_key']}&q={city}"
        resp = requests.get(url)
        if resp.ok:
            data = resp.json()
            temp = data['current']['temp_c']
            desc = data['current']['condition']['text']
            answer = f"Погода в {city}: {temp}°C, {desc}"
        else:
            answer = "Не удалось получить данные о погоде."
        answer_to_log = ['weatherapi.com', answer]
        bot.send_message(message.chat.id, answer)

    elif text == "Dogs":
        url = "https://dog.ceo/api/breeds/image/random"
        resp = requests.get(url)
        if resp.ok:
            image_url = resp.json().get('message')
            bot.send_photo(message.chat.id, image_url)
            answer = image_url
        else:
            answer = "Не удалось загрузить изображение собаки."
            bot.send_message(message.chat.id, answer)
        answer_to_log = ['dog.ceo', answer]

    elif text == "Space":
        url = f"https://api.nasa.gov/planetary/apod?api_key={secrets['nasa_key']}"
        resp = requests.get(url)
        if resp.ok: #если ответ есть, то гуд
            data = resp.json()
            title = data.get('title', 'Без названия')
            explanation = data.get('explanation', 'Описание отсутствует')
            image_url = data.get('url')

            caption = f"{title}\n\n{explanation}"
            if len(caption) > 1024: #отправляем только первый 1024 символа, потому что тг больше не пропускает
                caption = caption[:1021] + "..."
            bot.send_photo(message.chat.id, image_url, caption=caption)
            answer = f'{image_url}, {title}'
        else:
            answer = "Не удалось получить данные от NASA."
            bot.send_message(message.chat.id, answer)
        answer_to_log = ['nasa.gov', answer]

    else:
        bot.send_message(
            message.chat.id,
            f"Вы написали '{text}', я не знаю такой команды."
        )
        answer_to_log = ['None', 'None']

    return answer_to_log

if __name__ == "__main__":
    bot.polling()
