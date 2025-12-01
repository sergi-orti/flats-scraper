import telebot
import time

def send_telegram_message(token, chat_id, text):
    bot = telebot.TeleBot(token)
    try:
        bot.send_message(chat_id, text, parse_mode='HTML')
        time.sleep(1.5)  # delay para no spamear
    except Exception as e:
        print("Error enviando Telegram:", e)
