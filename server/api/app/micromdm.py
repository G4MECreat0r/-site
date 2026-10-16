"""MicroMDM API クライアント（最小限）。"""
import httpx


class MicroMDM:
    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0) -> None:
        self.base = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.timeout = timeout

    async def devices(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.get(f"{self.base}/v1/devices", headers=self.headers)
            r.raise_for_status()
            data = r.json()
            return data.get("devices", data) if isinstance(data, dict) else data

    async def queue(self, udid: str, request_type: str, payload: dict | None = None) -> dict:
        body: dict = {"udid": udid, "request_type": request_type}
        if payload:
            body["command"] = payload
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.post(f"{self.base}/v1/commands", headers=self.headers, json=body)
            r.raise_for_status()
            return r.json()

    async def command(self, uuid: str) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.get(f"{self.base}/v1/commands/{uuid}", headers=self.headers)
            r.raise_for_status()
            return r.json()


def extract_command_uuid(resp: dict) -> str | None:
    if not isinstance(resp, dict):
        return None
    if isinstance(resp.get("uuid"), str):
        return resp["uuid"]
    for v in (resp.get("responses") or {}).values():
        if isinstance(v, dict) and isinstance(v.get("command_uuid"), str):
            return v["command_uuid"]
    return None


def extract_location(resp: dict) -> dict | None:
    """コマンド結果から緯度経度を拾う。スキーマ差異に耐えるよう幅広く探す。"""
    node = resp.get("results") or resp.get("command", {}).get("results") or resp
    if isinstance(node, dict) and "DeviceLocation" in node:
        loc = node["DeviceLocation"]
        if isinstance(loc, dict) and "Latitude" in loc:
            return loc
    return None
