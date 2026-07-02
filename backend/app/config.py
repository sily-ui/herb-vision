"""应用配置模块，使用 pydantic-settings 加载环境变量"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类，从 .env 文件加载所有配置项"""

    # 数据库
    DATABASE_URL: str = "sqlite:///./medicine.db"

    # 微信小程序
    WX_APPID: str = ""
    WX_SECRET: str = ""

    # AI大模型（智谱GLM）
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL: str = "glm-4v"

    # JWT
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# 全局配置实例
settings = Settings()
