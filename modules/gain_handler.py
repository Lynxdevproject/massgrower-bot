from aiogram import types
import asyncpg
from bot_config import DB_URL

def register_gain_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["gain"])
    async def gain_muscle(message: types.Message):
        user = message.from_user
        user_id = user.id

        conn = await connect_db()
        user_data = await conn.fetchrow("SELECT xp, muscle_mass FROM users WHERE user_id = $1", user_id)

        xp = user_data["xp"] if user_data else 100
        muscle = user_data["muscle_mass"] if user_data else 10

        if xp < 10:
            await conn.close()
            await message.reply("⚠️ Kamu butuh minimal 10 EXP buat latihan. Pergi ngobrol dulu, jangan cuma ngintip barbel 😤")
            return

        gain_amount = xp // 10
        remaining_xp = xp % 10
        new_muscle = muscle + gain_amount

        await conn.execute(
            "UPDATE users SET xp = $1, muscle_mass = $2 WHERE user_id = $3",
            remaining_xp, new_muscle, user_id
        )
        await conn.close()

        await message.answer(
            f"🏋️‍♂️ Latihan selesai, {user.full_name}!\n"
            f"💪 Kamu berhasil menambah {gain_amount} kg otot!\n"
            f"⚡ Sisa EXP kamu: {remaining_xp}\n"
            f"Total massa otot: {new_muscle} kg\n\n"
            f"Nafas dulu… lalu balik lagi angkat virtual barbel 🧘"
        )
