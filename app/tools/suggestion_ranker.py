def rank_candidates(candidates):
    return sorted(
        candidates,
        key=lambda x: x["protein"] / max(x["calories"], 1),
        reverse=True
    )