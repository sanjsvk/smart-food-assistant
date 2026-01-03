from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from datetime import date
from contextlib import asynccontextmanager

from app.db.database import engine
from app.db.models import Base
from app.db.session import get_db
from app.db import crud

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

@app.get("/debug/today")
def debug_today(db: Session = Depends(get_db)):
    logs = crud.get_food_logs_for_day(db, date.today())
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