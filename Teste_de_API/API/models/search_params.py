from typing import Optional

from pydantic import BaseModel


class SearchParams(BaseModel):
    """Parameters for healthcare operator search"""
    query: str
    category: str
    limit: int = 20
