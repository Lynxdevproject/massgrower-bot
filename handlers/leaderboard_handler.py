from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import desc
from database.db import SessionLocal
from models.user import User
from handlers.stats_handler import get_level  # kalau fungsi level dipisah

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = SessionLocal()
    top_users = session.query(User).order_by(desc(User.xp)).limit(5).all()
    session.close()

    if not top_users:
        await update.message.reply_text("📉 Belum ada yang punya EXP di GrowMass. Ayo mulai ngobrol!")
        return

    message = "*🏆 GrowMass Leaderboard: Top 5 EXP*\n\n"
    for i, user in enumerate(top_users, start=1):
        level = get_level(user.xp)
        username = f"@{user.username}" if user.username else "(Tanpa Username)"
        message += (
            f"{i}. {user_id_display(user)}\n"
            f"   EXP: {user.xp} | Level: {level}\n\n"
        )

    await update.message.reply_text(message, parse_mode="Markdown")

def user_id_display(user):
    return f"{user.username}" if user.username else f"ID: {user.user_id}"
