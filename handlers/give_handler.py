import time
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User

DAILY_GIFT_LIMIT = 3
EXP_GIFT_AMOUNT = 10
DAY_SECONDS = 86400  # 1 hari

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    giver = update.effective_user
    reply = update.message.reply_to_message

    if not reply:
        await update.message.reply_text(
            "🎁 Kamu ingin memberi EXP ke siapa?\n"
            "Gunakan /give dengan reply ke pesan member yang mau kamu berikan hadiah EXP."
        )
        return

    receiver = reply.from_user

    if receiver.id == giver.id:
        await update.message.reply_text("😅 Kamu tidak bisa memberi EXP ke diri sendiri.")
        return

    # Setup user_data tracking
    user_data = context.user_data
    now = time.time()
    gift_data = user_data.get("gift_history", [])

    # Filter gift record dalam 24 jam terakhir
    recent_gifts = [ts for ts in gift_data if now - ts < DAY_SECONDS]

    if len(recent_gifts) >= DAILY_GIFT_LIMIT:
        await update.message.reply_text("🚫 Kamu sudah memberikan 3 hadiah EXP hari ini. Tunggu besok!")
        return

    # Tambah ke history dan update user_data
    recent_gifts.append(now)
    user_data["gift_history"] = recent_gifts

    # Tambahkan EXP ke receiver
    session: Session = SessionLocal()
    db_receiver = session.get(User, str(receiver.id))

    if not db_receiver:
        db_receiver = User(user_id=str(receiver.id), username=receiver.username, xp=EXP_GIFT_AMOUNT)
        session.add(db_receiver)
    else:
        db_receiver.xp += EXP_GIFT_AMOUNT

    session.commit()
    session.close()

    await update.message.reply_text(
        f"🎁 {giver.first_name} memberi *{EXP_GIFT_AMOUNT} EXP* kepada {receiver.first_name}!\n"
        "GrowMass makin solid dengan vibes saling dukung 💪",
        parse_mode="Markdown"
    )
