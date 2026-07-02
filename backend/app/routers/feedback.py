"""反馈接口路由"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.feedback import Feedback
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/feedback", tags=["反馈"])


class FeedbackCreateRequest(BaseModel):
    """提交反馈请求"""
    herb_id: int = None
    feedback_type: str  # identify_error / data_missing / other
    content: str
    image_path: str = None


@router.post("")
async def create_feedback(
    request: FeedbackCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """提交反馈"""
    # 验证反馈类型
    valid_types = ["identify_error", "data_missing", "other"]
    if request.feedback_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"反馈类型无效，可选值: {valid_types}")

    feedback = Feedback(
        user_id=current_user.id,
        herb_id=request.herb_id,
        feedback_type=request.feedback_type,
        content=request.content,
        image_path=request.image_path,
        status="pending",
        created_at=datetime.now(),
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "id": feedback.id,
        "message": "反馈提交成功",
    }


@router.get("")
async def list_feedback(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None, description="按状态筛选: pending/reviewed/resolved"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """获取反馈列表（管理端）"""
    query = db.query(Feedback)

    if status:
        query = query.filter(Feedback.status == status)

    total = query.count()
    offset = (page - 1) * page_size
    feedbacks = query.order_by(Feedback.created_at.desc()).offset(offset).limit(page_size).all()

    items = []
    for fb in feedbacks:
        items.append({
            "id": fb.id,
            "user_id": fb.user_id,
            "herb_id": fb.herb_id,
            "feedback_type": fb.feedback_type,
            "content": fb.content,
            "image_path": fb.image_path,
            "status": fb.status,
            "admin_reply": fb.admin_reply,
            "created_at": fb.created_at.isoformat() if fb.created_at else None,
        })

    return {"total": total, "page": page, "page_size": page_size, "items": items}
