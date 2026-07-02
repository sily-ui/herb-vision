"""FastAPI应用入口"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.db import init_db
from app.routers import identify, knowledge, user, feedback

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


@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "AI中药鉴定系统API服务运行中", "version": "1.0.0"}
