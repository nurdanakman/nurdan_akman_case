from enum import auto

from pydantic import BaseModel
from typing import Optional, List

from strenum import StrEnum


class Details(BaseModel):
    id : int
    name: str

class StatusTypes(StrEnum):
    available = auto()
    pending = auto()
    sold = auto()

class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Details] = None
    name: Optional[str] = None
    photoUrls: List[Optional[str]] = []
    tags: List[Optional[Details]] = []
    status: Optional[StatusTypes] = None