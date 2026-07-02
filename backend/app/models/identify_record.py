"""识别记录数据模型"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey

from app.database.db import Base


class IdentifyRecord(Base):
    """识别记录表"""

    __tablename__ = "identify_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    image_path = Column(String(500), comment="上传图片路径")
    herb_name = Column(String(50), comment="识别出的药材名称")
    confidence = Column(String(20), comment="置信度")
    result_json = Column(Text, comment="识别结果JSON")
    is_favorited = Column(Boolean, default=False, comment="是否收藏")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
