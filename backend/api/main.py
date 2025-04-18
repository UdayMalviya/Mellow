from fastapi import FastAPI
from backend.api.routers import (routes, users, roles,
                                permission, role_permission, users_roles,
                                tenants, tenant_user, data_sources,
                                time_series_meta, dataset, dataset_version,
                                encrupted_secret, cache, metric,
                                log, process_tracking)
app = FastAPI()
app.include_router(routes.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permission.router)
app.include_router(role_permission.router)
app.include_router(users_roles.router)
app.include_router(tenants.router)
app.include_router(tenant_user.router)
app.include_router(data_sources.router)
app.include_router(time_series_meta.router)
app.include_router(dataset.router)
app.include_router(dataset_version.router)
app.include_router(encrupted_secret.router)
app.include_router(cache.router)
app.include_router(metric.router)
app.include_router(log.router)
app.include_router(process_tracking.router)