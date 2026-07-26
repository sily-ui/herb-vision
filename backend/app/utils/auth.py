"""JWT认证工具模块"""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.config import settings
from app.database.db import SessionLocal

# Bearer Token 方式
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def create_access_token(data: dict) -> str:
    """创建JWT访问令牌

    Args:
        data: 要编码的数据，通常包含 {"sub": user_id}

    Returns:
        JWT令牌字符串
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    """验证JWT令牌

    Args:
        token: JWT令牌字符串

    Returns:
        解码后的payload字典

    Raises:
        HTTPException: 令牌无效或过期
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """获取当前登录用户的依赖注入

    从请求头中提取Bearer Token，验证并返回用户信息
    """
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
        )

    # 从数据库查询用户
    from app.models.user import User

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
            )
        return user
    finally:
        db.close()


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(optional_security),
):
    """可选认证，未登录返回 None"""
    if credentials is None:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
