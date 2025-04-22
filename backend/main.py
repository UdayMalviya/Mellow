from fastapi import FastAPI
from backend.api.routers import routes, dataset, version, data_cleaning

app = FastAPI(title="Mellow BI Platform")

app.include_router(routes.router)
app.include_router(dataset.router)
app.include_router(version.router)
app.include_router(data_cleaning.router)
