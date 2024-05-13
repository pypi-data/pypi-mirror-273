from typing import Iterable, Optional, Dict, List, AnyStr

from pydantic import BaseModel


class Case(BaseModel):
    id: int
    meta: Dict[str, List[List[str]]]
    steps: List[dict]


class Suite(BaseModel):
    name: str
    case_list: List[Case]
