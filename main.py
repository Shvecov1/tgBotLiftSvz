import sqlite3
import telebot
from telebot import types
import os
from dotenv import load_dotenv


load_dotenv()
os.getenv("TELEGRAM_BOT_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет, отправь логин и пароль")



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите логин и пароль")
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    print('ID: ' + str(message.from_user.id), 'TEXT: ' + message.text)

    if message.from_user.id == 544579688 or 123495858:
        conn = sqlite3.connect('database.db', check_same_thread=False)
        with conn as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT COUNT(street) FROM adressNew WHERE street LIKE '%{message.text}%' ORDER BY street ")
            result = cursor.fetchall()
            for test in result:
                print(test)
            res = int(''.join(map(str, test)))
            if res > 20 or res == 0:
                bot.send_message(message.chat.id, '❗Количество результатов ' + str(res) + '❗' + '\n' +  ' Уточните запрос, или введите номер дома.')
            else:
                bot.send_message(message.chat.id, '⌛Запрос выполняется...⌛')
                cursor.execute(f"SELECT * FROM adressNew WHERE street LIKE '%{message.text}%' ORDER BY street ")
                result = cursor.fetchall()
                for row in result:
                    markup = types.InlineKeyboardMarkup()
                    item = types.InlineKeyboardButton(row[2], callback_data=row[2])
                    markup.add(item)
                    print(row[2])
                    bot.send_message(message.chat.id,row[2],parse_mode='html', reply_markup=markup)
                bot.send_message(message.chat.id, '🟩Запрос выполнен!🟩')
    else:
        bot.send_message(message.chat.id, 'Нет доступа, для получения доступа скиньте ваш ID\n' + 'ID: ' + str(message.from_user.id))

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == call.data:
            bot.send_message(call.message.chat.id, '⌛Запрос выполняется...⌛')
            conn = sqlite3.connect('database.db', check_same_thread=False)
            with conn as db:
                cursor = db.cursor()
            cursor.execute(f"SELECT * FROM adressNew WHERE street = '{call.data}'")
            result = cursor.fetchall()
            for row in result:
                cursor.execute(f"SELECT * FROM adressNew WHERE id = '{row[0]}' ORDER BY street ")
            result = cursor.fetchall()

            for row in result:
                print(row[1], row[2], row[3], row[4])
                bot.send_message(call.message.chat.id, row[1] + '\n' + row[2] + ' ' + row[4] + '\n' + row[3] + ' ' + row[5] + ' ' + row[6] + '\n' + row[7] + '\n' + row[8], parse_mode='html')
    bot.send_message(call.message.chat.id, '🟩Запрос выполнен!🟩')
bot.infinity_polling()
