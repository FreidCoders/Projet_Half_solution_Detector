from core.scoring import calculate_score

def test_weighted_score():
    items = [
        {"weight": 1, "capability": 100},
        {"weight": 3, "capability": 0},
    ]
    result = calculate_score(items)
    assert result["ai_coverage"] == 25.0
    assert result["gap"] == 75.0
