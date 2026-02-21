import os
import asyncio
import random
import datetime
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiohttp import web

from config import BOT_TOKEN
import storage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ===== START =====
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        "👋 Привет! Я универсальный бот.\n\n"
        "📌 /add текст — добавить задачу\n"
        "📋 /list — список задач\n"
        "✅ /done номер — выполнить задачу\n"
        "🧹 /clear — очистить список\n\n"
        "⏰ /time — текущее время\n"
        "🌦 /weather город — погода\n"
        "💱 /rates — курсы валют\n"
        "🎲 /random — случайное число\n"
        "ℹ️ /help — помощь"
    )

# ===== HELP =====
@dp.message_handler(commands=["help"])
async def help_cmd(msg: types.Message):
    await msg.answer("Просто напиши команду из /start 👌")

# ===== TODO =====
@dp.message_handler(commands=["add"])
async def add_task(msg: types.Message):
    text = msg.get_args()
    if not text:
        return await msg.answer("❗ Напиши текст задачи")
    storage.add_task(msg.from_user.id, text)
    await msg.answer("✅ Задача добавлена")

@dp.message_handler(commands=["list"])
async def list_tasks(msg: types.Message):
    tasks = storage.get_tasks(msg.from_user.id)
    if not tasks:
        return await msg.answer("📭 Список пуст")
    text = ""
    for i, t in enumerate(tasks):
        text += f"{i+1}. {'✅' if t['done'] else '⏳'} {t['text']}\n"
    await msg.answer(text)

@dp.message_handler(commands=["done"])
async def done_task(msg: types.Message):
    try:
        index = int(msg.get_args()) - 1
    except:
        return await msg.answer("❗ Укажи номер")
    if storage.done_task(msg.from_user.id, index):
        await msg.answer("🎉 Готово!")
    else:
        await msg.answer("❌ Ошибка")

@dp.message_handler(commands=["clear"])
async def clear(msg: types.Message):
    storage.clear_tasks(msg.from_user.id)
    await msg.answer("🧹 Очищено")

# ===== TIME =====
@dp.message_handler(commands=["time"])
async def time_cmd(msg: types.Message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    await msg.answer(f"🕒 Сейчас {now}")

# ===== RANDOM =====
@dp.message_handler(commands=["random"])
async def random_cmd(msg: types.Message):
    await msg.answer(f"🎲 {random.randint(1, 100)}")

# ===== WEATHER =====
@dp.message_handler(commands=["weather"])
async def weather(msg: types.Message):
    city = msg.get_args()
    if not city:
        return await msg.answer("❗ Напиши город")

    url = f"https://wttr.in/{city}?format=3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            await msg.answer(await r.text())

# ===== RATES =====
@dp.message_handler(commands=["rates"])
async def rates(msg: types.Message):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.exchangerate.host/latest?base=USD") as r:
            data = await r.json()
            usd = data["rates"]["RUB"]
            eur = data["rates"]["EUR"]
            await msg.answer(f"💱 USD → RUB: {usd:.2f}\n💱 USD → EUR: {eur:.2f}")

# ===== RENDER WEB SERVER =====
async def web_server():
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="Bot is alive"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()

async def main():
    await web_server()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
