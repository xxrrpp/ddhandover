import telebot
import requests as rqst
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("xxxxx")
url = "xxxxx/"
ov = url + "ov/"
empty_product = url + "empr/"
empty_all = url + "emall/"
stock = url + "stock/"


@bot.message_handler(commands=["start"])
def welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("сводка")
    item2 = types.KeyboardButton("наличие")
    item3 = types.KeyboardButton("пустые все")
    item4 = types.KeyboardButton("пустые детально")

    markup.add(item1, item2, item3, item4)

    # bot.send_message(message.chat.id, "👋", )
    bot.send_message(message.chat.id, "👋👋👋", parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def lalala(message):
    # if message.chat.type == "private":
    if message.text in "сводка":
        msg = rqst.get(ov)
        if msg.status_code == 200:

            bot.send_message(message.chat.id, msg.text)
        else:
            bot.send_message(message.chat.id, "не удалось узнать")
    elif message.text in "наличие":
        msg = rqst.get(stock)
        if msg.status_code == 200:
            splitted_text = util.smart_split(msg.text, chars_per_string=3000)
            for text in splitted_text:
                bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "не удалось узнать")
    elif message.text in "пустые все":
        msg = rqst.get(empty_all)
        if msg.status_code == 200:
            splitted_text = util.smart_split(msg.text, chars_per_string=3000)
            for text in splitted_text:
                bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "не удалось узнать")
    elif message.text in "пустые детально":
        msg = rqst.get(empty_product)
        if msg.status_code == 200:
            splitted_text = util.smart_split(msg.text, chars_per_string=3000)
            for text in splitted_text:
                bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "не удалось узнать")
    else:
        bot.send_message(message.chat.id, "...")


bot.polling(none_stop=True)


# https://core.telegram.org/bots/api#available-methods
