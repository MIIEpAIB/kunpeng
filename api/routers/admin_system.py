from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.security import get_current_admin, get_password_hash, verify_password
from backend.app.db import models
from backend.app.db.database import get_db
from backend.app.schemas.common import APIResponse


router = APIRouter(prefix="/api/admin", tags=["AdminSystem"])


@router.post("/change-password", response_model=APIResponse[dict])
def change_admin_password_v1(
    body: dict,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    """
    按 v1 文档：
    URL: /api/admin/change-password
    Method: POST
    Body: { old_password, new_password, confirm_password }
    """
    old_password = body.get("old_password")
    new_password = body.get("new_password")
    confirm_password = body.get("confirm_password")
    if not old_password or not new_password or not confirm_password:
        raise HTTPException(
            status_code=400, detail="old_password, new_password, confirm_password required"
        )
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="new_password and confirm_password not match")
    if not verify_password(old_password, admin.password_hash):
        raise HTTPException(status_code=400, detail="old_password incorrect")
    admin.password_hash = get_password_hash(new_password)
    db.add(admin)
    db.commit()
    return APIResponse[dict](code=0, msg="ok", data={})


@router.put("/profile/password", response_model=APIResponse[dict])
def change_admin_password_legacy(
    body: dict,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    """
    兼容旧地址：/api/admin/profile/password
    Body: { old_password, new_password }
    """
    old_password = body.get("old_password")
    new_password = body.get("new_password")
    if not old_password or not new_password:
        raise HTTPException(status_code=400, detail="old_password and new_password required")
    if not verify_password(old_password, admin.password_hash):
        raise HTTPException(status_code=400, detail="old_password incorrect")
    admin.password_hash = get_password_hash(new_password)
    db.add(admin)
    db.commit()
    return APIResponse[dict](code=0, msg="ok", data={})


@router.get("/admin-users", response_model=APIResponse[dict])
def list_admin_users(
    username: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    q = db.query(models.AdminUser)
    if username:
        q = q.filter(models.AdminUser.username.like(f"%{username}%"))
    total = q.count()
    rows = (
        q.order_by(models.AdminUser.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    data_list = [
        {
            "id": a.id,
            "username": a.username,
            "roles": [],
            "status": a.status,
            "created_at": a.created_at,
        }
        for a in rows
    ]
    return APIResponse[dict](code=0, msg="ok", data={"total": total, "list": data_list})


@router.post("/admin-users", response_model=APIResponse[dict])
def create_admin_user(
    body: dict,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    exists = db.query(models.AdminUser).filter_by(username=username).first()
    if exists:
        raise HTTPException(status_code=400, detail="username exists")
    u = models.AdminUser(username=username, password_hash=get_password_hash(password), status=1)
    db.add(u)
    db.commit()
    db.refresh(u)
    return APIResponse[dict](code=0, msg="ok", data={"id": u.id})


@router.get("/op-logs", response_model=APIResponse[dict])
def list_op_logs(
    admin_name: str | None = Query(None),
    action: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    q = db.query(models.AdminOpLog)
    if admin_name:
        q = q.filter(models.AdminOpLog.username.like(f"%{admin_name}%"))
    if action:
        q = q.filter(models.AdminOpLog.action.like(f"%{action}%"))
    total = q.count()
    rows = (
        q.order_by(models.AdminOpLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    data_list = [
        {
            "id": r.id,
            "admin_id": r.admin_id,
            "username": r.username,
            "action": r.action,
            "target_type": r.target_type,
            "target_id": r.target_id,
            "detail": r.detail,
            "ip": r.ip,
            "created_at": r.created_at,
        }
        for r in rows
    ]
    return APIResponse[dict](code=0, msg="ok", data={"total": total, "list": data_list})

