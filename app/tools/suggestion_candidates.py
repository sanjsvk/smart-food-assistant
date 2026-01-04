from app.tools.nutrition_data import NUTRITION_TABLE

def get_candidate_foods():
    candidates = []
    for food, data in NUTRITION_TABLE.items():
        candidates.append({
            "name": food,
            "calories": data["calories"],
            "protein": data["protein"]
        })
    return candidates