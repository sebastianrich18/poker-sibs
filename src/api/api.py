from fastapi import FastAPI
from api.routes.v1.table import table_router
from api.routes.v1.player import player_router
from api.routes.v1.wallet import wallet_router

app = FastAPI(title="Poker Sibs API", version="1.0")

app.include_router(table_router, prefix="/api")
app.include_router(player_router, prefix="/api")
app.include_router(wallet_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "version": app.version}
