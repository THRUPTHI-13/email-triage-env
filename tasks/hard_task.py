def grade_hard(action, correct):
    route, priority = action

    score = 0.0

    if route == correct[0]:
        score += 0.4
    if priority == correct[1]:
        score += 0.4

    # Bonus for VIP + angry handling
    if correct[2] == "angry" and correct[3] == "VIP":
        if route == correct[0] and priority == correct[1]:
            score += 0.2

    return min(score, 1.0)