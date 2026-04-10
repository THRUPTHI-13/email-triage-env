def grade_easy(action, correct):
    route, priority = action

    if route == correct[0]:
        return 1.0
    return 0.0