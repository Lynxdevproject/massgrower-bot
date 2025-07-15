from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("➕ Tambahkan GrowMass ke Grup", url="https://t.me/GrowMassBot?startgroup=true")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    intro_message = (
        f"🏋️‍♂️ Halo {user.first_name}!\n\n"
        "Selamat datang di *GrowMass*, bot gym virtual berbasis obrolan grup!\n\n"
        "Cara kerjanya simpel:\n"
        "• Semakin aktif kamu ngobrol di grup, semakin banyak EXP yang kamu kumpulkan.\n"
        "• EXP bisa dikonversi jadi massa otot virtual 💪.\n"
        "• Kamu bisa adu kekuatan dengan member lain, lihat profil, dan naik peringkat!\n\n"
        "Ayo bikin grup kamu jadi arena gym digital! 😎"
    )

    await update.message.reply_text(intro_message, reply_markup=reply_markup, parse_mode="Markdown")
