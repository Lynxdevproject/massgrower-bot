import time
from aiogram import types
import asyncpg
from bot_config import DB_URL

# Tracking message history sementara (in-memory)
message_tracker = {}  # format: {user_id: [timestamp1, timestamp2, ...]}

PUNISH_TIMEOUT = 600  # 10 menit dalam detik
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 60  # dalam detik

def register_anti_spam(dp, bot):

    # 🔗 Connect DB
    async def connect_db():
        return await asyncpg.connect(DB_URL)

    # 🚨 Handler semua pesan teks di grup
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def detect_spam(message: types.Message):
        # Hanya respon di grup dan bukan bot
        if message.chat.type not in ["group", "supergroup"] or message.from_user.is_bot:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        now = time.time()

        # Ambil data dari DB: apakah user sedang dihukum
        conn = await connect_db()
        user_data = await conn.fetchrow(
            "SELECT punished_until FROM users WHERE user_id = $1", user_id
        )

        if user_data and user_data["punished_until"] and user_data["punished_until"].timestamp() > now:
            await conn.close()
            return  # User sedang dihukum, XP handler nanti bisa skip

        # Track pesan user
        timestamps = message_tracker.get(user_id, [])
        timestamps = [ts for ts in timestamps if now - ts < SPAM_INTERVAL]  # hanya simpan yg <= 60 detik
        timestamps.append(now)
        message_tracker[user_id] = timestamps

        if len(timestamps) >= SPAM_THRESHOLD:
            punished_until = now + PUNISH_TIMEOUT
            await conn.execute(
                "UPDATE users SET punished_until = TO_TIMESTAMP($1) WHERE user_id = $2",
                punished_until, user_id
            )
            await conn.close()

            await message.reply(
                f"💢 Diam! {message.from_user.full_name}, Kamu Melanggar Peraturan 👮\n\n"
                "Semua Tindakan Kamu Akan Diabadikan ⚠️ EXP Tidak Akan Bertambah\n"
                "Kamu Dibebaskan Dalam 10 menit ⏳"
            )
        else:
            await conn.close()
