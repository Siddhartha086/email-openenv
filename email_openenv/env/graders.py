def grade_response(response: str, expected_keywords: list):
    score = 0
    response = response.lower()

    for word in expected_keywords:
        if word in response:
            score += 1

    return score / len(expected_keywords)