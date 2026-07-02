"""药材数据模型"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database.db import Base


class Herb(Base):
    """药材信息表"""

    __tablename__ = "herbs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="药典标准名称")
    aliases = Column(String(200), comment="别名，逗号分隔")
    family = Column(String(50), comment="科属")
    source = Column(String(200), comment="来源")
    part_used = Column(String(50), comment="药用部位")
    nature_taste = Column(String(100), comment="性味")
    meridian_tropism = Column(String(100), comment="归经")
    efficacy = Column(Text, comment="功效")
    indications = Column(Text, comment="主治")
    usage_dosage = Column(String(200), comment="用法用量")
    contraindications = Column(Text, comment="禁忌")
    appearance_color = Column(String(100), comment="颜色")
    appearance_texture = Column(String(100), comment="质地")
    appearance_fracture = Column(String(100), comment="断面")
    appearance_odor = Column(String(100), comment="气味")
    authenticity_tips = Column(Text, comment="真伪鉴别要点")
    confusable_herbs = Column(String(200), comment="易混淆药材，逗号分隔")
    processing_method = Column(Text, comment="炮制方法")
    storage_condition = Column(String(200), comment="储存条件")
    harvesting_processing = Column(Text, comment="采收加工")
    image_main = Column(String(200), comment="主图路径")
    image_microscopic = Column(String(200), comment="显微图路径")
    image_processed = Column(String(200), comment="炮制图路径")
    category_part = Column(String(50), comment="按部位分类")
    category_efficacy = Column(String(50), comment="按功效分类")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
