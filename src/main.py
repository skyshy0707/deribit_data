from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.api.router import service

origins = [
    "http://localhost:9010"
]

app = FastAPI(
    docs_url="/docs",
    openapi_prefix="/api",
    title="Currencies",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

app.include_router(service.router)