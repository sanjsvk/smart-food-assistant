def normalize_food_name(name: str) -> str:
    name = name.lower().strip()

    # Simple plural normalization (MVP-safe)
    if name.endswith("s"):
        name = name[:-1]

    return name