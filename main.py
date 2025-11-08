# One PythonBot
# Версия 1.3

import telebot as tbot, pickle, random, time, json
import wisdom, jokes

"""
def load_token():
    with open("token.dat", "rb") as file:
        return pickle.load(file)
"""

with open("key.json") as file:
    TOKEN = json.load(file)["key"]

bot = tbot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="Ку! Я удобный бот:)")

@bot.message_handler(commands=["wisdom"])
def print_wisdom(message):
    bot.reply_to(message, random.choice(wisdom.WISDOM))

@bot.message_handler(commands=["joke"])
def get_joke(message):
    bot.reply_to(message, random.choice(jokes.JOKES))

@bot.message_handler(commands=["machine", "money"])
def money(message):
    randint = random.randint(0, 100)
    bot.reply_to(message, text="Раскручиваю автомат...")

    bot.send_message(message.chat.id, text="\U0001F3B0")
    time.sleep(2)

    if randint <= 50:
        bot.reply_to(message, text="Вы выиграли.")
    elif randint > 50:
        bot.reply_to(message, text="Вы проиграли.")


@bot.message_handler(commands=["stop", "break"])
def stop(message): 
    bot.send_message(message.chat.id, text="Выключаюсь..."); 
    bot.stop_bot()


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, text="Доступные команды:  \n/start\n/wisdom\n/joke\n/machine\n/help") 


@bot.message_handler(content_types=["text"])
def text_test(message):
    if message.text.lower() == "тест":
        bot.send_message(message.chat.id, "Успех!")



bot.polling()