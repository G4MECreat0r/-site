import asyncio
import os
import time

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .auth import require_token
from .micromdm import MicroMDM, extract_command_uuid, extract_location

app = FastAPI(title="MDM Location API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "*")],
    allow_methods=["*"],
    allow_headers=["*"],
)

mdm = MicroMDM(os.environ["MICROMDM_URL"], os.environ["MICROMDM_API_KEY"])
LATEST: dict[str, dict] = {}  # udid -> {lat, lon, accuracy, at}  ※永続化するならPostgresへ


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


@app.get("/devices", dependencies=[Depends(require_token)])
async def devices() -> dict:
    return {"devices": await mdm.devices(), "latest": LATEST}


@app.get("/devices/{udid}/location", dependencies=[Depends(require_token)])
async def get_location(udid: str) -> dict:
    if udid not in LATEST:
        raise HTTPException(404, "まだ取得していません")
    return LATEST[udid]


@app.post("/devices/{udid}/location", dependencies=[Depends(require_token)])
async def fetch_location(
    udid: str,
    timeout: int = Query(60, ge=5, le=180),
) -> dict:
    queued = await mdm.queue(udid, "DeviceLocation")
    cuuid = extract_command_uuid(queued)
    if not cuuid:
        return {"queued": queued, "note": "command_uuid を特定できませんでした"}

    deadline = time.time() + timeout
    while time.time() < deadline:
        cmd = await mdm.command(cuuid)
        loc = extract_location(cmd)
        if loc:
            result = {
                "udid": udid,
                "lat": float(loc["Latitude"]),
                "lon": float(loc["Longitude"]),
                "accuracy": loc.get("HorizontalAccuracy"),
                "at": loc.get("Timestamp") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            LATEST[udid] = result
            return result
        await asyncio.sleep(2)

    raise HTTPException(504, "端末から応答がありませんでした（オンライン/位置情報ONを確認）")
