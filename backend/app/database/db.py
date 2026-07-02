"""数据库连接与初始化模块"""
import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# 创建同步引擎（SQLite 不支持异步，使用同步引擎）
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 专用参数
    echo=settings.DEBUG,
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()


def get_db():
    """数据库会话依赖注入"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库：创建所有表 + 导入初始药材数据"""
    # 导入所有模型以便 create_all 能发现它们
    from app.models import Herb  # noqa: F401

    # 创建所有表
    Base.metadata.create_all(bind=engine)

    # 导入初始药材数据
    _import_herb_data()


def _import_herb_data():
    """从 herbs.json 导入初始药材数据"""
    from app.models.herb import Herb

    db = SessionLocal()
    try:
        # 检查是否已有数据，避免重复导入
        count = db.query(Herb).count()
        if count > 0:
            return

        # 读取 JSON 数据文件
        json_path = Path(__file__).parent / "init_data" / "herbs.json"
        if not json_path.exists():
            return

        with open(json_path, "r", encoding="utf-8") as f:
            herbs_data = json.load(f)

        # 批量插入
        for item in herbs_data:
            herb = Herb(**item)
            db.add(herb)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"导入初始药材数据失败: {e}")
    finally:
        db.close()
