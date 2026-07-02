"""识别接口路由"""
import json
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.identify_record import IdentifyRecord
from app.services.ai_service import identify_herb
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["识别"])

# 上传图片保存目录
UPLOAD_DIR = "uploads/identify"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
        result = await identify_herb(image_bytes)
    except Exception as e:
        # AI调用失败时返回错误信息
        raise HTTPException(status_code=500, detail=f"AI识别服务异常: {str(e)}")

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

    return {
        "record_id": record.id,
        "result": result,
    }
