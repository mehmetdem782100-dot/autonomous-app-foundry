from fastapi import FastAPI
from api.routers import projects
from core.resilience import wait_for_db

app = FastAPI(title="AAF - Core API")

@app.on_event("startup")
async def startup_event():
    await wait_for_db()

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(projects.router)
