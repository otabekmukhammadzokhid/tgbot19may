import asyncio
import logging
import ssl
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ==========================================
# CONFIG
# ==========================================

BOT_TOKEN = "8634610059:AAFozczGKkjOtqsvp-UcfYnOvrexvV-Ykzw"

# Replace with your real group ID
GROUP_ID = -1003549328437

# Replace with your real admin ID
ADMIN_ID = 6121238447

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(level=logging.INFO)

# ==========================================
# BOT SETUP
# ==========================================

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ==========================================
# STATES
# ==========================================

class AnonymousMessage(StatesGroup):
    waiting_for_text = State()
    waiting_for_choice = State()

# ==========================================
# BUTTONS
# ==========================================

choice_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send to a group"),
            KeyboardButton(text="Send to an admin"),
        ]
    ],
    resize_keyboard=True
)

# ==========================================
# START COMMAND
# ==========================================

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):

    await state.set_state(AnonymousMessage.waiting_for_text)

    await message.answer(
        "Hello, write a message to admin or a group.\n"
        "Everything is anonymous, no one will know that it's you.\n"
    )

    await message.answer(
        "Send text message about complaint, feedback or anything else"
    )

# ==========================================
# TEXT MESSAGE HANDLER
# ==========================================

@dp.message(AnonymousMessage.waiting_for_text)
async def get_text_message(message: Message, state: FSMContext):

    # Allow ONLY text messages
    if not message.text:
        await message.answer("Please send only text message")
        return

    # Ignore commands
    if message.text.startswith("/"):
        return

    # Save message
    await state.update_data(
        anonymous_text=message.text
    )

    # Ask where to send
    await message.answer(
        "Please choose where to send your anonymous message otherwise the message will not be sent.",
        reply_markup=choice_keyboard
    )

    await state.set_state(AnonymousMessage.waiting_for_choice)

# ==========================================
# SEND TO GROUP
# ==========================================

@dp.message(
    AnonymousMessage.waiting_for_choice,
    F.text == "Send to a group"
)
async def send_to_group(message: Message, state: FSMContext):

    data = await state.get_data()

    try:
        # Send anonymously to group
        await bot.send_message(
            chat_id=GROUP_ID,
            text=data["anonymous_text"]
        )

        # Remove buttons
        await message.answer(
            "Your message is sent anonymously",
            reply_markup=ReplyKeyboardRemove()
        )

    except Exception as e:
        logging.error(e)

        await message.answer(
            "Failed to send message",
            reply_markup=ReplyKeyboardRemove()
        )

    await message.answer("Send text message")

    # Return to text waiting state
    await state.set_state(AnonymousMessage.waiting_for_text)

# ==========================================
# SEND TO ADMIN
# ==========================================

@dp.message(
    AnonymousMessage.waiting_for_choice,
    F.text == "Send to an admin"
)
async def send_to_admin(message: Message, state: FSMContext):

    data = await state.get_data()

    try:
        # Send anonymously to admin
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=data["anonymous_text"]
        )

        # Remove buttons
        await message.answer(
            "Your message is sent anonymously",
            reply_markup=ReplyKeyboardRemove()
        )

    except Exception as e:
        logging.error(e)

        await message.answer(
            "Failed to send message",
            reply_markup=ReplyKeyboardRemove()
        )

    await message.answer("Send text message")

    # Return to text waiting state
    await state.set_state(AnonymousMessage.waiting_for_text)

# ==========================================
# WRONG BUTTON INPUT
# ==========================================

@dp.message(AnonymousMessage.waiting_for_choice)
async def wrong_button(message: Message):

    await message.answer("Please only press the buttons")

# ==========================================
# MAIN
# ==========================================

async def main():

    # Remove webhook
    await bot.delete_webhook(drop_pending_updates=True)

    print("Bot is running ...")

    # Start bot
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )

# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    asyncio.run(main())