from fastapi import Request
from logging import handlers, Formatter, getLogger, INFO
import time
import json

# 配置日志处理器，确保正确处理中文
handler = handlers.RotatingFileHandler(
    filename="app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8",  # 明确指定 UTF-8 编码
)

# 配置日志格式
formatter = Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

# 配置根日志记录器
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(handler)

# 同时输出到控制台
# console_handler = StreamHandler(sys.stdout)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)


async def log_request_middleware(request: Request, call_next):
    """记录请求信息的中间件"""
    start_time = time.time()

    # 记录请求信息
    logger.info("=" * 50)
    logger.info(f"请求路径: {request.method} {request.url}")
    logger.info(f"客户端地址: {request.client.host}")

    important_headers = [
        "authorization",
        "content-type",
        "accept",
    ]

    headers_to_log = {}
    for header_name in important_headers:
        if header_name in request.headers:
            headers_to_log[header_name] = request.headers[header_name]
    logger.info(f"请求头: {headers_to_log}")

    # 如果是POST请求，记录请求体
    if request.method == "POST":
        try:
            # 克隆请求体
            body_bytes = await request.body()

            try:
                body_json = json.loads(body_bytes.decode("utf-8"))
                logger.info(f"请求体 (JSON): {body_json}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                content_type = request.headers.get("content-type", "")
                if "multipart/form-data" in content_type:
                    logger.info(
                        "请求体 (multipart/form-data): 包含文件或其他二进制数据，已省略日志记录"
                    )
                elif "application/x-www-form-urlencoded" in content_type:
                    logger.info(
                        f"请求体 (application/x-www-form-urlencoded): {body_bytes.decode('utf-8', errors='replace')}"
                    )

                else:
                    logger.info(
                        f"请求体 (二进制): 长度 {len(body_bytes)} 字节, 无法解码为文本"
                    )

            # 创建一个新的 BodyCache 对象
            async def receive():
                return {"type": "http.request", "body": body_bytes, "more_body": False}

            request._receive = receive
        except Exception as e:
            logger.error(f"读取请求体失败: {str(e)}")

    # 处理请求
    response = await call_next(request)

    # 记录处理时间
    process_time = time.time() - start_time
    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"处理时间: {process_time:.2f}秒")
    logger.info("=" * 50)

    return response
