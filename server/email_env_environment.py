from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import EmailAction, EmailObservation
except ImportError:
    from models import EmailAction, EmailObservation


class EmailEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        
        self.tasks = {
            "easy": [
                ("billing", "high", "normal", "normal"),
                ("tech", "medium", "normal", "normal"),
            ],
            "medium": [
                ("billing", "high", "angry", "VIP"),
                ("tech", "medium", "normal", "normal"),
                ("general", "low", "normal", "normal"),
            ],
            "hard": [
                ("billing", "high", "angry", "VIP"),
                ("spam", "low", "normal", "normal"),
                ("tech", "medium", "normal", "normal"),
                ("general", "low", "normal", "normal"),
            ],
        }

        self.current_task = "easy"
        self.emails = self.tasks[self.current_task]
        self.index = 0

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        
        if self.current_task == "easy":
            self.current_task = "medium"
        elif self.current_task == "medium":
            self.current_task = "hard"
        else:
            self.current_task = "easy"

        self.emails = self.tasks[self.current_task]
        self.index = 0

        return EmailObservation(
    email=str(self.emails[self.index]),
    task=self.current_task,   
    reward=0.1,
    done=False,
)

    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        current_email = self.emails[self.index]

        correct_route = current_email[0]
        correct_priority = current_email[1]

        route = action.route
        priority = action.priority

        
        if route == correct_route and priority == correct_priority:
            reward = 0.9
        elif route == correct_route:
            reward = 0.6
        else:
            reward = 0.2

        
        if priority != correct_priority:
            reward -= 0.1

        
        if current_email[2] == "angry" and current_email[3] == "VIP":
            reward += 0.1

        
        reward = max(0.1, min(0.9, reward))

       
        self.index += 1
        done = self.index >= len(self.emails)

        next_email = "done" if done else str(self.emails[self.index])

        return EmailObservation(
    email=next_email,
    task=self.current_task,   
    reward=reward,
    done=done,
)

    @property
    def state(self) -> State:
        return self._state