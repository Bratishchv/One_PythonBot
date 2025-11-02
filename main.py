# One PythonBot
# Версия 1.1

import telebot, pickle, random, time
from telebot import TeleBot
import wisdom, jokes


def load_token():
    with open("token.dat", "rb") as file:
        return pickle.load(file)
    
bot = TeleBot(load_token())



@bot.message_handler(commands=["start"])
def start(message):
     bot.send_message(message.chat.id, text="Ку!")

@bot.message_handler(commands=["wisdom"])
def print_wisdom(message):
    bot.reply_to(message, random.choice(wisdom.WISDOM))

@bot.message_handler(commands=["joke"])
def get_joke(message):
    bot.reply_to(message, random.choice(jokes.JOKES))

@bot.message_handler(commands=["money"])
def money(message):
    randint = random.randint(0, 100)
    bot.reply_to(message, text="Бросаю монетку...")
    time.sleep(2)

    if randint <= 50:
        bot.reply_to(message, text="Выпал орёл.")
    elif randint > 50:
        bot.reply_to(message, text="Выпала решка.")

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, text="Доступные команды:  \n/start\n/wisdom\n/joke\n/money\n/help") 


bot.polling()