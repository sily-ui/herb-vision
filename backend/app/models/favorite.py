"""用户收藏模型"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint

from app.database.db import Base


class Favorite(Base):
    """用户收藏的药材"""

    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "herb_id", name="uix_user_herb"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    herb_id = Column(Integer, ForeignKey("herbs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
