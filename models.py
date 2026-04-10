from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class EmailAction(Action):
    route: str = Field(..., description="Route of email")
    priority: str = Field(..., description="Priority of email")


class EmailObservation(Observation):
    email: str = Field(default="")