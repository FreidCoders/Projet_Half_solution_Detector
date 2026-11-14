def build_opportunities(evaluations):
    opportunities = []
    for item in evaluations:
        if item["capability"] < 60:
            reason = item["limitation"]
            opportunities.append({"task": item["task"], "reason": reason})
    return opportunities
