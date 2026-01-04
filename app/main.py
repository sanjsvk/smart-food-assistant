from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pydantic import BaseModel

from app.db.database import engine
from app.db.models import Base
from app.db.session import get_db
from app.db import crud
from app.tools.schemas import FoodItem
from app.tools.nutrition_calculator import calculate_nutrition
from app.llm.client import parse_food_input
from app.llm.validators import validate_parsed_output

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (nothing needed yet)

app = FastAPI(
    title="Smart Food Assistant",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/workflows/test")
async def workflow_test(request: Request):
    payload = await request.json()
    return {"received": payload}

@app.get("/debug/today", tags=["debug"])
def debug_today(db: Session = Depends(get_db)):
    today_utc = datetime.now(timezone.utc).date()
    logs = crud.get_food_logs_for_day(db, today_utc)
    return {
        "count": len(logs),
        "logs": [
            {
                "raw_text": l.raw_text,
                "calories": l.calories,
                "protein": l.protein,
            }
            for l in logs
        ],
    }

@app.post("/debug/calculate", tags=["debug"])
def debug_calculate(items: list[FoodItem]):
    return calculate_nutrition(items)

class FoodLogRequest(BaseModel):
    raw_text: str

@app.post("/log_food")
def log_food(
    payload: FoodLogRequest,
    db: Session = Depends(get_db)
):
    raw_text = payload.raw_text
    parsed_raw = parse_food_input(raw_text)
    parsed = validate_parsed_output(parsed_raw)

    nutrition = calculate_nutrition(parsed.items)

    crud.create_food_log(
        db=db,
        raw_text=raw_text,
        parsed_items=parsed_raw,
        calories=nutrition["total_calories"],
        protein=nutrition["total_protein"],
    )

    return {
        "parsed": parsed_raw,
        "nutrition": nutrition
    }