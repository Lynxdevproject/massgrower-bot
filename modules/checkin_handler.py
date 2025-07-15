from aiogram import types
import asyncpg
from datetime import date
from bot_config import DB_URL

DAILY_REWARD = 3

def register_checkin_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["checkin"])
    async def checkin(message: types.Message):
        user = message.from_user
        user_id = user.id
        today = date.today()

        conn = await connect_db()
        user_data = await conn.fetchrow(
            "SELECT xp, last_checkin FROM users WHERE user_id = $1", user_id
        )

        if not user_data:
            await conn.execute(
                """
                INSERT INTO users (user_id, full_name, xp, last_checkin)
                VALUES ($1, $2, $3, $4)
                """,
                user_id, user.full_name, DAILY_REWARD, today
            )
            await conn.close()
            await message.reply(f"📆 Check-in berhasil! Kamu dapet {DAILY_REWARD} EXP hari ini 💪")
            return

        last_checkin = user_data["last_checkin"]
        xp = user_data["xp"]

        if last_checkin == today:
            await conn.close()
            await message.reply("⏱️ Kamu udah check-in hari ini. Balik lagi besok, otot gak bisa disuruh lembur 😴")
            return

        xp += DAILY_REWARD
        await conn.execute(
            "UPDATE users SET xp = $1, last_checkin = $2 WHERE user_id = $3",
            xp, today, user_id
        )
        await conn.close()
        await message.reply(f"📆 Check-in sukses! Kamu dapet +{DAILY_REWARD} EXP hari ini 🏋️‍♂️")
