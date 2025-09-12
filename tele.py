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
    btn2 = types.KeyboardButton("Bogs")
    btn3 = types.KeyboardButton("Cosmos")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

@bot.message_handler(func=lambda msg: True, content_types=['text'])
@logging
def handle_buttons(message):
    text = message.text

    if text == "Weather":
        city = "Minsk"
        url = ("http://api.weatherapi.com/v1/current.json?key={secrets['weatherapi_key']}&q={city}")
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
        else:
            bot.send_message(message.chat.id, "Не удалось загрузить изображение собаки.")
        answer_to_log = ['dog.ceo', answer]

    elif text == "Cosmos":
        url = f"https://api.nasa.gov/planetary/apod?api_key={secrets['nasa_key']}"
        resp = requests.get(url)
        if resp.ok:
            data = resp.json()
            title = data.get('title', 'Без названия')
            explanation = data.get('explanation', 'Описание отсутствует')
            image_url = data.get('url')

            caption = f"{title}\n\n{explanation}"
            if len(caption) > 1024:
                caption = caption[:1021] + "..."
            bot.send_photo(message.chat.id, image_url, caption=caption)
        else:
            bot.send_message(message.chat.id, "Не удалось получить данные от NASA.")
        answer_to_log = ['nasa.gov', answer]

    else:
        bot.send_message(
            message.chat.id,
            f"Вы написали '{text}', я не знаю такой команды."
        )

    return answer_to_log

if __name__ == "__main__":
    bot.polling()
