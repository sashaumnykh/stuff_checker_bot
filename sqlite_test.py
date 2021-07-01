import telebot
import sqlite3

bot = telebot.TeleBot('1880633054:AAGQyhqzRDHWhFkjhfd3OEtWGM0PpIu8rxM')

conn = sqlite3.connect('C:/Users/alexa/OneDrive/Документы/projects/stuff_checker/db/stuffcheckerdb.db', check_same_thread=False)
cursor = conn.cursor()

#
def creator(user_id):
    tableName = 'user_' + str(user_id)
    print(tableName)
    stmt = """CREATE TABLE IF NOT EXISTS """ + tableName + """ (stuff_name TEXT, date TEXT )"""
    conn.execute(stmt)
    conn.commit()
    tb_exist = conn.execute(f"""SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{tableName}'""")
    print(tb_exist.fetchone())
    #stmt = """INSERT INTO user_353118024 VALUES (1)"""
    #conn.execute(stmt)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет,  + {message.from_user.first_name}  + !')
    creator(message.from_user.id)

if __name__ == '__main__':
     bot.polling(none_stop=True)