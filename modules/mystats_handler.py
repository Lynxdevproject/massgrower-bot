from aiogram import types
import asyncpg
from bot_config import DB_URL

def register_mystats_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    def get_level(muscle_mass: int) -> str:
        if muscle_mass >= 200:
            return "🏆 Macho"
        elif muscle_mass >= 100:
            return "💪 Lumayan Kekar"
        elif muscle_mass >= 50:
            return "🏋️ Berproses"
        else:
            return "🐣 Kroco"

    @dp.message_handler(commands=["mystats"])
    async def mystats(message: types.Message):
        user = message.from_user
        user_id = user.id

        conn = await connect_db()
        user_data = await conn.fetchrow(
            "SELECT xp, muscle_mass FROM users WHERE user_id = $1", user_id
        )
        await conn.close()

        xp = user_data["xp"] if user_data and "xp" in user_data else 100
        muscle = user_data["muscle_mass"] if user_data and "muscle_mass" in user_data else 10
        level = get_level(muscle)

        username = user.username if user.username else "—"

        mystats_text = (
            f"*📊 Gym Status Kamu:*\n\n"
            f"👤 Nama        : {user.full_name}\n"
            f"🔖 Username    : {username}\n"
            f"⚡ Jumlah EXP  : {xp}\n"
            f"💪 Massa Otot  : {muscle} kg\n"
            f"🥇 Level       : {level}\n\n"
            f"Keep grinding, kekuatanmu belum maksimum 🚀"
        )
        await message.answer(mystats_text, parse_mode="Markdown")
