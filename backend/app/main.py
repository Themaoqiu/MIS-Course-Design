from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 导入 CORS 中间件，用于处理跨域请求

from app.routers.api_v1 import api_router # 导入聚合后的 API 路由器
from app.core.config import settings # 导入应用配置
from app.db.database import engine, Base # 导入数据库引擎和模型基类

# ---- 数据库表创建 ----
# 在应用启动时创建所有在 Base 中定义的表 (如果它们尚不存在)
# 注意：对于生产环境，强烈建议使用数据库迁移工具如 Alembic 来管理数据库表结构的变更。
Base.metadata.create_all(bind=engine)
# 你可以在项目根目录下运行 `alembic init alembic` 初始化 Alembic，然后配置并使用它。
# ----

app = FastAPI(
    title=settings.PROJECT_NAME, # API 文档的标题
    openapi_url=f"{settings.API_V1_STR}/openapi.json", # OpenAPI schema 的路径
    docs_url=f"{settings.API_V1_STR}/docs", # Swagger UI 文档路径
    redoc_url=f"{settings.API_V1_STR}/redoc" # ReDoc 文档路径
)

# ---- CORS (Cross-Origin Resource Sharing) 中间件配置 ----
# 允许来自指定源 (你的 Vue 前端应用) 的跨域请求
# 在开发环境中，Vue CLI (通常是 :8080) 或 Vite (通常是 :5173 或 :3000) 服务与 FastAPI 后端服务在不同端口上，
# 因此需要配置 CORS。
origins = [
    "http://localhost:8080", # Vue CLI 默认开发服务器地址
    "http://localhost:5173", # Vite 默认开发服务器地址 (Vue 3)
    "http://localhost:3000", # Vite 另一个常见端口或 Next.js/Nuxt.js
    # 如果你的前端部署在其他地址，也需要添加进来
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允许的源列表
    allow_credentials=True, # 是否允许携带 cookies
    allow_methods=["*"], # 允许所有 HTTP 方法 (GET, POST, PUT, DELETE 等)
    allow_headers=["*"], # 允许所有 HTTP 请求头
)
# ----

# 将聚合后的 API 路由器包含到主应用中，并设置统一的 API 版本前缀
app.include_router(api_router, prefix=settings.API_V1_STR)

# 一个简单的根路径端点，用于测试 API 是否正常运行
@app.get("/", tags=["Root"])
async def root():
    return {"message": f"欢迎访问 {settings.PROJECT_NAME}!"}

# 运行 FastAPI 应用的命令 (在项目根目录下，假设 main.py 在 app 文件夹内):
# uvicorn app.main:app --reload
# --reload 参数可以在代码变更时自动重启服务，非常适合开发环境。