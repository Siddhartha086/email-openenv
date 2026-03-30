from pydantic import BaseModel

class Observation(BaseModel):
    email: str
    task: str

class Action(BaseModel):
    response: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict