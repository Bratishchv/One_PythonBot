# One PythonBot
# Версия 1.0

import telebot, pickle
from telebot import TeleBot


def load_token():
    with open("token.dat", "rb") as file:
        return pickle.load(file)
    
bot = TeleBot(load_token())



@bot.message_handler(commands=["start"])
def start(message):
        bot.send_message(message.chat.id, text="Ку!")


bot.polling()