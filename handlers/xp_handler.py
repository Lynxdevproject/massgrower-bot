import time
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User

SPAM_THRESHOLD = 5
COOLDOWN_SECONDS = 600  # 10 menit
XP_PER_MESSAGE = 5
XP_PENALTY = -5         # EXP dikurangi saat spam

async def xp_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type != "group":
        return

    user = update.effective_user
    user_data = context.user_data
    now = time.time()

    # Check cooldown aktif
    if user_data.get("cooldown_until", 0) > now:
        return  # EXP tidak dihitung

    # Track 5 pesan terakhir (timestamp)
    messages = user_data.get("recent_messages", [])
    messages.append(now)
    user_data["recent_messages"] = messages[-SPAM_THRESHOLD:]  # simpan max 5

    # Deteksi spam: 5 pesan dalam <10 detik
    if len(messages) == SPAM_THRESHOLD and messages[-1] - messages[0] < 10:
        user_data["cooldown_until"] = now + COOLDOWN_SECONDS

        # Minus EXP ke database
        session: Session = SessionLocal()
        db_user = session.get(User, str(user.id))
        if db_user:
            db_user.xp = max(db_user.xp + XP_PENALTY, 0)  # Jangan sampai negatif
            session.commit()
        session.close()

        await update.message.reply_text(
            "⛔️ *Stop! Kamu Melanggar Peraturan*\n"
            "EXP kamu dikurangi *5 poin* sebagai hukuman.\n"
            "Semua aksi setelah ini akan diabaikan hingga *10 menit ke depan*.",
            parse_mode="Markdown"
        )
        return

    # Kalau aman, tambahin EXP
    session = SessionLocal()
    db_user = session.get(User, str(user.id))
    if not db_user:
        db_user = User(user_id=str(user.id), username=user.username, xp=XP_PER_MESSAGE)
        session.add(db_user)
    else:
        db_user.xp += XP_PER_MESSAGE

    session.commit()
    session.close()
