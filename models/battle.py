from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database.db import Base
import datetime

class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    challenger_id = Column(String, ForeignKey("users.user_id"))
    challenged_id = Column(String, ForeignKey("users.user_id"))
    winner_id = Column(String, ForeignKey("users.user_id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    resolved = Column(Boolean, default=True)
    method = Column(String)  # contoh: "random", "muscle_check", "skill_boost"
