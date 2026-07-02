"""反馈数据模型"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from app.database.db import Base


class Feedback(Base):
    """用户反馈表"""

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    herb_id = Column(Integer, ForeignKey("herbs.id"), comment="药材ID")
    feedback_type = Column(String(20), comment="反馈类型: identify_error/data_missing/other")
    content = Column(Text, comment="反馈内容")
    image_path = Column(String(500), comment="反馈图片路径")
    status = Column(String(20), default="pending", comment="状态: pending/reviewed/resolved")
    admin_reply = Column(Text, comment="管理员回复")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
