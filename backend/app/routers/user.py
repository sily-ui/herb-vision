"""用户接口路由"""
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database.db import get_db
from app.models.user import User
from app.models.identify_record import IdentifyRecord
from app.utils.auth import create_access_token, get_current_user

router = APIRouter(prefix="/api", tags=["用户"])

# 微信API地址
WX_API_URL = "https://api.weixin.qq.com/sns/jscode2session"


class WxLoginRequest(BaseModel):
    """微信登录请求"""
    code: str


class UpdateProfileRequest(BaseModel):
    """更新用户信息请求"""
    nickname: str = None
    avatar_url: str = None
    phone: str = None


@router.post("/auth/wx-login")
async def wx_login(request: WxLoginRequest, db: Session = Depends(get_db)):
    """微信小程序登录（code换openid）"""
    if not settings.WX_APPID or settings.WX_APPID in ("your_appid", ""):
        return _dev_login(db)

    params = {
        "appid": settings.WX_APPID,
        "secret": settings.WX_SECRET,
        "js_code": request.code,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WX_API_URL, params=params)
        data = response.json()

    openid = data.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="微信登录失败，无法获取openid")

    user = db.query(User).filter(User.openid == openid).first()
    if user is None:
        user = User(openid=openid, created_at=datetime.now(), updated_at=datetime.now())
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {
        "token": token,
        "user": {
            "id": user.id,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
        },
    }


@router.post("/auth/dev-login")
async def dev_login(db: Session = Depends(get_db)):
    """开发环境快捷登录（无需真实微信 code）"""
    return _dev_login(db)


def _dev_login(db: Session):
    """开发环境创建/获取 mock 用户并返回 token"""
    mock_openid = "dev-user-001"
    user = db.query(User).filter(User.openid == mock_openid).first()
    if user is None:
        user = User(openid=mock_openid, nickname="道友", created_at=datetime.now(), updated_at=datetime.now())
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {
        "token": token,
        "user": {
            "id": user.id,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
        },
    }


@router.get("/user/profile")
async def get_profile(current_user=Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "openid": current_user.openid,
        "nickname": current_user.nickname,
        "avatar_url": current_user.avatar_url,
        "phone": current_user.phone,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }


@router.put("/user/profile")
async def update_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """更新用户信息"""
    if request.nickname is not None:
        current_user.nickname = request.nickname
    if request.avatar_url is not None:
        current_user.avatar_url = request.avatar_url
    if request.phone is not None:
        current_user.phone = request.phone

    current_user.updated_at = datetime.now()
    db.commit()

    return {"message": "更新成功"}


@router.get("/user/records")
async def get_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """获取识别记录列表"""
    query = db.query(IdentifyRecord).filter(IdentifyRecord.user_id == current_user.id)
    total = query.count()
    offset = (page - 1) * page_size
    records = query.order_by(IdentifyRecord.created_at.desc()).offset(offset).limit(page_size).all()

    items = []
    for record in records:
        items.append({
            "id": record.id,
            "image_path": record.image_path,
            "herb_name": record.herb_name,
            "confidence": record.confidence,
            "is_favorited": record.is_favorited,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        })

    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.delete("/user/records/{record_id}")
async def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """删除识别记录"""
    record = db.query(IdentifyRecord).filter(
        IdentifyRecord.id == record_id,
        IdentifyRecord.user_id == current_user.id,
    ).first()

    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")

    db.delete(record)
    db.commit()

    return {"message": "删除成功"}


@router.get("/user/favorites")
async def get_favorites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """获取收藏列表"""
    query = db.query(IdentifyRecord).filter(
        IdentifyRecord.user_id == current_user.id,
        IdentifyRecord.is_favorited == True,
    )
    total = query.count()
    records = query.order_by(IdentifyRecord.created_at.desc()).all()

    items = []
    for record in records:
        items.append({
            "id": record.id,
            "image_path": record.image_path,
            "herb_name": record.herb_name,
            "confidence": record.confidence,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        })

    return {"total": total, "items": items}


@router.post("/user/favorites")
async def add_favorite(
    record_id: int = Query(..., description="识别记录ID"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """添加收藏"""
    record = db.query(IdentifyRecord).filter(
        IdentifyRecord.id == record_id,
        IdentifyRecord.user_id == current_user.id,
    ).first()

    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")

    record.is_favorited = True
    db.commit()

    return {"message": "收藏成功"}


@router.delete("/user/favorites/{record_id}")
async def remove_favorite(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """取消收藏"""
    record = db.query(IdentifyRecord).filter(
        IdentifyRecord.id == record_id,
        IdentifyRecord.user_id == current_user.id,
    ).first()

    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")

    record.is_favorited = False
    db.commit()

    return {"message": "取消收藏成功"}
