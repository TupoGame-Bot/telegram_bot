import telebot
from telebot import types
import os

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📥 Пополнить", callback_data="deposit"))
    keyboard.add(types.InlineKeyboardButton("📤 Вывод", callback_data="withdraw"))
    keyboard.add(types.InlineKeyboardButton("📞 Помощь", callback_data="help"))

    welcome_text = """
Добро пожаловать в PayGo

📥 Пополнение: 0%
📤 Вывод: 0%
✅ Работаем: 24/7

🎟 *Промокод при регистрации:* 
💜 PAYGO
💜 До 35.000 сом бонуса при депозите

Оператор: @phelpgo_bot
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='Markdown')


# Обработка нажатий кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "deposit":
        # Создаём меню с сайтами
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("1xbet", callback_data="site_1xbet"))
        keyboard.add(types.InlineKeyboardButton("1win", callback_data="site_1win"))
        keyboard.add(types.InlineKeyboardButton("melbet", callback_data="site_melbet"))

        deposit_text = """
📥 Пополнить > Выберите сайт для пополнения

⚠️ Проверьте ваш ID еще раз
❌ Отменить пополнение невозможно
