"""知识库服务模块"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.herb import Herb


def get_herbs(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    category_part: Optional[str] = None,
    category_efficacy: Optional[str] = None,
    keyword: Optional[str] = None,
) -> dict:
    """获取药材列表（分页+筛选）

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        category_part: 按部位分类筛选
        category_efficacy: 按功效分类筛选
        keyword: 关键词搜索

    Returns:
        包含 total、page、page_size、items 的字典
    """
    query = db.query(Herb)

    # 按部位分类筛选
    if category_part:
        query = query.filter(Herb.category_part == category_part)

    # 按功效分类筛选
    if category_efficacy:
        query = query.filter(Herb.category_efficacy == category_efficacy)

    # 关键词搜索（名称或别名）
    if keyword:
        query = query.filter(
            (Herb.name.contains(keyword)) | (Herb.aliases.contains(keyword))
        )

    # 计算总数
    total = query.count()

    # 分页
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


def get_herb_by_id(db: Session, herb_id: int) -> Optional[Herb]:
    """根据ID获取药材详情

    Args:
        db: 数据库会话
        herb_id: 药材ID

    Returns:
        药材对象或None
    """
    return db.query(Herb).filter(Herb.id == herb_id).first()


def search_herbs(db: Session, keyword: str) -> list:
    """关键词搜索药材（名称/别名/功效）

    Args:
        db: 数据库会话
        keyword: 搜索关键词

    Returns:
        匹配的药材列表
    """
    return (
        db.query(Herb)
        .filter(
            (Herb.name.contains(keyword))
            | (Herb.aliases.contains(keyword))
            | (Herb.efficacy.contains(keyword))
        )
        .all()
    )


def compare_herbs(db: Session, herb_id_1: int, herb_id_2: int) -> dict:
    """对比两个药材

    Args:
        db: 数据库会话
        herb_id_1: 第一个药材ID
        herb_id_2: 第二个药材ID

    Returns:
        包含两个药材信息的对比字典
    """
    herb_1 = db.query(Herb).filter(Herb.id == herb_id_1).first()
    herb_2 = db.query(Herb).filter(Herb.id == herb_id_2).first()

    return {
        "herb_1": herb_1,
        "herb_2": herb_2,
    }
