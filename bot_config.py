import os
from dotenv import load_dotenv

# ⏬ Load .env file
load_dotenv()

# 🔑 Ambil variabel dari environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DATABASE_URL")  # Format: postgres://user:pass@host:port/dbname
