from fastapi import FastAPI
from app.api.endpoints.auth.router import router as auth_router

app = FastAPI(
    title="FastAPI Auth Demo",
    description="FastAPI用户认证示例项目",
    version="1.0.0"
)

# 注册认证路由
app.include_router(auth_router, prefix="/api", tags=["认证"]) 