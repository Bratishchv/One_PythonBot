# One PythonBot
# Версия 1.2

import telebot, pickle, random, time
from telebot import TeleBot
import wisdom, jokes

"""
def load_token():
    with open("token.dat", "rb") as file:
        return pickle.load(file)
"""

TOKEN = '8207941725:AAHlCI0KzzDU9Vg0Yk-gh2UB2_plyEhg_-M'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="Ку! Я удобный бот:)")

@bot.message_handler(commands=["wisdom"])
def print_wisdom(message):
    bot.reply_to(message, random.choice(wisdom.WISDOM))

@bot.message_handler(commands=["joke"])
def get_joke(message):
    bot.reply_to(message, random.choice(jokes.JOKES))

@bot.message_handler(commands=["random"])
def money(message):
    randint = random.randint(0, 100)
    bot.reply_to(message, text="Раскручиваю автомат...")

    bot.send_message(message.chat.id, text="\U0001F3B0")
    time.sleep(2)

    if randint <= 50:
        bot.reply_to(message, text="Вы выиграли.")
    elif randint > 50:
        bot.reply_to(message, text="Вы проиграли.")

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, text="Доступные команды:  \n/start\n/wisdom\n/joke\n/money\n/help") 


@bot.message_handler(content_types=["text"])
def text_test(message):
    if message.text.lower() == "тест":
        bot.send_message(message.chat.id, "Успех!")



bot.polling()