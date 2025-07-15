import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User

EXP_REWARD = 15

# Command /challenge
async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    challenger = update.effective_user
    reply_target = update.message.reply_to_message

    if not reply_target:
        await update.message.reply_text(
            "🌀 Kamu ingin berduel dengan *bayangan* atau *angin*?\n"
            "Coba reply pesan member yang mau kamu tantang dulu!",
            parse_mode="Markdown"
        )
        return

    challenged = reply_target.from_user

    if challenged.id == challenger.id:
        await update.message.reply_text("🤨 Nge-challenge diri sendiri? Mending introspeksi dulu bro.")
        return

    context.chat_data["last_challenge"] = {
        "challenger_id": challenger.id,
        "challenger_name": challenger.first_name,
        "challenged_id": challenged.id,
        "challenged_name": challenged.first_name
    }

    keyboard = [
        [
            InlineKeyboardButton("✅ Terima Tantangan", callback_data="challenge_accept"),
            InlineKeyboardButton("🌀 Skip Kroco", callback_data="challenge_skip"),
            InlineKeyboardButton("❌ Tolak", callback_data="challenge_decline")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"⚔️ *{challenger.first_name}* menantang *{challenged.first_name}* untuk duel!\n"
        "Pilih tindakanmu:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Button handler
async def challenge_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = context.chat_data.get("last_challenge")
    if not data:
        await query.edit_message_text("⛔️ Tantangan sudah kedaluwarsa atau tidak ditemukan.")
        return

    if query.from_user.id != data["challenged_id"]:
        await query.answer("⚠️ Kamu bukan yang ditantang!", show_alert=True)
        return

    challenger_name = data["challenger_name"]
    challenged_name = data["challenged_name"]
    challenger_id = data["challenger_id"]
    challenged_id = data["challenged_id"]

    session: Session = SessionLocal()

    if query.data == "challenge_accept":
        winner_id = random.choice([challenger_id, challenged_id])
        winner_name = challenger_name if winner_id == challenger_id else challenged_name

        db_user = session.get(User, str(winner_id))
        if db_user:
            db_user.xp += EXP_REWARD
            session.commit()

        await query.edit_message_text(
            f"⚔️ Duel antara *{challenger_name}* vs *{challenged_name}* berlangsung sengit!\n\n"
            f"🏆 Pemenangnya adalah *{winner_name}*! Ia mendapatkan *{EXP_REWARD} EXP*!",
            parse_mode="Markdown"
        )

    elif query.data == "challenge_skip":
        await query.edit_message_text(
            f"💤 {challenged_name} berkata:\n"
            "*Ilmu kamu belum cukup untuk menantang sang penantang!*",
            parse_mode="Markdown"
        )

    elif query.data == "challenge_decline":
        await query.edit_message_text(
            f"❌ {challenged_name} menolak duel.\n"
            "GrowMass tetap damai... untuk sekarang 😅",
            parse_mode="Markdown"
        )

    session.close()
    context.chat_data["last_challenge"] = None
