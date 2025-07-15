from sqlalchemy import Column, String, Integer, ForeignKey
from database.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    name = Column(String)
    category = Column(String)        # Contoh: "gym" atau "food"
    exp_cost = Column(Integer)
    quantity = Column(Integer, default=1)  # Bisa stack kalau dibeli banyak
