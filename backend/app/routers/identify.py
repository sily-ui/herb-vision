"""识别接口路由"""
import json
import os
import re
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.herb import Herb
from app.models.identify_record import IdentifyRecord
from app.services.ai_service import identify_herb
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["识别"])

# 上传图片保存目录
UPLOAD_DIR = "uploads/identify"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _normalize_name(name: str) -> str:
    """统一名称用于模糊匹配"""
    return re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", (name or "").lower())


def _match_herb_in_db(db: Session, ai_name: str, aliases: str = "") -> Optional[Herb]:
    """用 AI 识别出的药材名在数据库中查找最匹配的药材"""
    if not ai_name:
        return None

    target = _normalize_name(ai_name)
    if not target:
        return None

    herbs = db.query(Herb).all()
    best = None
    best_score = 0

    for herb in herbs:
        score = 0
        candidates = [herb.name, herb.aliases or ""]
        for cand in candidates:
            norm_cand = _normalize_name(cand)
            if not norm_cand:
                continue
            if target in norm_cand or norm_cand in target:
                score = max(score, len(norm_cand))
            for t in [target, _normalize_name(aliases)]:
                if t and t in norm_cand:
                    score = max(score, len(t))
        if score > best_score:
            best_score = score
            best = herb

    return best


def _ai_confidence_to_number(confidence) -> int:
    """把 AI 返回的置信度转成数字"""
    if isinstance(confidence, (int, float)):
        return int(confidence)
    if confidence == "高":
        return 92
    if confidence == "中":
        return 72
    if confidence == "低":
        return 45
    return 50


@router.post("/identify")
async def identify_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """上传图片识别中药

    接收用户上传的中药图片，调用AI大模型进行识别，返回识别结果并保存记录。
    """
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    # 读取图片字节
    image_bytes = await file.read()

    # 限制文件大小（10MB）
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")

    # 保存上传的图片
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    try:
        # 调用AI服务进行识别
        ai_result = await identify_herb(image_bytes)
    except Exception as e:
        # AI调用失败时返回错误信息
        raise HTTPException(status_code=500, detail=f"AI识别服务异常: {str(e)}")

    # 尝试把 AI 识别结果与数据库药材匹配，提升结果可靠性
    matched_herb = _match_herb_in_db(db, ai_result.get("name"), ai_result.get("aliases", ""))

    if matched_herb:
        result = {
            "herb_id": matched_herb.id,
            "name": matched_herb.name,
            "aliases": matched_herb.aliases or "",
            "family": matched_herb.family or ai_result.get("family", ""),
            "source": matched_herb.source or ai_result.get("source", ""),
            "part_used": matched_herb.part_used or "",
            "nature_taste": matched_herb.nature_taste or ai_result.get("nature_taste", ""),
            "meridian_tropism": matched_herb.meridian_tropism or ai_result.get("meridian_tropism", ""),
            "efficacy": matched_herb.efficacy or ai_result.get("efficacy", ""),
            "indications": matched_herb.indications or ai_result.get("indications", ""),
            "usage_dosage": matched_herb.usage_dosage or ai_result.get("usage_dosage", ""),
            "contraindications": matched_herb.contraindications or ai_result.get("contraindications", ""),
            "appearance": {
                "color": matched_herb.appearance_color or ai_result.get("appearance", {}).get("color", ""),
                "texture": matched_herb.appearance_texture or ai_result.get("appearance", {}).get("texture", ""),
                "fracture": matched_herb.appearance_fracture or ai_result.get("appearance", {}).get("fracture", ""),
                "odor": matched_herb.appearance_odor or ai_result.get("appearance", {}).get("odor", ""),
            },
            "authenticity_tips": matched_herb.authenticity_tips or ai_result.get("authenticity_tips", ""),
            "confusable_herbs": matched_herb.confusable_herbs or ai_result.get("confusable_herbs", ""),
            "confidence": _ai_confidence_to_number(ai_result.get("confidence")),
            "image": matched_herb.image_main or "",
            "matched_from_db": True,
        }
    else:
        # 未匹配到数据库，使用 AI 原始结果
        result = {
            "herb_id": None,
            "name": ai_result.get("name", "未知药材"),
            "aliases": ai_result.get("aliases", ""),
            "family": ai_result.get("family", ""),
            "source": ai_result.get("source", ""),
            "part_used": "",
            "nature_taste": ai_result.get("nature_taste", ""),
            "meridian_tropism": ai_result.get("meridian_tropism", ""),
            "efficacy": ai_result.get("efficacy", ""),
            "indications": ai_result.get("indications", ""),
            "usage_dosage": ai_result.get("usage_dosage", ""),
            "contraindications": ai_result.get("contraindications", ""),
            "appearance": ai_result.get("appearance", {}),
            "authenticity_tips": ai_result.get("authenticity_tips", ""),
            "confusable_herbs": ai_result.get("confusable_herbs", ""),
            "confidence": _ai_confidence_to_number(ai_result.get("confidence")),
            "image": "",
            "matched_from_db": False,
        }

    # 保存识别记录到数据库
    herb_name = result.get("name", "未知")
    confidence = result.get("confidence", "低")

    record = IdentifyRecord(
        user_id=current_user.id,
        image_path=file_path,
        herb_name=herb_name,
        confidence=confidence,
        result_json=json.dumps(result, ensure_ascii=False),
        created_at=datetime.now(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # 返回结果中注入 record_id，便于前端收藏/反馈
    result["record_id"] = record.id

    return {
        "record_id": record.id,
        "result": result,
    }
