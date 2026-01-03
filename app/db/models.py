from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from datetime import datetime

from .database import Base


class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    raw_text = Column(String, nullable=False)
    parsed_items = Column(JSON, nullable=True)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)

    calorie_goal = Column(Float, nullable=False)
    protein_goal = Column(Float, nullable=False)