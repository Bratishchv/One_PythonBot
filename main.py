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
timer_setup1 = False
timer_setup2 = False



@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="Ку! Я удобный бот:)")

@bot.message_handler(commands=["wisdom"])
def print_wisdom(message):
    bot.reply_to(message, random.choice(wisdom.WISDOM))

@bot.message_handler(commands=["joke"])
def get_joke(message):
    bot.reply_to(message, random.choice(jokes.JOKES))

@bot.message_handler(commands=["coin"])
def coin(message):
    bot_mess = bot.send_message(message.chat.id, "Подбрасываю монетку...")
    coins = ("л орёл", "ла решка")
    time.sleep(2)

    bot.reply_to(bot_mess, f"Выпа{random.choice(coins)}.")

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
    global timer_setup1
    bot.send_message(message.chat.id, "Введите время в минутах устанавлеммого таймера (секунды вы ещё сможете указать):")
    timer_setup1 = True

@bot.message_handler(content_types=["text"])
def get_timer_time_seckonds(message):
    global timer_setup1, timer_setup2
    if timer_setup2:
        global timer_time
        try:
            timer_time_seckonds = int(message.text)
        except:
            bot.reply_to(message, "Это не число!")
        else:
            if timer_time_seckonds >= 60:
                bot.reply_to(message, "\U0001F6D1 60 секунд -- это минута! Минуты нужно писать в" + 
                                      "минуты, а секунды -- в секунды!")
            else:
                timer_setup1 = False
                timer_setup2 = True
                timer_time += timer_time_seckonds
                bot.reply_to(message, f"Ок. Таймер на {timer_time // 60} минут и на {timer_time - timer_time // 60} секунд. " + 
                                       "Скоро сработает! \U000023F3")
                
                if timer_time >= 300:
                    timer_time_minets = timer_time // 60
                    if timer_time_minets != 0:
                        for i in range(1, timer_time_minets):
                            time.sleep(60)
                    else:
                        time.sleep(timer_time)

                bot_mess = bot.send_message(message.chat.id, "\U000023F2")
                bot.reply_to(bot_mess, "Конец таймера!")

@bot.message_handler(content_types=["text"])
def get_timer_time_min(message):
    global timer_setup1, timer_setup2
    if timer_setup1:
        global timer_time, timer_time
        try:
            timer_time_minets = int(message.text)
        except:
            bot.reply_to(message, "Это не число!")
        else:
            if timer_time_minets > 5:
                bot.reply_to(message, "\U0001F6D1 Слишком долго! Максиум 5 минут.")
            else:
                timer_time += 60 * timer_time_minets
                timer_setup1 = False
                bot.send_message(message.chat.id, "А теперь введите дополнительные секунды.")
                timer_setup2 = True
 

@bot.message_handler(commands=["get_password"])
def get_password(message):
    import string
    chars = string.ascii_letters + string.digits + string.punctuation
    #chars = string.printable
    password = "".join(random.sample(chars, 16))
    bot.send_message(message.chat.id, text=f"Сгенерироваемый пароль: {password}")


class Exit(Exception): pass

@bot.message_handler(commands=["stop", "break"])
def stop(message): 
    bot.send_message(message.chat.id, text="Выключаюсь..."); 
    raise Exit("The user has logged out of the program.")

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    bot.reply_to(message, "Я пока не умею разпозновать голос. " +
                          "Напиши текстом!")

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, 
                 text = f"""Справка по командам: 
start - Приветствие
wisdom - Получить мудрость
joke - Получить шутку
machine - Покрутить автомат
cube - Кинуть кубик
coin - Подбросить монетку
timer - Завести таймер
help - Помощь"""                 
                ) 

@bot.message_handler(content_types=["text"])
def text_test(message):
    if not timer_setup1 and not timer_setup2 and message.text.lower() == "тест":
        bot.send_message(message.chat.id, "Успех!")



bot.polling()