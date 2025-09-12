#Gfhdthev
#Лабоарторная работа №1. Создание телеграмм бота

from secret import secrets
from logs import logging

import telebot
from telebot import types
import requests

bot = telebot.TeleBot(secrets['telegram_bot_token'])

@logging
@bot.message_handler(commands=['start'])
def start(message:telebot.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Weather")
    btn2 = types.KeyboardButton("Dogs")
    btn3 = types.KeyboardButton("Cosmos")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

@logging
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Weather":
        city = "Minsk"
        url = f"http://api.weatherapi.com/v1/current.json?key={secrets['weatherapi_key']}&q={city}"
        response = requests.get(url).json()
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        answer = ['weatherapi.com', f"Погода в {city}: {temp}°C, {desc}"]
        bot.send_message(message.chat.id, answer[1])

    elif message.text == "Dogs":
        url = f"https://dog.ceo/api/breeds/image/random"
        response = requests.get(url).json()
        image_url = response['message']
        answer = ['dog.ceo', f"{image_url}"]
        bot.send_message(message.chat.id, answer[1])

    elif message.text == "Cosmos":
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        title = data.get('title', 'Без названия')
        explanation = data.get('explanation', 'Описание отсутствует')
        image_url = data['url']
        
        # Ограничиваем длину подписи до 1024 символов
        max_caption_length = 1024
        caption = f"{title}\n\n{explanation}"
        
        if len(caption) > max_caption_length:
            # Обрезаем текст и добавляем многоточие
            caption = caption[:max_caption_length-3] + "..."
        
        # Отправляем фото с обрезанной подписью
        bot.send_photo(
            message.chat.id,
            image_url,
            caption=caption
        )
        answer = ['nasa.gov', caption]

    return answer

@logging
@bot.message_handler(content_types=['text'])
def handle_messages(message):
    bot.send_message(message.chat.id, f'Вы написали \'{message.text}\', я не знаю такой команды')

bot.polling(none_stop=True)