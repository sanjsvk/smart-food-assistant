from typing import List
from pydantic import BaseModel, ValidationError

from app.tools.schemas import FoodItem


class ParsedFood(BaseModel):
    items: List[FoodItem]
    confidence: float


def validate_parsed_output(raw: dict) -> ParsedFood:
    try:
        return ParsedFood(**raw)
    except ValidationError as e:
        raise ValueError(f"Parsed output validation failed: {e}")