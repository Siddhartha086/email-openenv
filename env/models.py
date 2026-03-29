from pydantic import BaseModel
from typing import List, Optional


class Observation(BaseModel):
    goal: str
    email_content: str
    current_stage: str
    history: List[str]
    available_actions: List[str]
    last_action_error: Optional[str] = None


class Action(BaseModel):
    action_type: str
    payload: Optional[str] = None