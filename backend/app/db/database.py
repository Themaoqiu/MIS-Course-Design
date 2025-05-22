from sqlalchemy import create_engine # SQLAlchemy 的核心组件，用于连接数据库
from sqlalchemy.ext.declarative import declarative_base # 用于定义数据模型的基类
from sqlalchemy.orm import sessionmaker # 用于创建数据库会話
from app.core.config import settings # 导入应用配置

# 创建数据库引擎
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL) 
# 创建数据库会话
# autocommit=False: 事务自动提交关闭，需要手动 commit
# autoflush=False: 在查询前自动将当前会话中的所有挂起更改刷新到数据库关闭，通常与 autocommit=False 一起使用
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据模型基类
# 所有的数据模型类都将继承自这个 Base 类
Base = declarative_base()

def get_db():
    db = SessionLocal() # 创建一个新的数据库会话
    try:
        yield db # 将会话提供给请求处理函数
    finally:
        db.close() # 请求处理完毕后，关闭会话，释放资源
