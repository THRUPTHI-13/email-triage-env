def grade_medium(action, correct):
    route, priority = action

    score = 0.0

    if route == correct[0]:
        score += 0.5
    if priority == correct[1]:
        score += 0.5

    return score