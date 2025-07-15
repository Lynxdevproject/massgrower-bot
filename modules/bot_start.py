from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncpg
from bot_config import BOT_TOKEN, DB_URL

def register_bot_start(dp, bot):

    # 🔗 Koneksi PostgreSQL
    async def connect_db():
        return await asyncpg.connect(DB_URL)

    # 🟢 /start command
    @dp.message_handler(commands=["start"])
    async def start_cmd(message: types.Message):
        user = message.from_user
        user_name = user.full_name
        user_id = user.id

        text = (
            f"Halo {user_name}! 🏋️‍♂️\n\n"
            "Aku adalah *Bot Minigame Pembesar Otot*, terinspirasi dari Mini Game Discord!\n"
            "Bot ini hanya berfungsi di grup. Tambahkan aku ke grupmu dan mulai latihan virtual 💪\n\n"
            "Tekan tombol di bawah ini untuk menambahkan aku ke grup atau lihat source code-nya:"
        )

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("🎈 Add me to your group", url="https://t.me/MassGrowerBot?startgroup=true"),
            InlineKeyboardButton("☕ Source code", url="https://github.com/Lynxdevproject/massgrower-bot")
        )

        await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

        # 🗂️ Simpan user ke database
        conn = await connect_db()
        await conn.execute(
            """
            INSERT INTO users (user_id, full_name)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
            """,
            user_id, user_name
        )
        await conn.close()

    # 🎉 Sambutan saat bot masuk grup
    @dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
    async def welcome_group(message: types.Message):
        for new_member in message.new_chat_members:
            if new_member.id == bot.id:
                welcome_text = (
                    "Hi kalian semua, siap berolahraga virtual? 🏋️‍♀️🔥\n\n"
                    "Tekan tombol bantuan di bawah untuk melihat potensi kekuatan ku (fitur segera menyusul)"
                )
                help_keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton("⚙️ Bantuan", callback_data="show_help")
                )
                await message.answer(welcome_text, reply_markup=help_keyboard)

    # ⚙️ Tombol bantuan (sementara)
    @dp.callback_query_handler(lambda c: c.data == "show_help")
    async def help_callback(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            "⚙️ Bantuan akan hadir di versi berikutnya ya 💪"
                )
