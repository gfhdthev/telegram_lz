import requests
from telebot import TeleBot, types
from secret import secrets
from logs import logging

bot = TeleBot(secrets['telegram_bot_token'])

bot.set_my_commands([
    types.BotCommand("start", "СТАРТ")
], language_code='ru')

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda m: m.text == 'СТАРТ', content_types=['text'])
@logging
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Weather"),
        types.KeyboardButton("Dogs"),
        types.KeyboardButton("Cosmos")
    )
    bot.send_message(
        message.chat.id,
        "Выберите категорию:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda msg: True, content_types=['text'])
@logging
def handle_buttons(message):
    text = message.text

    if text == "Weather":
        city = "Minsk"
        url = ("http://api.weatherapi.com/v1/current.json""?key={secrets['weatherapi_key']}&q={city}"
        )
        resp = requests.get(url)
        if resp.ok:
            data = resp.json()
            temp = data['current']['temp_c']
            desc = data['current']['condition']['text']
            answer = f"Погода в {city}: {temp}°C, {desc}"
        else:
            answer = "Не удалось получить данные о погоде."
        bot.send_message(message.chat.id, answer)

    elif text == "Dogs":
        url = "https://dog.ceo/api/breeds/image/random"
        resp = requests.get(url)
        if resp.ok:
            image_url = resp.json().get('message')
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.send_message(message.chat.id, "Не удалось загрузить изображение собаки.")

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

    else:
        bot.send_message(
            message.chat.id,
            f"Вы написали '{text}', я не знаю такой команды."
        )

if __name__ == "__main__":
    bot.polling(none_stop=True)
