from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash, verify_password
from backend.app.db import models
from backend.app.db.database import get_db
from backend.app.schemas.admin import AdminLoginRequest, AdminLoginResponse
from backend.app.schemas.common import APIResponse


router = APIRouter(prefix="/api/admin", tags=["AdminAuth"])


@router.post(
    "/login",
    response_model=APIResponse[AdminLoginResponse],
    summary="管理员登录",
)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = (
        db.query(models.AdminUser)
        .filter(models.AdminUser.username == payload.username)
        .first()
    )
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误"
        )
    if not verify_password(payload.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误"
        )
    if admin.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="管理员已禁用"
        )

    token = create_access_token(
        data={"sub": admin.id}, expires_delta=timedelta(hours=8)
    )
    resp = AdminLoginResponse(
        token=token, admin_id=admin.id, username=admin.username, roles=[]
    )
    return APIResponse[AdminLoginResponse](code=0, msg="ok", data=resp)


@router.post(
    "/init-super-admin",
    summary="初始化超级管理员（仅开发调试用）",
)
def init_super_admin(db: Session = Depends(get_db)):
    """
    创建一个默认的 admin/admin123 管理员，避免无法登录。
    生产环境应删除或关闭此接口。
    """
    exists = db.query(models.AdminUser).filter_by(username="admin").first()
    if exists:
        return {"code": 0, "msg": "already_exists"}
    admin = models.AdminUser(
        username="admin", password_hash=get_password_hash("admin123"), status=1
    )
    db.add(admin)
    db.commit()
    return {"code": 0, "msg": "ok", "data": {"username": "admin", "password": "admin123"}}

