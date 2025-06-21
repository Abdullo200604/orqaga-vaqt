from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
import asyncio
import logging
from datetime import datetime, timedelta
from aiogram.filters import Command


TOKEN = "7721595571:AAErmLr9IMZyFWw5WR86fKEIxdq9_hG1INs"  # <-- o'zingizning token bilan almashtiring
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Assalomu Aleykum ")

@dp.message(F.text.regexp(r'^\d{2}:\d{2}$'))  # faqat masalan "00:50" formatidagi vaqtni qabul qiladi
async def timer_handler(msg: Message):
    try:
        target_time = datetime.strptime(msg.text, "%H:%M").time()
        now = datetime.now()
        target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)

        if target_datetime < now:
            target_datetime += timedelta(days=1)  # Agar vaqt o‘tgasa, ertangi kunni hisoblaydi

        message = await msg.answer("⏳ Tayyorlanmoqda...")

        while True:
            now = datetime.now()
            if now >= target_datetime:
                await message.edit_text("⏰ Vaqt yetdi!")
                break
            remaining = target_datetime - now
            minutes = remaining.seconds // 60
            seconds = remaining.seconds % 60
            await message.edit_text(f"⏳ Qolgan vaqt: {minutes:02}:{seconds:02}")
            await asyncio.sleep(60 - now.second)  # har daqiqa oxirida yangilanadi

    except Exception as e:
        await msg.answer(f"Xatolik: {e}")


async def main() -> None:
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())