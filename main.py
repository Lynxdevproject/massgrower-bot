import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Load env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Init DB
from database.db import init_db
init_db(DATABASE_URL)

# Import handlers dari package modular
from handlers import (
    start,
    xp_tracker,
    stats,
    leaderboard,
    challenge,
    challenge_callback,
    give,
    shop,
    shop_callback,
    surrender
)

# Setup Bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command Handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(CommandHandler("give", give))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("surrender", surrender))

    # CallbackQuery Handler
    app.add_handler(CallbackQueryHandler(challenge_callback, pattern="^challenge_"))
    app.add_handler(CallbackQueryHandler(shop_callback, pattern="^shop_|^buy_"))

    # XP Tracker via Message Handler (auto kasih EXP)
    app.add_handler(CommandHandler("xp", xp_tracker))  # bisa diubah jadi MessageHandler kalau mau auto

    print("GrowMass is now running... 🦍")
    app.run_polling()

if __name__ == "__main__":
    main()
