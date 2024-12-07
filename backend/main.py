from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.auth.router import router as auth_router
from app.api.endpoints.notification.router import router as notification_router
from app.api.endpoints.demo.router import router as demo_router
from app.middleware.logging import log_request_middleware

app = FastAPI(
    title="FastAPI Auth Demo", description="FastAPI用户认证示例项目", version="1.0.0"
)

app.middleware("http")(log_request_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)

# 注册认证路由
app.include_router(auth_router, prefix="/api", tags=["认证"])
app.include_router(notification_router, prefix="/api", tags=["通知"])
app.include_router(demo_router, prefix="/api", tags=["演示"])
