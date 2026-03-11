from fastapi import FastAPI

from backend.app.api.routers import (
    admin_auth,
    admin_users,
    admin_products,
    admin_orders,
)


app = FastAPI(
    title="Kunpeng Yidao Admin & App API",
    version="1.0.0",
)


app.include_router(admin_auth.router)
app.include_router(admin_users.router)
app.include_router(admin_products.router)
app.include_router(admin_orders.router)


@app.get("/health", tags=["System"])
def health_check() -> dict:
    return {"code": 0, "msg": "ok", "data": {"status": "healthy"}}

