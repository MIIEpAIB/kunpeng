"""移动端接口 v1：测字/抽签 /api/divination/*, /api/lottery/*（接入 DeepSeek）"""
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.app.core.deepseek import chat as deepseek_chat
from backend.app.schemas.common import APIResponse

router_div = APIRouter(prefix="/api/divination", tags=["Mobile-Divination"])
router_lot = APIRouter(prefix="/api/lottery", tags=["Mobile-Lottery"])


def _call_ai(system: str, user: str) -> str:
    try:
        return deepseek_chat(system, user)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI 服务暂时不可用: {str(e)}")


@router_div.get("/purpose/list", response_model=APIResponse[list])
def mobile_divination_purpose_list():
    """移动端：测字目的选项"""
    return APIResponse(code=0, msg="ok", data=[{"purpose_code": "fortune", "purpose_name": "问财运"}, {"purpose_code": "marriage", "purpose_name": "问姻缘"}])


class CharacterCalculateBody(BaseModel):
    character: str = ""
    purpose_code: str = ""


@router_div.post("/character/calculate", response_model=APIResponse[dict])
def mobile_character_calculate(body: CharacterCalculateBody):
    """移动端：测字测算（DeepSeek）"""
    sys = "你是测字师，根据用户写的一个字和问事目的，用中文从字形、字义、寓意给出简短解读，语气温和。"
    user = f"字：{body.character or '未提供'}，问事类型：{body.purpose_code or '一般'}"
    text = _call_ai(sys, user)
    return APIResponse(
        code=0,
        msg="ok",
        data={"result_id": str(uuid4()), "analysis": text, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )


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
    """移动端：抽签（DeepSeek 生成签文）"""
    sys = "你是解签师。请随机生成一签：签号（如第壹签）、吉凶等级（上上/上吉/中平/下等）、一句签诗、一句白话解释。用中文，一行一行写，格式：签号、等级、签诗、解释。"
    user = f"问事类型：{body.purpose_code or '求签'}"
    text = _call_ai(sys, user)
    lines = [s.strip() for s in (text or "").split("\n") if s.strip()]
    lottery_no = lines[0] if lines else "第壹签"
    lottery_level = lines[1] if len(lines) > 1 else "上上签"
    return APIResponse(
        code=0,
        msg="ok",
        data={
            "lottery_id": str(uuid4()),
            "lottery_no": lottery_no,
            "lottery_level": lottery_level,
            "draw_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lottery_poetry": lines[2] if len(lines) > 2 else text,
            "lottery_explain": lines[3] if len(lines) > 3 else text,
        },
    )


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
    """移动端：解签（DeepSeek）"""
    sys = "你是解签师，对用户抽到的签给出签诗与详细白话解释，语气温和、正向。用中文。"
    user = f"签 ID：{body.lottery_id}，请直接给出一段签诗和一段解释。"
    text = _call_ai(sys, user)
    return APIResponse(
        code=0,
        msg="ok",
        data={
            "lottery_id": body.lottery_id,
            "lottery_poetry": text.split("\n")[0] if text else "",
            "lottery_explain": text,
        },
    )


@router_lot.post("/share", response_model=APIResponse[dict])
def mobile_lottery_share(body: LotteryInterpretBody):
    """移动端：分享抽签"""
    return APIResponse(code=0, msg="ok", data={"share_url": "", "share_image": "", "share_title": ""})
