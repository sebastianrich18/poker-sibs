from fastapi import Header, HTTPException

from .auth import validate_token


async def get_current_player(authorization: str = Header(...)) -> str:
    token = authorization.replace("Bearer ", "")
    payload = validate_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["player_id"]
