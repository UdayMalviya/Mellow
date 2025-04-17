from fastapi import FastAPI
from backend.api.routers import routes

app = FastAPI()
app.include_router(routes.router)
