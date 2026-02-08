import telebot
from telebot import types
import os

TOKEN = os.environ.get("TOKEN")  # <- берём токен из Render
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("/help", "/info")
    bot.send_message(message.chat.id, "Привет! Я бот с кнопками 🤖", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "Вот список команд:\n/start\n/help\n/info")

@bot.message_handler(commands=['info'])
def info_cmd(message):
    bot.send_message(message.chat.id, "Я пример бота с кнопками и командами!")

bot.infinity_polling()


