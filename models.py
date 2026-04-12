from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class EmailAction(Action):
    route: str
    priority: str


class EmailObservation(Observation):
    email: str = Field(default="")
    task: str = Field(default="")   # ✅ ADD THIS