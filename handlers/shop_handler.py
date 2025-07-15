from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🏋️ Alat Gym", callback_data="shop_gym"),
            InlineKeyboardButton("🍗 Makanan Bulking", callback_data="shop_food")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "*🏪 GrowMass Shop*\n\n"
        "Tukar EXP kamu dengan perlengkapan gym atau makanan berprotein!\n"
        "Pilih kategori di bawah untuk melihat item yang tersedia 💪",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
