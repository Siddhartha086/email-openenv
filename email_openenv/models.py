from pydantic import BaseModel
from typing import Optional


class ActionRequest(BaseModel):
    type: str
    label: Optional[str] = None
    department: Optional[str] = None
    response: Optional[str] = None