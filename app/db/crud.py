from sqlalchemy.orm import Session
from datetime import date, datetime

from .models import FoodLog, UserProfile


def create_food_log(
    db: Session,
    raw_text: str,
    parsed_items: dict,
    calories: float,
    protein: float,
):
    log = FoodLog(
        raw_text=raw_text,
        parsed_items=parsed_items,
        calories=calories,
        protein=protein,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_food_logs_for_day(db: Session, day: date):
    start = datetime.combine(day, datetime.min.time())
    end = datetime.combine(day, datetime.max.time())

    return (
        db.query(FoodLog)
        .filter(FoodLog.timestamp >= start)
        .filter(FoodLog.timestamp <= end)
        .all()
    )


def get_or_create_user_profile(db: Session):
    profile = db.query(UserProfile).first()
    if profile:
        return profile

    profile = UserProfile(
        calorie_goal=2000,
        protein_goal=150,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile