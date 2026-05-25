import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

# ==========================================
# CONFIG
# ==========================================

BOT_TOKEN = "8634610059:AAFozczGKkjOtqsvp-UcfYnOvrexvV-Ykzw"

# Your group ID
GROUP_ID = -1003549328437

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(level=logging.INFO)

# ==========================================
# BOT SETUP
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# START COMMAND
# ==========================================

@dp.message(CommandStart())
async def start_command(message: Message):

    await message.answer(
        "Welcome! Feel free to share your feedback, complaints, or suggestions anonymously. Your identity will remain private, and your message will be forwarded securely."
        , reply_markup=ReplyKeyboardRemove()
    )

# ==========================================
# MESSAGE HANDLER
# ==========================================

@dp.message()
async def anonymous_forward(message: Message):

    # Ignore commands
    if message.text and message.text.startswith("/"):
        return

    try:
        # Forward message anonymously to group
        await bot.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

        # Reply to user
        await message.reply("Thank you for your feedback. Our team will review your comments carefully and work on the improvments accordingly.")

        #await message.answer(
        #    "Feel free to share your feedback, complaints, or suggestions anonymously. Your identity will remain private, and your message will be forwarded securely."

        #)

    except Exception as e:
        logging.error(e)

        await message.answer("Failed to send message")

# ==========================================
# MAIN
# ==========================================

async def main():

    # Remove webhook
    await bot.delete_webhook(drop_pending_updates=True)

    print("Bot is running ...")

    # Start polling
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )

# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    asyncio.run(main())