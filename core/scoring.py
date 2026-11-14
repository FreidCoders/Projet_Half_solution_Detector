def calculate_score(evaluations):
    total_weight = sum(max(1, item["weight"]) for item in evaluations)
    if not total_weight:
        return {"ai_coverage": 0.0, "gap": 100.0}
    weighted = sum(item["weight"] * item["capability"] for item in evaluations)
    coverage = weighted / total_weight
    return {"ai_coverage": round(coverage, 1), "gap": round(100 - coverage, 1)}
