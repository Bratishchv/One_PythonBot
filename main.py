# One PythonBot
# Версия 1.4

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
timer_setup = False


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="Ку! Я удобный бот:)")

@bot.message_handler(commands=["wisdom"])
def print_wisdom(message):
    bot.reply_to(message, random.choice(wisdom.WISDOM))

@bot.message_handler(commands=["joke"])
def get_joke(message):
    bot.reply_to(message, random.choice(jokes.JOKES))

@bot.message_handler(commands=["machine"])
def money(message):
    randint = random.randint(0, 100)
    bot.reply_to(message, text="Раскручиваю автомат...")

    bot.send_message(message.chat.id, text="\U0001F3B0")
    time.sleep(2)

    if randint <= 50:
        bot.reply_to(message, text="Вы выиграли.")
    elif randint > 50:
        bot.reply_to(message, text="Вы проиграли.")

@bot.message_handler(commands=["cube"])
def cube(message):
    bot_mess = bot.send_message(message.chat.id, "Бросаю кубик...")
    bot.reply_to(bot_mess, "\U0001F3B2")

    bot.send_message(bot_mess.chat.id, str(random.randint(1, 6)))

@bot.message_handler(commands=["timer"])
def timer(message):
    global timer_setup
    bot.send_message(message.chat.id, "Введите время в секундах устанавлеммого таймера:")
    timer_setup = True

@bot.message_handler(content_types=["text"])
def get_timer_time(message):
    global timer_setup
    if timer_setup:
        global timer_time, start_time
        try:
            timer_time = int(message.text)
        except:
            bot.reply_to(message, "Это не число!")
        else:
            if timer_time > 300:
                bot.reply_to(message, "\U0001F6D1 Слишком долго! Максиум 5 минут (300 секунд).")
            else:
                bot.reply_to(message, f"Ок. Таймер на {timer_time} секунд. Скоро сработает! \U000023F3")
                start_time = time.time_ns() / 1_000_000_000
                timer_setup = False
                time.sleep(timer_time)
                bot_mess = bot.send_message(message.chat.id, "\U000023F2")
                bot.reply_to(bot_mess, "Конец таймера!")

class Exit(Exception): pass

@bot.message_handler(commands=["stop", "break"])
def stop(message): 
    bot.send_message(message.chat.id, text="Выключаюсь..."); 
    raise Exit("The user has logged out of the program.")
    bot.stop_bot()

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    bot.reply_to(message, "Я пока не умею разпозновать голос. " +
                          "Напиши текстом!")

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, text="Доступные команды:  \n/start\n/wisdom\n/joke\n/machine\n/cube\n/timer\n/help") 


@bot.message_handler(content_types=["text"])
def text_test(message):
    if timer_setup == False and message.text.lower() == "тест":
        bot.send_message(message.chat.id, "Успех!")



bot.polling()