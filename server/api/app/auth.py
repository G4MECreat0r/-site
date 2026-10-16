import os
from fastapi import Header, HTTPException

TOKEN = os.getenv("DASHBOARD_TOKEN")


async def require_token(authorization: str | None = Header(default=None)) -> None:
    if not TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    if authorization.split(" ", 1)[1] != TOKEN:
        raise HTTPException(403, "bad token")
