from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel

Url = str
ErrorInfo = Dict[Optional[str], Optional[str]]


class ExpertiseInfoInResponse(BaseModel):
    language_name: Optional[str]
    experience: Optional[float]
    description: Optional[str]


class DeveloperInfoInResponse(BaseModel):
    first_name: Optional[str]
    github_account: Url
    stack: List[ExpertiseInfoInResponse]


class TicketInfoInResponse(BaseModel):
    id: int
    created: datetime
    title: Optional[str]
    description: Optional[str]
    points: int
    assigned_to: DeveloperInfoInResponse
