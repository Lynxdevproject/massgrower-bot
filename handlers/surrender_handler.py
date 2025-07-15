from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User

async def surrender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    session: Session = SessionLocal()

    db_user = session.get(User, str(user.id))

    if db_user:
        db_user.xp = 0
        db_user.muscle = 0
        db_user.wins = 0 if hasattr(db_user, "wins") else None
        db_user.losses = 0 if hasattr(db_user, "losses") else None
        session.commit()

        await update.message.reply_text(
            f"🏳️ *{user.first_name} telah meninggalkan pertempuran!*\n"
            "Semua statistik kamu telah direset.\n"
            "Saatnya menyepi dan mungkin meditasi... atau bikin comeback legendaris 👀",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "⚠️ Data kamu belum tercatat.\n"
            "Kalau belum berotot, gak bisa nyerah dong 😅"
        )

    session.close()
