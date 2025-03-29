from typing import Optional

from pydantic import BaseModel


class SearchParams(BaseModel):
    """Parameters for healthcare operator search"""
    query: str
    search_razao_social: bool = True
    # TODO: Do when the front end is finished to check if it will be possible to handle that many custom params
    # search_nome_fantasia: bool = True
    # search_cidade: bool = False
    # uf_filter: Optional[str] = None
    limit: int = 20
