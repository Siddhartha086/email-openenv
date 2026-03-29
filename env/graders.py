def grade_easy(state, sample):
    return 1.0 if state["classification"] == sample["classification"] else 0.0


def grade_medium(state, sample):
    score = 0.0
    if state["classification"] == sample["classification"]:
        score += 0.5
    if state["route"] == sample["route"]:
        score += 0.5
    return score


def grade_hard(state, sample):
    score = 0.0
    if state["classification"] == sample["classification"]:
        score += 0.25
    if state["route"] == sample["route"]:
        score += 0.25
    if state["reply"]:
        score += 0.25
    if state["stage"] == "replied":
        score += 0.25
    return score