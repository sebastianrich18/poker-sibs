from fastapi import APIRouter

from api.schemas import GetTableResponse


table_router = APIRouter(prefix="/v1/table", tags=["Table"])

@table_router.get("/{table_id}", response_model=GetTableResponse)
async def get_table(table_id: int):
    """
    Retrieve table information by table ID.
    """
    # Placeholder for actual implementation
    return {"table_id": table_id, "status": "open", "max_seats": 6}