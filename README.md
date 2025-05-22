# 🏭 企业库存管理信息系统 (Enterprise Inventory Management System)

本项目是一个基于 FastAPI 和 Vue.js 构建的企业库存管理信息系统, 作为上海电力大学信息管理与信息系统的管理信息系统课程设计, 顺便练习 FastAPI 和 Vue

## 📖 项目简介

该系统允许用户管理企业或组织的物资信息，跟踪每种物资的当前库存水平，记录详细的出入库流水，并提供一个总览仪表盘来快速了解整体库存状况。

## 🛠️ 主要技术栈

### 🔧 后端 (Backend)

* **框架**: FastAPI - 一个现代、快速（高性能）的 Python web 框架，用于构建 API⚡
* **数据库**: MySQL (通过 `pymysql` 连接)🗃️
* **ORM**: SQLAlchemy - 用于 Python 的 SQL 工具包和对象关系映射器🧩
* **数据验证**: Pydantic - 基于 Python 类型提示的数据验证和设置管理✅
* **ASGI 服务器**: Uvicorn - 用于 FastAPI 的 ASGI 服务器🚀

### 🎨前端 (Frontend)

* **框架**: Vue.js (版本 3) 🌟
* **构建工具**: Vite ⚡
* **UI 组件库**: shadcn-vue - 基于 Tailwind CSS 和 Radix Vue 的可复用组件 🎨。
* **CSS 框架**: Tailwind CSS 🎨
* **状态管理**: (根据需要，例如 Pinia) 🧠
* **路由**: Vue Router 🗺️
* **HTTP 客户端**: Axios 🌐
* **通知**: vue-sonner 🔔

## ✨ 功能特性

* **📊 总览仪表盘**
    * 显示物资种类总数
    * 显示当前库存总量
    * 显示库存预警数量 ⚠️
* **📦 物资管理**
    * 创建新物资（编码、名称、型号、单位、供应商、备注、是否启用）➕
    * 查看物资列表（支持分页、按编码或名称搜索）🔍
    * 查看单个物资详情 👀
    * 更新物资信息 ✏️
    * 删除物资（有业务逻辑检查，如库存是否为零、是否有出入库记录）❌
* **📉 库存查看**
    * 查看所有物资的当前库存余額列表（支持分页）📋
    * 根据物资ID查看特定物资的库存余額 🔎
    * (管理员) 手动调整物资的最低/最高库存水平 ⚙️
* **📥 入库管理**
    * 创建新的入库记录（关联物资、数量、入库单号、备注）📦
    * 创建入库记录时自动更新相应物资的库存余額 🔄
    * 查看入库记录列表（支持分页、按物资ID和时间范围过滤）📜
    * 查看单个入库记录详情 👀
* **📤 出库管理**
    * 创建新的出库记录（关联物资、数量、出库单号、领用人、备注）📤
    * 创建出库记录时检查库存是否充足并自动更新库存余額 ✅
    * 查看出库记录列表（支持分页、按物资ID和时间范围过滤）📜
    * 查看单个出库记录详情 👀

## 项目结构 (后端)

```tree
backend/
├── app/                  # FastAPI 应用核心代码
│   ├── core/             # 配置 (config.py)
│   ├── crud/             # CRUD 操作 (数据库交互逻辑)
│   ├── db/               # 数据库设置 (database.py)
│   ├── models/           # SQLAlchemy ORM 模型
│   ├── routers/          # API 路由定义
│   ├── schemas/          # Pydantic 数据模型 (请求/响应体)
│   ├── __init__.py
│   └── main.py           # FastAPI 应用入口
├── .env.example          # 环境变量示例文件
├── requirements.txt      # Python 依赖
└── uvicorn_runner.py     # (可选) 或直接通过 uvicorn 命令运行
```
## 安装与运行

### 后端

1.  **环境准备**:
    * 安装 Python (推荐 3.9+)。
    * 安装 MySQL 数据库并确保其正在运行。
    * 创建一个数据库 (例如 `warehouse_db`)。

2.  **克隆或下载项目到 `backend` 目录。**

3.  **创建并激活 Python 虚拟环境**:
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

4.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```
    (你需要根据项目实际使用的库生成 `requirements.txt` 文件，例如通过 `pip freeze > requirements.txt`)

5.  **配置环境变量**:
    * 复制 `.env.example` (如果提供) 为 `.env` 文件。
    * 修改 `.env` 文件中的数据库连接字符串 `SQLALCHEMY_DATABASE_URL` 以匹配你的 MySQL 设置。例如：
        ```env
        SQLALCHEMY_DATABASE_URL=mysql+pymysql://user:password@host:port/warehouse_db
        ```

6.  **运行数据库表结构创建 (首次运行或模型更新后)**:
    FastAPI 应用启动时会尝试创建表 (通过 `Base.metadata.create_all(bind=engine)` 在 `app/main.py` 中)。
    对于生产环境或更复杂的 schema 变更，推荐使用 Alembic进行数据库迁移。

7.  **启动 FastAPI 应用**:
    在 `backend` 目录下运行：
    ```bash
    uvicorn app.main:app --reload
    ```
    服务器通常会运行在 `http://127.0.0.1:8000`。

### 前端

1.  **环境准备**:
    * 安装 Node.js (推荐 LTS 版本) 和 npm (或 pnpm/yarn)。

2.  **克隆或下载项目到 `frontend` 目录**
    ```bash
    cd frontend/MIS
    ```

3.  **安装依赖**:
    ```bash
    npm install
    ```

4.  **配置环境变量 (如果需要)**:
    在 `frontend/MIS/` 目录下创建 `.env.development` 文件，并设置后端 API 的基础 URL：
    ```env
    VITE_API_BASE_URL=http://localhost:8000/api/v1
    ```

5.  **运行开发服务器**:
    ```bash
    npm run dev
    ```
    前端应用通常会运行在 `http://localhost:5173` (或其他 Vite 默认端口)。

## API 文档

当后端 FastAPI 应用成功运行后，可以通过以下路径访问自动生成的 API 文档：

* **Swagger UI**: `http://127.0.0.1:8000/api/v1/docs`
* **ReDoc**: `http://127.0.0.1:8000/api/v1/redoc`

## ⚠️ 注意事项

* 确保后端服务先于前端服务启动，或者前端能够正确处理后端服务暂时不可用的情况。
* 根据实际部署环境，可能需要调整 CORS 配置、数据库连接字符串等。
* 对于生产部署，不建议使用 `--reload` 参数运行 Uvicorn，并应考虑使用 Gunicorn + Uvicorn workers 或其他生产级 ASGI 服务器配置。

---

