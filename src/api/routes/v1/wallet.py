from fastapi import APIRouter


wallet_router = APIRouter(prefix="/v1/wallet", tags=["Wallet"])

@wallet_router.get("/{player_id}")
async def get_wallet(player_id: int):
    """
    Retrieve wallet information by player ID.
    """
    # Placeholder for actual implementation
    return {"player_id": player_id, "balance": 1000, "currency": "USD"}