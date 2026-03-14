"""移动端接口 v1：商城 /api/mall/*, /api/account/recharge/*"""
from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.app.schemas.common import APIResponse

router_mall = APIRouter(prefix="/api/mall", tags=["Mobile-Mall"])
router_account = APIRouter(prefix="/api/account", tags=["Mobile-Account"])


@router_mall.get("/product/filter/options", response_model=APIResponse[dict])
def mobile_mall_filter_options():
    """移动端：商品筛选选项（分类、生肖、价格等）"""
    return APIResponse(code=0, msg="ok", data={"types": [], "zodiacs": [], "price_ranges": []})


@router_mall.get("/product/list", response_model=APIResponse[dict])
def mobile_mall_product_list(
    page_num: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    type_code: str | None = Query(None),
    zodiac_code: str | None = Query(None),
    price_min: int | None = Query(None),
    price_max: int | None = Query(None),
):
    """移动端：商品列表"""
    return APIResponse(code=0, msg="ok", data={"total": 0, "page_num": page_num, "page_size": page_size, "list": []})


@router_mall.get("/product/detail", response_model=APIResponse[dict])
def mobile_mall_product_detail(product_id: str = Query(...)):
    """移动端：商品详情"""
    return APIResponse(code=0, msg="ok", data={"product_id": product_id, "product_name": "", "price": 0, "description": ""})


class MallCartAddBody(BaseModel):
    product_id: str = ""
    quantity: int = 1


@router_mall.post("/cart/add", response_model=APIResponse[dict])
def mobile_mall_cart_add(body: MallCartAddBody):
    """移动端：加入购物车"""
    return APIResponse(code=0, msg="ok", data={"cart_id": "uuid", "message": "加入购物车成功"})


class MallOrderCreateBody(BaseModel):
    product_id: str = ""
    quantity: int = 1
    address_id: str = ""


@router_mall.post("/order/create", response_model=APIResponse[dict])
def mobile_mall_order_create(body: MallOrderCreateBody):
    """移动端：立即购买创建订单"""
    return APIResponse(code=0, msg="ok", data={"order_id": "uuid", "order_no": "", "total_amount": 0})


# ---------- account/recharge ----------
@router_account.get("/recharge/config", response_model=APIResponse[dict])
def mobile_recharge_config():
    """移动端：充值配置"""
    return APIResponse(code=0, msg="ok", data={"min_recharge_amount": 10.0, "recharge_tips": "所充金额可用于购买产品、网上祭祀、网上祈福等服务"})


class RechargeOrderCreateBody(BaseModel):
    recharge_amount: float = 0
    pay_method: str = "alipay"


@router_account.post("/recharge/order/create", response_model=APIResponse[dict])
def mobile_recharge_order_create(body: RechargeOrderCreateBody):
    """移动端：创建充值订单"""
    return APIResponse(code=0, msg="ok", data={"order_id": "uuid", "order_no": "", "recharge_amount": body.recharge_amount, "pay_params": {}})


@router_account.get("/recharge/order/status", response_model=APIResponse[dict])
def mobile_recharge_order_status(order_id: str = Query(...)):
    """移动端：查询充值订单状态"""
    return APIResponse(code=0, msg="ok", data={"order_id": order_id, "order_status": "pending", "current_balance": 0})
