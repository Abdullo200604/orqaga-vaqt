from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio
import logging
from datetime import datetime, timedelta
import re
from aiogram.filters import Command
from aiogram import F

TOKEN = "7721595571:AAFXQr2-W7Z0x8E3AfpB3P8a2u6M9VqBtAs"  # o'zingizning tokenni qo'ying
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start komandasini ishlatish
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Assalomu Aleykum")

# Vaqtni qabul qiladigan handler (HH:MM:SS formatida)
@dp.message(F.text)
async def timer_handler(msg: Message):
    try:
        logging.info(f"Received message: {msg.text}")

        # Regex yordamida vaqtni olish
        match = re.match(r'@Pdptimebot\s*(\d{2}):(\d{2}):(\d{2})', msg.text)

        if not match:
            await msg.answer("Iltimos, vaqtni to'g'ri formatda kiriting (masalan, @Pdptimebot 00:50:30).")
            return

        # Soat, minut, va soniyani ajratib olish
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))

        # Hozirgi vaqtni olish
        now = datetime.now()
        target_datetime = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)

        # Agar vaqt o'tgan bo'lsa, ertangi kunni hisoblash
        if target_datetime < now:
            target_datetime += timedelta(days=1)

        # Foydalanuvchiga xabar yuborish
        message = await msg.answer("⏳ Tayyorlanmoqda...")

        # Vaqtni har soniyada yangilash
        while True:
            now = datetime.now()
            remaining = target_datetime - now

            if remaining.total_seconds() <= 0:
                await message.edit_text("⏰ Vaqt yetdi!")
                break

            # To'g'ri minut va soniya hisoblash
            minutes_left = remaining.seconds // 60
            seconds_left = remaining.seconds % 60

            # Foydalanuvchiga vaqtni yuborish (faqat bitta xabarni yangilaymiz)
            await message.edit_text(f"⏳ Qolgan vaqt: {minutes_left:02}:{seconds_left:02}")

            # Har soniyada yangilash
            await asyncio.sleep(1)  # Update every second

    except Exception as e:
        await msg.answer(f"Xatolik: {e}")

# Botni ishlashni boshlash
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
