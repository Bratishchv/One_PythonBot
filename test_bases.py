import time, sqlite3 as sl3, random, json

import telebot as tbot

with open("key.json") as file:
    TOKEN = json.load(file)["key"]

bot = tbot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    connection = sl3.connect("base_test.sql")
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50), roll integer)")



    connection.commit()
    cur.close()
    connection.close()
    bot.send_message(message.chat.id, text="Время регистрации! Введи своё имя")
    bot.register_next_step_handler(message, get_username)

def get_username(message):
    global name

    name = message.text.strip().capitalize()

    bot.send_message(message.chat.id, text="Отлично! А теперь введи свой пароль.")
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global name, password

    password = hash(message.text.strip())



    bot.send_message(message.chat.id, text="Если ты администатор, введи его пароль, иначе введи 0")
    bot.register_next_step_handler(message, get_roll)

def get_roll(message):
    global roll

    if int(message.text) == 0:
        roll = 0
    elif message.text == "5923":
        roll = 1
    else:
        bot.send_message(message.chat.id, text="Непонятный ввод!") 
        get_roll(message)
    
    markup = tbot.types.InlineKeyboardMarkup()
    markup.add(tbot.types.InlineKeyboardButton(text="Список пользователей",
                                               callback_data="users"))
    
    bot.send_message(message.chat.id, "Ты зарегестрирован!", reply_markup=markup)

    save_login()

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    connection = sl3.connect("base_test.sql")
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    connection.commit()
    cur.close()
    connection.close()

    info = ""
    for i in users:
        if roll == 1:
            info += f"Имя: {i[1]}, пароль (закодированный): {i[2]}, статус: {i[3]}\n"
        else:
            info += f"Имя: {i[1]}, статус: {i[3]}\n"

    bot.send_message(call.message.chat.id, text=f"Вот список пользователей: \n{info}")

def save_login():
    connection = sl3.connect("base_test.sql")
    cur = connection.cursor()
    cur.execute("INSERT INTO users (name, pass, roll) VALUES ('%s', '%s', '%d')" % (name, password, roll))



    connection.commit()
    cur.close()
    connection.close()


bot.polling()