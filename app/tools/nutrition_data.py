import json
from pathlib import Path

NUTRITION_TABLE_PATH = Path("data/food_knowledge/nutrition_table.json")

def load_nutrition_table() -> dict:
    with open(NUTRITION_TABLE_PATH, "r") as f:
        return json.load(f)

NUTRITION_TABLE = load_nutrition_table()