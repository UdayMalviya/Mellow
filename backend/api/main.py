from fastapi import FastAPI
from backend.api.routers import routes, users

app = FastAPI()
app.include_router(routes.router)
app.include_router(users.router)
