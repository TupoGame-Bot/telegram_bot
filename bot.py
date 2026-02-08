import telebot
from telebot import types
import os

TOKEN = os.environ.get("TOKEN")  # токен из Render
bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    # Клавиатура с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("💰 Баланс", "➕ Пополнить")
    keyboard.row("📤 Вывод", "ℹ️ Инфо")
    keyboard.row("📞 Поддержка")

    # Текст приветствия
    welcome_text = """
Добро пожаловать в PayGo

📥 Пополнение: 0%
📤 Вывод: 0%
✅ Работаем: 24/7

🎟 Промокод при регистрации: 
PAYGO
До 35.000 сом бонуса при депозите

Оператор: @phelpgo_bot
"""

    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

# Остальные команды
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "Вот список команд:\n/start\n/help\n/info")

@bot.message_handler(commands=['info'])
def info_cmd(message):
    bot.send_message(message.chat.id, "Я пример бота с кнопками и командами!")

bot.infinity_polling()
