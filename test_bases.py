import time, sqlite3 as sl3, random, json

import telebot as tbot

with open("key.json") as file:
    TOKEN = json.load(file)["key"]

bot = tbot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    connection = sl3.connect("base.sql")
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))")



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
    bot.send_message(message.chat.id, "Ты зарегестрирован!")
    save_login()


def save_login():
    connection = sl3.connect("test.sql")
    cur = connection.cursor()
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))



    connection.commit()
    cur.close()
    connection.close()


bot.polling()