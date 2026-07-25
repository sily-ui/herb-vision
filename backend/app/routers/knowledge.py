"""知识库接口路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.herb import Herb
from app.services.knowledge_service import (
    get_herbs,
    get_herb_by_id,
    search_herbs,
    compare_herbs,
)
from app.services.ai_service import ai_compare_herbs

router = APIRouter(prefix="/api/herbs", tags=["知识库"])


@router.get("")
async def list_herbs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category_part: str = Query(None, description="按部位分类筛选"),
    category_efficacy: str = Query(None, description="按功效分类筛选"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
):
    """获取药材列表（分页+筛选）"""
    result = get_herbs(db, page, page_size, category_part, category_efficacy, keyword)

    # 将ORM对象转为字典
    items = []
    for herb in result["items"]:
        items.append(_herb_to_dict(herb))

    return {
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "items": items,
    }


@router.get("/search")
async def search_herbs_api(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    db: Session = Depends(get_db),
):
    """关键词搜索药材（名称/别名/功效）"""
    herbs = search_herbs(db, keyword)
    return {"items": [_herb_to_dict(h) for h in herbs]}


@router.get("/compare")
async def compare_herbs_api(
    q: str = Query(..., description="两个药材ID，逗号分隔，如: 1,2"),
    db: Session = Depends(get_db),
):
    """对比两个药材"""
    try:
        ids = q.split(",")
        herb_id_1 = int(ids[0].strip())
        herb_id_2 = int(ids[1].strip())
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="参数格式错误，请使用: q=1,2")

    result = compare_herbs(db, herb_id_1, herb_id_2)

    if result["herb_1"] is None or result["herb_2"] is None:
        raise HTTPException(status_code=404, detail="药材不存在")

    return {
        "herb_1": _herb_to_dict(result["herb_1"]),
        "herb_2": _herb_to_dict(result["herb_2"]),
    }


@router.get("/ai-compare")
async def ai_compare_herbs_api(
    q: str = Query(..., description="两个药材ID，逗号分隔，如: 1,2"),
    db: Session = Depends(get_db),
):
    """AI 智能对比两个药材"""
    try:
        ids = q.split(",")
        herb_id_1 = int(ids[0].strip())
        herb_id_2 = int(ids[1].strip())
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="参数格式错误，请使用: q=1,2")

    result = compare_herbs(db, herb_id_1, herb_id_2)

    if result["herb_1"] is None or result["herb_2"] is None:
        raise HTTPException(status_code=404, detail="药材不存在")

    herb1 = _herb_to_dict(result["herb_1"])
    herb2 = _herb_to_dict(result["herb_2"])

    ai_result = await ai_compare_herbs(herb1, herb2)

    return {
        "herb_1": herb1,
        "herb_2": herb2,
        "ai_compare": ai_result,
    }


@router.get("/{herb_id}")
async def get_herb_detail(
    herb_id: int,
    db: Session = Depends(get_db),
):
    """获取药材详情"""
    herb = get_herb_by_id(db, herb_id)
    if herb is None:
        raise HTTPException(status_code=404, detail="药材不存在")
    return _herb_to_dict(herb)


def _herb_to_dict(herb: Herb) -> dict:
    """将药材ORM对象转为字典"""
    return {
        "id": herb.id,
        "name": herb.name,
        "aliases": herb.aliases,
        "family": herb.family,
        "source": herb.source,
        "part_used": herb.part_used,
        "nature_taste": herb.nature_taste,
        "meridian_tropism": herb.meridian_tropism,
        "efficacy": herb.efficacy,
        "indications": herb.indications,
        "usage_dosage": herb.usage_dosage,
        "contraindications": herb.contraindications,
        "appearance_color": herb.appearance_color,
        "appearance_texture": herb.appearance_texture,
        "appearance_fracture": herb.appearance_fracture,
        "appearance_odor": herb.appearance_odor,
        "authenticity_tips": herb.authenticity_tips,
        "confusable_herbs": herb.confusable_herbs,
        "processing_method": herb.processing_method,
        "storage_condition": herb.storage_condition,
        "harvesting_processing": herb.harvesting_processing,
        "image_main": herb.image_main,
        "image_microscopic": herb.image_microscopic,
        "image_processed": herb.image_processed,
        "category_part": herb.category_part,
        "category_efficacy": herb.category_efficacy,
        "created_at": herb.created_at.isoformat() if herb.created_at else None,
    }
