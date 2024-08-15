123123123123123123123123123123123o

import subprocess
import time
import telebot
from pyowm import OWM
from telebot import types


owm = OWM('Your OWM API Token')



token='Your Telegram token'

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚡️ Світло вдома є?")
    btn2 = types.KeyboardButton("Погода")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привіт, я твій новий бот для перевірки світла та погоди", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "⚡️ Світло вдома є?":
        output = subprocess.run(['./svet.sh'], capture_output=True, text=True).stdout.strip()
        bot.send_message(message.chat.id, text=output)
    elif message.text == "Погода":
        markup = types.InlineKeyboardMarkup()
        cities = ['Kiev']
        for city in cities:
            btn = types.InlineKeyboardButton(city, callback_data=f'weather-{city}')
            markup.add(btn)
        bot.send_message(message.chat.id, text="Обери місто:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Нуууу, таке я поки що не вмію...")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    city = call.data.split('-')[1]
    # try:
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    # w.detailed_status         # 'clouds'
    # w.wind()                  # {'speed': 4.6, 'deg': 330}
    # w.humidity                # 87
    # w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    # w.rain                    # {}
    # w.heat_index              # None
    # w.clouds                  # 75
    bot.send_message(call.message.chat.id, f"Погода в місті {city}:\nТемпература: {w.temperature('celsius')['temp']}°C\nТемпература макс: {w.temperature('celsius')['temp_max']}°C, мін: {w.temperature('celsius')['temp_min']}°C\nХмарність: {w.detailed_status},{w.clouds}% . Дощ: { w.rain }.\nВологість: { w.humidity }")
    # except:
    #     bot.send_message(call.message.chat.id, f"Не вдалось отримати погоду для міста {city}. Спробуйте ще раз.")
bot.polling(none_stop=True)
