"""Entry point. Creates the FastAPI instance, includes the router(s), sets up any startup/shutdown events (like checking DB connection).
 This file should stay thin — it wires things together, it doesn't contain logic."""

from fastapi import FastAPI
from app.routers.urls import router 

app = FastAPI()

app.include_router(router)