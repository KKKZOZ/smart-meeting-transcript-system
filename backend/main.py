from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.auth.router import router as auth_router
from app.api.endpoints.notification.router import router as notification_router
from app.api.endpoints.demo.router import router as demo_router
from app.api.endpoints.transcription.router import router as transcription_router
from app.api.endpoints.record.router import router as record_router
from app.api.endpoints.summaries.router import router as summaries_router
from app.api.endpoints.tasks.router import router as tasks_router
from app.middleware.logging import log_request_middleware

app = FastAPI(
    title="Smart Meeting Transcript System",
    description="",
    version="0.1.0",
    openapi_extra={"security": [{"OAuth2PasswordBearer": []}]},
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
app.include_router(transcription_router, prefix="/api", tags=["创建会议"])
app.include_router(record_router, prefix="/api", tags=["会议记录"])
app.include_router(summaries_router, prefix="/api", tags=["生成摘要"])
app.include_router(tasks_router, prefix="/api", tags=["待办事项"])
