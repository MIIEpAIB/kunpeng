"""v1 祭祀：贡品分类/列表、陵墓、订单、动态 /api/sacrifice/*"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.security import get_current_admin
from backend.app.db import models
from backend.app.db.database import get_db
from backend.app.schemas.common import APIResponse

router = APIRouter(prefix="/api/sacrifice", tags=["Sacrifice"])


# ---------- 贡品分类 ----------
@router.get("/category/list", response_model=APIResponse[dict])
def category_list(
    category_name: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    page_num: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    q = db.query(models.OfferingCategory)
    if category_name:
        q = q.filter(models.OfferingCategory.name.like(f"%{category_name}%"))
    if start_date:
        try:
            q = q.filter(models.OfferingCategory.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
        except ValueError:
            pass
    if end_date:
        try:
            q = q.filter(models.OfferingCategory.created_at <= datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            pass
    total = q.count()
    rows = q.order_by(models.OfferingCategory.id.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
    list_ = [{"id": r.id, "category_name": r.name, "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""} for r in rows]
    return APIResponse[dict](code=0, msg="ok", data={"total": total, "list": list_})


@router.get("/category/all", response_model=APIResponse[dict])
def category_all(
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    rows = db.query(models.OfferingCategory).order_by(models.OfferingCategory.id).all()
    list_ = [{"id": r.id, "category_name": r.name} for r in rows]
    return APIResponse[dict](code=0, msg="ok", data={"list": list_})


class CategoryAddBody(BaseModel):
    category_name: str


@router.post("/category/add", response_model=APIResponse[dict])
def category_add(
    body: CategoryAddBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    c = models.OfferingCategory(name=body.category_name)
    db.add(c)
    db.commit()
    return APIResponse[dict](code=0, msg="新增成功", data=None)


class CategoryEditBody(BaseModel):
    id: int
    category_name: str


@router.post("/category/edit", response_model=APIResponse[dict])
def category_edit(
    body: CategoryEditBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    r = db.query(models.OfferingCategory).filter(models.OfferingCategory.id == body.id).first()
    if not r:
        raise HTTPException(404, "分类不存在")
    r.name = body.category_name
    db.commit()
    return APIResponse[dict](code=0, msg="保存成功", data=None)


# ---------- 贡品列表 ----------
@router.get("/tribute/list", response_model=APIResponse[dict])
def tribute_list(
    tribute_name: str | None = Query(None),
    category_id: int | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    page_num: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    q = db.query(models.Offering)
    if tribute_name:
        q = q.filter(models.Offering.name.like(f"%{tribute_name}%"))
    if category_id:
        q = q.filter(models.Offering.category_id == category_id)
    if start_date:
        try:
            q = q.filter(models.Offering.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
        except ValueError:
            pass
    if end_date:
        try:
            q = q.filter(models.Offering.created_at <= datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            pass
    total = q.count()
    rows = q.order_by(models.Offering.id.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
    list_ = []
    for r in rows:
        cat = db.get(models.OfferingCategory, r.category_id)
        list_.append({
            "id": r.id,
            "tribute_name": r.name,
            "category_id": r.category_id,
            "category_name": cat.name if cat else "",
            "image_url": r.icon or "",
            "price": r.price_coin,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
        })
    return APIResponse[dict](code=0, msg="ok", data={"total": total, "list": list_})


class TributeAddBody(BaseModel):
    tribute_name: str
    category_id: int
    image_url: str = ""
    price: int


@router.post("/tribute/add", response_model=APIResponse[dict])
def tribute_add(
    body: TributeAddBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    o = models.Offering(name=body.tribute_name, category_id=body.category_id, price_coin=body.price, icon=body.image_url or None)
    db.add(o)
    db.commit()
    return APIResponse[dict](code=0, msg="新增成功", data=None)


@router.get("/tribute/detail", response_model=APIResponse[dict])
def tribute_detail(
    id: int = Query(..., alias="id"),
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    r = db.get(models.Offering, id)
    if not r:
        raise HTTPException(404, "贡品不存在")
    return APIResponse[dict](code=0, msg="ok", data={"id": r.id, "tribute_name": r.name, "category_id": r.category_id, "image_url": r.icon or "", "price": r.price_coin})


class TributeEditBody(BaseModel):
    id: int
    tribute_name: str
    category_id: int
    image_url: str = ""
    price: int


@router.post("/tribute/edit", response_model=APIResponse[dict])
def tribute_edit(
    body: TributeEditBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    r = db.get(models.Offering, body.id)
    if not r:
        raise HTTPException(404, "贡品不存在")
    r.name = body.tribute_name
    r.category_id = body.category_id
    r.icon = body.image_url or None
    r.price_coin = body.price
    db.commit()
    return APIResponse[dict](code=0, msg="保存成功", data=None)


class TributeDeleteBody(BaseModel):
    id: int


@router.post("/tribute/delete", response_model=APIResponse[dict])
def tribute_delete(
    body: TributeDeleteBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    db.query(models.Offering).filter(models.Offering.id == body.id).delete()
    db.commit()
    return APIResponse[dict](code=0, msg="删除成功", data=None)


# ---------- 祭祀动态 ----------
class SacrificeDynamicCreateBody(BaseModel):
    user_account: str
    tribute_name: str
    message: str
    deceased_name: str
    relationship: str


@router.post("/dynamic/create", response_model=APIResponse[dict])
def dynamic_create(
    body: SacrificeDynamicCreateBody,
    db: Session = Depends(get_db),
    admin: models.AdminUser = Depends(get_current_admin),
):
    feed = models.SacrificeFeed(
        user_mobile=body.user_account,
        offering_name=body.tribute_name,
        deceased_name=body.deceased_name,
        relation=body.relationship,
        content=body.message,
        sacrifice_time=datetime.utcnow(),
        created_by_admin=admin.id,
    )
    db.add(feed)
    db.commit()
    return APIResponse[dict](code=0, msg="创建成功", data=None)
