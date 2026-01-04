def aggregate_daily_intake(logs):
    total_calories = sum(l.calories for l in logs)
    total_protein = sum(l.protein for l in logs)

    return {
        "calories": round(total_calories, 2),
        "protein": round(total_protein, 2)
    }