from fastapi import APIRouter, Depends, Query, HTTPException
from models.operators_response import OperatorsResponse
from models.search_params import SearchParams

from services.search_service import SearchService

router = APIRouter()


@router.get("/operators/search", response_model=OperatorsResponse)
async def search_operadoras(
        query: str = Query(..., description="Search term"),
        category: str = Query(..., description="Search category"),
        search_service: SearchService = Depends(),
):
    """
    Search healthcare operators by text query.
    Returns the most relevant matches based on the search parameters.
    """

    search_params = SearchParams(
        query=query,
        category=category
    )

    # Set definitive 20 limit to avoid malicious request
    search_params.limit = 20

    results = search_service.search_operadoras(search_params)

    if not results:
        raise HTTPException(status_code=404, detail="No matching operators found")

    return results
