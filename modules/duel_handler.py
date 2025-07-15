from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncpg
import random
from bot_config import DB_URL

def register_duel_handler(dp, bot):

    async def connect_db():
        return await asyncpg.connect(DB_URL)

    @dp.message_handler(commands=["duel"])
    async def initiate_duel(message: types.Message):
        if not message.reply_to_message:
            await message.reply("⚔️ Kamu harus reply pesan seseorang untuk menantangnya duel!")
            return

        challenger = message.from_user
        opponent = message.reply_to_message.from_user

        if opponent.is_bot:
            await message.reply("🤖 Lawan kamu terlalu jago... dia bot.")
            return

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("✅ Terima Duel", callback_data=f"duel_accept:{challenger.id}"),
            InlineKeyboardButton("❌ Tolak Duel", callback_data=f"duel_decline:{challenger.id}")
        )

        await message.reply(
            f"🥊 {challenger.full_name} menantang {opponent.full_name} untuk duel otot!\n\n"
            "⚠️ Terima atau tolak tantangan di bawah ini!",
            reply_markup=keyboard
        )

    @dp.callback_query_handler(lambda c: c.data.startswith("duel_accept:"))
    async def handle_duel_accept(callback_query: types.CallbackQuery):
        attacker_id = int(callback_query.data.split(":")[1])
        defender = callback_query.from_user

        conn = await connect_db()
        attacker_data = await conn.fetchrow("SELECT xp, muscle_mass FROM users WHERE user_id = $1", attacker_id)
        defender_data = await conn.fetchrow("SELECT xp, muscle_mass FROM users WHERE user_id = $1", defender.id)

        attacker_muscle = attacker_data["muscle_mass"] if attacker_data else 10
        defender_muscle = defender_data["muscle_mass"] if defender_data else 10

        total = attacker_muscle + defender_muscle
        win_chance_attacker = attacker_muscle / total
        winner = attacker_id if random.random() < win_chance_attacker else defender.id
        loser = defender.id if winner == attacker_id else attacker_id

        xp_reward = 25
        await conn.execute("UPDATE users SET xp = xp + $1 WHERE user_id = $2", xp_reward, winner)
        await conn.execute("UPDATE users SET xp = xp - $1 WHERE user_id = $2", xp_reward, loser)
        await conn.close()

        winner_name = callback_query.from_user.full_name if winner == defender.id else "Penantang"
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            f"🏁 Duel selesai!\n🎖️ Pemenang: *{winner_name}*\n"
            f"⚡ XP +{xp_reward} diberikan\n"
            f"💀 Lawan kehilangan XP...\n\n"
            f"Hati-hati ngajak duel sembarangan 😎",
            parse_mode="Markdown"
        )

    @dp.callback_query_handler(lambda c: c.data.startswith("duel_decline:"))
    async def handle_duel_decline(callback_query: types.CallbackQuery):
        challenger_id = int(callback_query.data.split(":")[1])
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.message.chat.id,
            "❌ Duel ditolak! Kamu bisa kabur, tapi tidak bisa sembunyikan ketakutan 💨"
        )
