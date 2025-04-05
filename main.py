import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from rss_generator import generate_rss
import openai
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настраиваем бота с правильным parse_mode
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Настраиваем диспетчер
dp = Dispatcher(storage=MemoryStorage())

# Устанавливаем ключ OpenAI
openai.api_key = OPENAI_API_KEY


# Обработка новых постов из канала
@dp.channel_post(F.text | F.caption)
async def handle_post(msg: Message):
    text = msg.caption or msg.text
    if not text:
        return

    # Получаем картинку (если есть)
    image_url = None
    if msg.photo:
        file = await bot.get_file(msg.photo[-1].file_id)
        image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file.file_path}"

    # Загружаем промт для GPT
    with open("seo_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read().replace("{тут будет текст поста}", text)

    # Запрашиваем у GPT SEO-статью
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    seo_text = response["choices"][0]["message"]["content"]

    # Генерируем RSS-файл
    generate_rss(title="Новая статья из Telegram", body=seo_text, image_url=image_url)

    print("✅ Пост обработан и добавлен в RSS")


# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())