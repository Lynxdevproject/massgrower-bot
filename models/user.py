from sqlalchemy import Column, String, Integer
from database.db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String)
    xp = Column(Integer, default=0)         # Pengalaman user
    muscle = Column(Integer, default=0)     # Massa otot (bisa didapat dari /gain)
    wins = Column(Integer, default=0)       # Jumlah kemenangan duel
    losses = Column(Integer, default=0)     # Jumlah kekalahan duel
