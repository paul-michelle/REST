from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass

Url = str
ErrorInfo = Dict[Optional[str], Optional[str]]


@dataclass
class ExpertiseInfo:
    language_name: str
    experience: float
    description: str


@dataclass
class DeveloperInfo:
    first_name: str
    github_account: Url
    stack: List[ExpertiseInfo]


@dataclass
class TicketInfo:
    created: datetime
    title: str
    description: str
    points: int
    assigned_to: DeveloperInfo

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)
