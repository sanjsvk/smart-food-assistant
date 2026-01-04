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
from app.rag.vector_store import VectorStore
from app.tools.aggregation import aggregate_daily_intake
from app.tools.goal_evaluator import evaluate_goals
from app.tools.suggestion_candidates import get_candidate_foods
from app.tools.suggestion_filter import filter_by_budget
from app.tools.suggestion_ranker import rank_candidates
from app.llm.suggestion_explainer import explain_suggestions

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
vector_store = VectorStore()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/workflows/test")
async def workflow_test(request: Request):
    payload = await request.json()
    return {"received": payload}

# --------------------------------------------------
# Debug / Development Endpoints
# Not intended for production UI
# --------------------------------------------------
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

# --------------------------------------------------
# Debug / Development Endpoints
# Not intended for production UI
# --------------------------------------------------
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
    retrieved_context = vector_store.query(raw_text)
    parsed_raw = parse_food_input(
        user_input=raw_text,
        context=retrieved_context
    )
    parsed = validate_parsed_output(parsed_raw)

    nutrition = calculate_nutrition(parsed.items)

    log = crud.create_food_log(
        db=db,
        raw_text=raw_text,
        parsed_items=parsed_raw,
        calories=nutrition["total_calories"],
        protein=nutrition["total_protein"],
    )

    vector_store.add_document(
        doc_id=str(log.id),
        text=raw_text,
        metadata={
            "calories": nutrition["total_calories"],
            "protein": nutrition["total_protein"]
        }
    )

    return {
        "parsed": parsed_raw,
        "nutrition": nutrition
    }

@app.get("/debug/retrieve", tags=["debug"])
def debug_retrieve(query: str):
    return vector_store.query(query)

@app.get("/summary/today")
def today_summary(db: Session = Depends(get_db)):
    today_utc = datetime.now(timezone.utc).date()

    # Fetch today's food logs
    logs = crud.get_food_logs_for_day(db, today_utc)

    # Aggregate calories & protein
    intake = aggregate_daily_intake(logs)

    # Load user goals
    profile = crud.get_or_create_user_profile(db)

    # Compare intake vs goals
    evaluation = evaluate_goals(intake, profile)

    return {
        "intake": intake,
        "goals": evaluation
    }

@app.get("/suggest/next")
def suggest_next_meal(db: Session = Depends(get_db)):
    today_utc = datetime.now(timezone.utc).date()

    logs = crud.get_food_logs_for_day(db, today_utc)
    intake = aggregate_daily_intake(logs)

    profile = crud.get_or_create_user_profile(db)
    evaluation = evaluate_goals(intake, profile)

    remaining_cal = evaluation["calories"]["remaining"]
    remaining_protein = evaluation["protein"]["remaining"]

    candidates = get_candidate_foods()
    filtered = filter_by_budget(
        candidates,
        remaining_cal,
        remaining_protein
    )

    ranked = rank_candidates(filtered)

    explanation = explain_suggestions(
        remaining={
            "calories": remaining_cal,
            "protein": remaining_protein
        },
        suggestions=ranked[:5]
    )

    return {
        "remaining": {
            "calories": remaining_cal,
            "protein": remaining_protein
        },
        "suggestions": ranked[:5],
        "explanation": explanation
    }