from datetime import time

import dateparser
import telebot
import sqlite3
import datetime
from datetime import datetime, timezone, timedelta
import config

# from telegram.ext import CommandHandler, Updater

#updater = Updater('token', use_context=True)
#job_queue = updater.job_queu

bot = telebot.TeleBot('token')
conn = sqlite3.connect('db adress',
                       check_same_thread=False)
cursor = conn.cursor()

global table_name
table_name = 'users_items'

# create a table for a new user
def creator(user_id):
    table_name = 'user_' + str(user_id)
    stmt = """CREATE TABLE IF NOT EXISTS """ + table_name + """ (stuff_name TEXT, date TEXT )"""
    conn.execute(stmt)
    conn.commit()
    # tb_exist = conn.execute(f"""SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name}'""")
    # print(tb_exist.fetchone())


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    #creator(message.from_user.id)


@bot.message_handler(commands=['help'])
def helper(message):
    msg = "для работы со мной тебе пригодятся следующие команды: \n\
    /add — добавляет новую вещь в список;\n\
    /getall — показывает все вещи, что ты добавил(а) ранее;"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands="add")
def add(message):
    msg = "опишите вещь в формате 'название вещи: срок хранения', например: \n\
                коробка от мультиварки: 28 октября 2021\n\
    срок хранения - день, когда вещь можно выбросить"
    message = bot.reply_to(message, msg)
    bot.register_next_step_handler(message, add_new_stuff)


def add_new_stuff(message):
    txt = message.text
    user_id = message.from_user.id
    name, date = txt.split(":")[0].strip(), txt.split(":")[1].strip()
    date = str(dateparser.parse(date, languages=['ru'])).split(' ')[0]
    conn.execute(
        f"""INSERT INTO {table_name} VALUES (?, ?, ?)""", (user_id, name, date)
    )
    conn.commit()


@bot.message_handler(commands="getall")
def get_all(message):
    items = conn.execute(f"""SELECT * FROM {table_name}""").fetchall()
    msg = ''
    user_id = str(message.from_user.id)
    for i in items:
        item = list(i)
        if str(item[0]) == user_id:
            msg += str(item[1]) + ': ' + str(item[2]) + '\n'
    bot.send_message(message.chat.id, msg)

if __name__ == '__main__':
    bot.polling(none_stop=True)

