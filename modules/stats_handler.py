from aiogram import types
import asyncpg
from bot_config import DB_URL

def register_stats_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["stats"])
    async def show_stats(message: types.Message):
        user = message.from_user
        user_id = user.id

        conn = await connect_db()
        user_data = await conn.fetchrow(
            """
            SELECT xp, muscle_mass FROM users WHERE user_id = $1
            """, user_id
        )
        await conn.close()

        xp = user_data["xp"] if user_data and "xp" in user_data else 100
        muscle = user_data["muscle_mass"] if user_data and "muscle_mass" in user_data else 10

        username = user.username if user.username else "—"

        stats_text = (
            f"*📊 Statistik Gym Virtual Kamu:*\n\n"
            f"👤 Nama        : {user.full_name}\n"
            f"🔖 Username    : {username}\n"
            f"⚡ Jumlah EXP  : {xp}\n"
            f"💪 Massa Otot  : {muscle} kg\n\n"
            f"Ayo lanjut latihan biar makin kekar! 🏋️‍♂️"
        )
        await message.answer(stats_text, parse_mode="Markdown")
