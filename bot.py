import telebot
from telebot import types
import os

TOKEN = os.environ.get("TOKEN")  # токен из Render
bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    # Inline-кнопки без Баланса
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📥 Пополнение", callback_data="deposit"))
    keyboard.add(types.InlineKeyboardButton("📤 Вывод", callback_data="withdraw"))
    keyboard.add(types.InlineKeyboardButton("📞 Помощь", callback_data="help"))

    # Текст приветствия с промокодом и выделением
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

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "deposit":
        bot.answer_callback_query(call.id, "Для пополнения используйте PayGo или свяжитесь с оператором.")
        bot.send_message(call.message.chat.id, "💳 Выберите способ пополнения: ...")
    elif call.data == "withdraw":
        bot.answer_callback_query(call.id, "Для вывода средств свяжитесь с оператором.")
        bot.send_message(call.message.chat.id, "💸 Введите сумму для вывода: ...")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "Оператор: @phelpgo_bot")
        bot.send_message(call.message.chat.id, "Если возникли вопросы, пишите оператору.")

bot.infinity_polling()
