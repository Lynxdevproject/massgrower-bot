from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database.db import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))  # siapa yang melakukan transaksi
    type = Column(String)           # contoh: "purchase", "gift", "duel_reward", "reset"
    details = Column(String)        # info spesifik transaksi ("Beli Dumbbell", "Kasih EXP ke Budi", dll)
    exp_change = Column(Integer)    # berapa EXP ditambah/dikurangin
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
