from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from models.operator import OperatorResponse
from models.search_params import SearchParams

from services.search_service import SearchService

router = APIRouter()


@router.get("/operators/search", response_model=List[OperatorResponse])
async def search_operadoras(
        q: str = Query(..., description="Search term"),
        #
        # TODO: Do when the front end is finished to check if it will be possible to handle that many custom params
        #razao_social: Optional[bool] = Query(True, description="Search in razao_social field"),
        #nome_fantasia: Optional[bool] = Query(True, description="Search in nome_fantasia field"),
        #cidade: Optional[bool] = Query(False, description="Search in cidade field"),
        #uf: Optional[str] = Query(None, description="Filter by UF/state"),
        #limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
        search_service: SearchService = Depends(),
):
    """
    Search healthcare operators by text query.
    Returns the most relevant matches based on the search parameters.
    """

    # Set truncate custom params for test
    search_params = SearchParams(
        query=q,
        search_razao_social=True,
        #search_nome_fantasia=nome_fantasia,
        #search_cidade=cidade,
        #uf_filter=uf,
    )

    # Set definitive 20 limit to avoid malicious request
    search_params.limit = 20

    results = search_service.search_operadoras(search_params)

    if not results:
        raise HTTPException(status_code=404, detail="No matching operators found")

    return results
