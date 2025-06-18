from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import logging
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(
    KeyboardButton("📊 Готовые таблицы"),
    KeyboardButton("🖼 Презентации"),
    KeyboardButton("📩 Рассылки")
)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет! Я нейро-продавец 🤖\n\nВыбери, что тебя интересует:",
        reply_markup=main_kb
    )

@dp.message_handler(lambda msg: msg.text in ["📊 Готовые таблицы", "🖼 Презентации", "📩 Рассылки"])
async def choose_product(message: types.Message):
    user_data[message.from_user.id] = {"product": message.text}
    await message.answer("Как тебя зовут?")

@dp.message_handler(lambda msg: msg.from_user.id in user_data and "name" not in user_data[msg.from_user.id])
async def get_name(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Как с тобой связаться? (Telegram @, email или номер)")

@dp.message_handler(lambda msg: msg.from_user.id in user_data and "contact" not in user_data[msg.from_user.id])
async def get_contact(message: types.Message):
    user_data[message.from_user.id]["contact"] = message.text
    await message.answer("Если хочешь, оставь комментарий к заказу. Или напиши «нет».")

@dp.message_handler(lambda msg: msg.from_user.id in user_data and "comment" not in user_data[msg.from_user.id])
async def get_comment(message: types.Message):
    user_data[message.from_user.id]["comment"] = message.text
    data = user_data[message.from_user.id]

    text = (
        f"📥 Новая заявка:\n\n"
        f"🛒 Продукт: {data['product']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Контакт: {data['contact']}\n"
        f"💬 Комментарий: {data['comment']}"
    )

    await bot.send_message(ADMIN_USERNAME, text)
    await message.answer("Спасибо! Твоя заявка принята ✅")
    del user_data[message.from_user.id]

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
