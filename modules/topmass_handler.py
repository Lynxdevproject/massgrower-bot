from aiogram import types
import asyncpg
from datetime import date
from bot_config import DB_URL

def register_topmass_handler(dp):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["topmass"])
    async def topmass(message: types.Message):
        today = date.today()
        conn = await connect_db()

        rows = await conn.fetch(
            """
            SELECT full_name, muscle_mass 
            FROM users 
            WHERE last_checkin = $1 OR giveme_last = $1
            ORDER BY muscle_mass DESC
            LIMIT 10
            """,
            today
        )
        await conn.close()

        if not rows:
            await message.reply("📭 Belum ada yang latihan hari ini... Yuk mulai check-in atau latihan dulu biar muncul di ranking!")
            return

        leaderboard = "*🏆 Ranking Kekekaran Hari Ini:*\n\n"
        for i, row in enumerate(rows, start=1):
            leaderboard += f"{i}. {row['full_name']} – {row['muscle_mass']} kg\n"

        await message.answer(leaderboard, parse_mode="Markdown")
