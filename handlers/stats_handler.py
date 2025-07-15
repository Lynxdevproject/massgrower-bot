from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User

def get_level(xp: int) -> str:
    if xp < 50:
        return "1. Pemula 🐣"
    elif xp < 150:
        return "2. Bulking 🥩"
    elif xp < 300:
        return "3. Mulai Berotot 💪"
    elif xp < 500:
        return "4. Berkembang 🏋️"
    else:
        return "5. Kekar 🦍"

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    session: Session = SessionLocal()

    db_user = session.get(User, str(user.id))

    if db_user:
        level = get_level(db_user.xp)
        message = (
            f"📋 *Statistik GrowMass*\n\n"
            f"👤 Nama: {user.full_name}\n"
            f"🔹 Username: @{user.username or 'N/A'}\n"
            f"🆔 User ID: {user.id}\n"
            f"⚡ EXP: {db_user.xp}\n"
            f"🏆 Level: {level}"
        )
    else:
        message = (
            f"⚠️ Data kamu belum tercatat di database.\n"
            "Ayo aktif dulu di grup biar dapet EXP dan mulai berotot! 💪"
        )

    session.close()
    await update.message.reply_text(message, parse_mode="Markdown")
