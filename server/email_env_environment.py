from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailAction, EmailObservation


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.emails = [
            {
                "text": "I was charged twice for my subscription. Please fix this immediately!",
                "route": "billing",
                "priority": "high",
                "tone": "angry",
                "user": "VIP"
            },
            {
                "text": "My app is crashing when I open it. Can you help?",
                "route": "tech",
                "priority": "medium",
                "tone": "normal",
                "user": "normal"
            },
            {
                "text": "Just wanted to know your working hours.",
                "route": "general",
                "priority": "low",
                "tone": "normal",
                "user": "normal"
            },
            {
                "text": "You won a lottery! Click this link now!",
                "route": "spam",
                "priority": "low",
                "tone": "normal",
                "user": "normal"
            },
            {
                "text": "I emailed last week and still no response. This is unacceptable for a premium user.",
                "route": "general",
                "priority": "high",
                "tone": "angry",
                "user": "VIP"
            }
        ]

        self.index = 0

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.index = 0

        email = self.emails[self.index]["text"]

        return EmailObservation(
            email=email,
            reward=0.0,
            done=False,
        )

    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        current_email = self.emails[self.index]

        correct_route = current_email["route"]
        correct_priority = current_email["priority"]
        tone = current_email["tone"]
        user = current_email["user"]

        route = action.route
        priority = action.priority

        reward = 0.0

        # Reward logic
        if route == correct_route:
            reward += 0.4
        else:
            reward -= 0.2

        if priority == correct_priority:
            reward += 0.4

        if tone == "angry" and priority == "high":
            reward += 0.2

        if tone == "angry" and user == "VIP" and reward > 0:
            reward += 0.2

        reward = max(0.0, min(1.0, reward))

        self.index += 1
        done = self.index >= len(self.emails)

        next_email = "done" if done else self.emails[self.index]["text"]

        return EmailObservation(
            email=next_email,
            reward=reward,
            done=done,
        )

    @property
    def state(self) -> State:
        return self._state