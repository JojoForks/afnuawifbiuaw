from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import httpx
import re

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_URL = "https://courier.yandex.ru/vrs/api/v1/log"
UUID_PATTERN = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{8}-[a-f0-9]{8}-[a-f0-9]{8}$')

def validate_uuid(uuid: str) -> str:
    if not UUID_PATTERN.match(uuid):
        raise HTTPException(422, "Invalid UUID format")
    return uuid

@app.get("/request/{uuid}")
async def get_request(uuid: str = Path(...)):
    validate_uuid(uuid)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/request/{uuid}")
        return r.json()

@app.get("/original_request/{uuid}")
async def get_request(uuid: str = Path(...)):
    validate_uuid(uuid)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/original_request/{uuid}")
        return r.json()

@app.get("/response/{uuid}")
async def get_response(uuid: str = Path(...)):
    validate_uuid(uuid)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/response/{uuid}")
        return r.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4999)
