def filter_by_budget(candidates, remaining_calories, remaining_protein):
    valid = []
    for c in candidates:
        if (
            c["calories"] <= remaining_calories
            and c["protein"] <= remaining_protein
        ):
            valid.append(c)
    return valid