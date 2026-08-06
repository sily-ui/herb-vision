"""FastAPI应用入口"""
import os
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.db import init_db
from app.routers import identify, knowledge, user, feedback
from app.utils.auth import get_current_user

# 创建FastAPI应用
app = FastAPI(
    title="AI中药鉴定系统",
    description="基于AI大模型的中药鉴定与知识库系统",
    version="1.0.0",
)

# 配置CORS（开发阶段允许所有源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有路由
app.include_router(identify.router)
app.include_router(knowledge.router)
app.include_router(user.router)
app.include_router(feedback.router)


@app.on_event("startup")
async def startup_event():
    """应用启动事件：初始化数据库"""
    init_db()


# 挂载静态文件目录
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 通用上传目录
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """通用文件上传接口（需登录）"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")

    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return {"path": f"/static/uploads/{file_name}"}


@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "AI中药鉴定系统API服务运行中", "version": "1.0.0"}
