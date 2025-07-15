from aiogram import types
import asyncpg
from datetime import date
from bot_config import DB_URL

DAILY_LIMIT = 5
REWARD_XP = 5

def register_giveme_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["giveme"])
    async def giveme_command(message: types.Message):
        user = message.from_user
        user_id = user.id

        conn = await connect_db()
        user_data = await conn.fetchrow(
            "SELECT xp, giveme_count, giveme_last FROM users WHERE user_id = $1", user_id
        )

        today = date.today()

        if not user_data:
            await conn.execute(
                """
                INSERT INTO users (user_id, full_name, xp, giveme_count, giveme_last)
                VALUES ($1, $2, $3, $4, $5)
                """,
                user_id, user.full_name, REWARD_XP, 1, today
            )
            await conn.close()
            await message.reply(f"🫶 Kamu menerima {REWARD_XP} EXP! (1/5 hari ini)")
            return

        last_date = user_data["giveme_last"]
        count_today = user_data["giveme_count"]
        xp = user_data["xp"]

        if last_date != today:
            # Reset counter
            count_today = 0

        if count_today >= DAILY_LIMIT:
            await conn.close()
            await message.reply("⛔ Batas minta EXP hari ini sudah habis! Balik lagi besok 💤")
            return

        count_today += 1
        xp += REWARD_XP

        await conn.execute(
            """
            UPDATE users 
            SET xp = $1, giveme_count = $2, giveme_last = $3 
            WHERE user_id = $4
            """,
            xp, count_today, today, user_id
        )

        await conn.close()
        await message.reply(
            f"✨ Kamu menerima {REWARD_XP} EXP! ({count_today}/5 hari ini)\n"
            f"Semoga hari kamu penuh semangat latihan 💪"
        )
