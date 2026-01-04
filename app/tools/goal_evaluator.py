def evaluate_goals(intake, goals):
    calorie_diff = goals.calorie_goal - intake["calories"]
    protein_diff = goals.protein_goal - intake["protein"]

    return {
        "calories": {
            "goal": goals.calorie_goal,
            "current": intake["calories"],
            "remaining": round(calorie_diff, 2),
            "status": "over" if calorie_diff < 0 else "under"
        },
        "protein": {
            "goal": goals.protein_goal,
            "current": intake["protein"],
            "remaining": round(protein_diff, 2),
            "status": "over" if protein_diff < 0 else "under"
        }
    }