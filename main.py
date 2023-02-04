import sqlite3
import telebot

import os
from dotenv import load_dotenv
load_dotenv()
os.getenv("TELEGRAM_BOT_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите адрес дома, я покажу где стоит моноблок, и какие дома к нему подключены")


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == message.text:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        with conn as db:
            cursor = db.cursor()
        print(message.text)
        cursor.execute(f"SELECT * FROM adressNew WHERE street = '{message.text}'")
        result = cursor.fetchall()
        for row in result:
            cursor.execute(f"SELECT * FROM adressNew WHERE id = '{row[0]}' ORDER BY street ")
        result = cursor.fetchall()
        for row in result:
            print(row[1], row[2], row[3], row[4])
            bot.send_message(message.chat.id, row[1] + '\n' + row[2] + ' ' + row[4] + '\n' +  row[3] + ' ' + row[5] + ' ' + row[6], parse_mode='html')

bot.infinity_polling()
