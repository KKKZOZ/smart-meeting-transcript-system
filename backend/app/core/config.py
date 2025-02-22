from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    应用配置类
    使用pydantic_settings进行环境变量管理
    所有配置项都可以通过环境变量覆盖
    """

    SMTP_SERVER: str
    SMTP_PORT: str
    SENDER_EMAIL: str
    SENDER_PASSWORD: str

    ALIBABA_ACCESS_KEY_ID: str
    ALIBABA_ACCESS_KEY_SECRET: str

    BAIDU_APP_ID: str
    BAIDU_APP_KEY: str

    OPENAI_API_KEY: str
    OPENAI_API_BASE: str

    SPARKAI_URL: str
    SPARKAI_APP_ID: str
    SPARKAI_API_SECRET: str
    SPARKAI_API_KEY: str
    SPARKAI_DOMAIN: str

    # 数据库连接URL
    DATABASE_URL: str  # = "mysql+pymysql://root:123456@localhost/gjrcdemo"

    # JWT加密密钥
    SECRET_KEY: str

    # JWT算法
    ALGORITHM: str = "HS256"
    # JWT令牌过期时间(分钟)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
