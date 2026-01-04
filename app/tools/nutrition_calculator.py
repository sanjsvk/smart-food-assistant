from typing import List
from .schemas import FoodItem
from .nutrition_data import NUTRITION_TABLE


class UnknownFoodError(Exception):
    pass


def calculate_nutrition(items: List[FoodItem]) -> dict:
    total_calories = 0.0
    total_protein = 0.0

    breakdown = []

    for item in items:
        food_key = item.name.lower()

        if food_key not in NUTRITION_TABLE:
            raise UnknownFoodError(f"Unknown food: {item.name}")

        ref = NUTRITION_TABLE[food_key]

        # Normalize quantity multiplier
        multiplier = item.quantity

        calories = ref["calories"] * multiplier
        protein = ref["protein"] * multiplier

        total_calories += calories
        total_protein += protein

        breakdown.append({
            "food": item.name,
            "calories": calories,
            "protein": protein
        })

    return {
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "breakdown": breakdown
    }