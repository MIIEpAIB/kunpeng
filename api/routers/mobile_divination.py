"""移动端接口 v1：测字/抽签 /api/divination/*, /api/lottery/*"""
from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.app.schemas.common import APIResponse

router_div = APIRouter(prefix="/api/divination", tags=["Mobile-Divination"])
router_lot = APIRouter(prefix="/api/lottery", tags=["Mobile-Lottery"])


@router_div.get("/purpose/list", response_model=APIResponse[list])
def mobile_divination_purpose_list():
    """移动端：测字目的选项"""
    return APIResponse(code=0, msg="ok", data=[{"purpose_code": "fortune", "purpose_name": "问财运"}, {"purpose_code": "marriage", "purpose_name": "问姻缘"}])


class CharacterCalculateBody(BaseModel):
    character: str = ""
    purpose_code: str = ""


@router_div.post("/character/calculate", response_model=APIResponse[dict])
def mobile_character_calculate(body: CharacterCalculateBody):
    """移动端：测字测算"""
    return APIResponse(code=0, msg="ok", data={"result_id": "uuid", "analysis": "", "created_at": ""})


@router_div.get("/history/list", response_model=APIResponse[dict])
def mobile_divination_history_list(page_num: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """移动端：测字历史"""
    return APIResponse(code=0, msg="ok", data={"total": 0, "list": []})


@router_div.get("/history/detail", response_model=APIResponse[dict])
def mobile_divination_history_detail(record_id: str = Query(...)):
    """移动端：测字记录详情"""
    return APIResponse(code=0, msg="ok", data={"record_id": record_id})


# ---------- lottery ----------
@router_lot.get("/purpose/list", response_model=APIResponse[list])
def mobile_lottery_purpose_list():
    """移动端：抽签目的选项"""
    return APIResponse(code=0, msg="ok", data=[{"purpose_code": "fortune", "purpose_name": "问财运"}])


class LotteryDrawBody(BaseModel):
    purpose_code: str = ""


@router_lot.post("/draw", response_model=APIResponse[dict])
def mobile_lottery_draw(body: LotteryDrawBody):
    """移动端：抽签"""
    return APIResponse(code=0, msg="ok", data={"lottery_id": "uuid", "lottery_no": "第壹签", "lottery_level": "上上签", "draw_time": ""})


@router_lot.get("/history/list", response_model=APIResponse[dict])
def mobile_lottery_history_list(page_num: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """移动端：抽签历史"""
    return APIResponse(code=0, msg="ok", data={"total": 0, "list": []})


@router_lot.get("/history/detail", response_model=APIResponse[dict])
def mobile_lottery_history_detail(lottery_id: str = Query(...)):
    """移动端：抽签记录详情"""
    return APIResponse(code=0, msg="ok", data={"lottery_id": lottery_id})


class LotteryInterpretBody(BaseModel):
    lottery_id: str = ""


@router_lot.post("/interpret", response_model=APIResponse[dict])
def mobile_lottery_interpret(body: LotteryInterpretBody):
    """移动端：解签"""
    return APIResponse(code=0, msg="ok", data={"lottery_id": body.lottery_id, "lottery_poetry": "", "lottery_explain": ""})


@router_lot.post("/share", response_model=APIResponse[dict])
def mobile_lottery_share(body: LotteryInterpretBody):
    """移动端：分享抽签"""
    return APIResponse(code=0, msg="ok", data={"share_url": "", "share_image": "", "share_title": ""})
