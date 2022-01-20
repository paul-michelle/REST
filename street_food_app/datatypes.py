from typing import List
from datetime import datetime
from dataclasses import dataclass

Url = str


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
