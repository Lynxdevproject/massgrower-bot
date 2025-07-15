from aiogram import Bot, Dispatcher, executor
import logging
from bot_config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Register all modules
from modules.bot_start import register_bot_start
from modules.anti_spam_handler import register_anti_spam
from modules.stats_handler import register_stats_handler
from modules.gain_handler import register_gain_handler
from modules.duel_handler import register_duel_handler
from modules.mystats_handler import register_mystats_handler
from modules.giveme_handler import register_giveme_handler
from modules.checkin_handler import register_checkin_handler
from modules.topmass_handler import register_topmass_handler
from modules.surrender_handler import register_surrender_handler

register_bot_start(dp, bot)
register_anti_spam(dp, bot)
register_stats_handler(dp)
register_gain_handler(dp)
register_duel_handler(dp, bot)
register_mystats_handler(dp)
register_giveme_handler(dp)
register_checkin_handler(dp)
register_topmass_handler(dp)
register_surrender_handler(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
