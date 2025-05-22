from pydantic_settings import BaseSettings # 从 pydantic-settings 导入 BaseSettings 用于加载配置
from typing import ClassVar  # 如果需要声明类变量

class Settings(BaseSettings):
    PROJECT_NAME: str = "企业库存管理信息系统" # 项目名称
    API_V1_STR: str = "/api/v1" # API 版本前缀

    # 数据库配置
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:057211397@127.0.0.1:3306/warehouse_db"

    class Config:
        case_sensitive = True # 配置项名称大小写敏感
        env_file = ".env" # 可以通过 .env 文件加载环境变量 (需要 python-dotenv 库)
        env_file_encoding = 'utf-8' # .env 文件编码
        extra = "allow"  # 允许未定义的字段

settings = Settings() 