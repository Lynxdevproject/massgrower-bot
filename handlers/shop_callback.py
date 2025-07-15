from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def shop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "shop_gym":
        keyboard = [
            [InlineKeyboardButton("🏋️ Dumbbell (30 EXP)", callback_data="buy_dumbbell")],
            [InlineKeyboardButton("💪 Bench Press (50 EXP)", callback_data="buy_bench")],
            [InlineKeyboardButton("🏃 Treadmill (40 EXP)", callback_data="buy_treadmill")]
        ]
        await query.edit_message_text(
            "*🧰 Alat Gym Tersedia:*\n\nPilih item untuk dibeli:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "shop_food":
        keyboard = [
            [InlineKeyboardButton("🍗 Ayam Panggang (25 EXP)", callback_data="buy_chicken")],
            [InlineKeyboardButton("🥚 Telur Rebus (15 EXP)", callback_data="buy_egg")],
            [InlineKeyboardButton("🥛 Susu Whey (40 EXP)", callback_data="buy_whey")]
        ]
        await query.edit_message_text(
            "*🍽️ Makanan Bulking:*\n\nPilih makanan bergizi untuk masa otot!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
