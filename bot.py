import telebot

TOKEN = "8535847780:AAGPgHzEurss5sI2KjHFB7x9ICcipBpLQtI"

bot = telebot.TeleBot(TOKEN, parse_mode=None)

try:
    print(bot.get_me())
except Exception as e:
    print("Ошибка подключения:", e)
