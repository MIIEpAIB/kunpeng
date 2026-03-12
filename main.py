import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 使用相对导入，兼容本地 (backend.app.main) 和服务器 (app.main) 两种运行方式
from .api.routers import (
    admin_auth,
    admin_system,
    admin_users,
    admin_products,
    admin_orders,
    captcha,
    dashboard,
    common,
    operation,
    user,
    product,
    product_order,
    blessing,
    sacrifice,
)


app = FastAPI(
    title="Kunpeng Yidao Admin & App API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_auth.router)
app.include_router(admin_system.router)
app.include_router(admin_users.router)
app.include_router(admin_products.router)
app.include_router(admin_orders.router)
app.include_router(captcha.router)
app.include_router(dashboard.router)
app.include_router(common.router)
app.include_router(operation.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(product_order.router)
app.include_router(blessing.router)
app.include_router(sacrifice.router)

# 上传文件静态访问
_static = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(_static):
    app.mount("/static", StaticFiles(directory=_static), name="static")


@app.get("/health", tags=["System"])
def health_check() -> dict:
    return {"code": 0, "msg": "ok", "data": {"status": "healthy"}}

