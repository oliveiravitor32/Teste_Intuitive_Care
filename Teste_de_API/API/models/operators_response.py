from typing import List

from pydantic import BaseModel

from models.operator import Operator


class OperatorsResponse(BaseModel):
    data: List[Operator]
