import time, sqlite3 as sl3, random, json

import telebot as tbot

with open("key.json") as file:
    TOKEN = json.load(file)["key"]

bot = tbot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="Привет! Давай зарегестируемся! Введи /register")

@bot.message_handler(commands=["register"])
def register(message):
    bot.send_message(message.chat.id, text="Время регистрации! Введи своё имя")
    bot.register_next_step_handler(message, get_username)

def get_username(message):
    global name

    name = message.text.strip()

    try:
        connection = sl3.connect("base_test.sql")
        cur = connection.cursor()
        names_tuple = cur.execute("SELECT name FROM users;")
    except sl3.OperationalError as e:
        bot.send_message(message.chat.id, text=f"Упс! К сожалению, произошла ошибка {e} на стороне сервера. ")
    else:
        names = []
        for i in names_tuple:
            names.append(i[0])

        if name not in names:
            bot.send_message(message.chat.id, text="Отлично! А теперь введи свой пароль.")
            bot.register_next_step_handler(message, get_password)
        else:
            bot.send_message(message.chat.id, text="Это имя пользователя уже занято. Введи другое.")
            bot.register_next_step_handler(message, get_username)

    cur.close()
    connection.close()


def get_password(message):
    global name, password

    password = hash(message.text.strip())



    bot.send_message(message.chat.id, text="Если ты администатор, введи его пароль, иначе введи 0")
    bot.register_next_step_handler(message, get_role)

def get_role(message):
    global role

    try:
        int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, text="Некорректный ввод!")
        bot.register_next_step_handler(message, get_role)
        return
    else:
        if int(message.text) == 0:
            role = 0
        elif message.text == "5923":
            role = 1
        else:
            bot.send_message(message.chat.id, text="Неверный пароль!") 
            bot.register_next_step_handler(message, get_role)
            return
    
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
        if role == 1:
            info += f"Имя: {i[1]}, пароль (закодированный): {i[2]}, статус: {"администратор" if i[3] == 1 else "пользователь"}\n"
        else:
            info += f"Имя: {i[1]}, статус: {"администратор" if i[3] == 1 else "пользователь"}\n"

    bot.send_message(call.message.chat.id, text=f"Вот список пользователей: \n{info}")

def save_login():
    connection = sl3.connect("base_test.sql")
    cur = connection.cursor()
    cur.execute("INSERT INTO users (name, pass, role) VALUES ('%s', '%s', '%d')" % (name, password, role))



    connection.commit()
    cur.close()
    connection.close()


bot.polling()