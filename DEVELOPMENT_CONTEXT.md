# 开发上下文记录

> 本文件记录了从零搭建 my-backend 项目的完整过程和当前进度，
> 用于在不同设备/会话间同步开发上下文。

---

## 项目基本信息

- **项目名称：** my-backend（MiroFish 后端的独立学习项目）
- **仓库地址：** git@github.com:Lemon-J/miro.git
- **本地路径：** d:\jiaok\MiroFish\my-backend
- **参考项目：** d:\jiaok\MiroFish\MiroFish-Rep（MiroFish 原始项目）
- **技术栈：** Python 3.11+ / Flask 3.x / OpenAI SDK / Zep Cloud
- **PRD 文档：** MiroFish-Rep/PRD_BACKEND.md

---

## 当前进度

### 已完成

| 步骤 | 内容 | 状态 |
|------|------|------|
| 1.1 | 创建目录结构 + requirements.txt | ✅ |
| 1.2 | 创建 .env / .env.example + config.py | ✅ |
| 1.3 | 创建 utils/logger.py（日志工具） | ✅ |
| 1.4 | 创建 app/__init__.py（Flask 工厂） | ✅ |
| 1.5 | 创建 run.py（启动入口） | ✅ |
| 1.6 | 创建 app/api/test.py（测试蓝图，含 /ping /config /llm_chat） | ✅ |
| 1.7 | Git 初始化 + 推送到 GitHub | ✅ |

### 当前目录结构

```
my-backend/
├── .env                # 本地配置（已 gitignore）
├── .env.example        # 配置模板
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── run.py              # 启动入口：python run.py
├── uploads/            # 运行时数据
├── logs/               # 日志文件
└── app/
    ├── __init__.py     # Flask 工厂函数 create_app()
    ├── config.py       # Config 类，从 .env 读配置
    ├── api/
    │   ├── __init__.py # 导出蓝图
    │   └── test.py     # 测试蓝图：/api/test/ping, /api/test/config, /api/test/llm_chat
    ├── models/         # 数据层（待写）
    ├── services/       # 业务逻辑层（待写）
    └── utils/
        ├── __init__.py
        ├── logger.py   # 日志：文件+控制台双输出
        └── llm_client.py # LLM 调用封装（用户已写）
```

### .env 配置

```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
LLM_API_KEY=sk-xxxx           # 用户已配置 DeepSeek
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_NAME=deepseek-v4-pro
ZEP_API_KEY=                  # 未配置
```

---

## 下一步：第 2 步 工具层

继续编写 `app/utils/` 下的工具模块，按以下顺序：

### 2a. utils/llm_client.py — ✅ 用户已写好

包含 `LLMClient` 类，提供 `chat()` 和 `chat_json()` 方法。

### 2b. utils/file_parser.py — 待写

**职责：** 从 PDF/MD/TXT 文件提取纯文本
**参考：** MiroFish-Rep/backend/app/utils/file_parser.py
**依赖：** PyMuPDF (fitz), charset_normalizer, chardet
**核心内容：**
- `FileParser.extract_text(file_path)` — 根据扩展名分派
- `FileParser.extract_from_multiple(file_paths)` — 多文件合并
- `split_text_into_chunks(text, chunk_size, overlap)` — 文本分块
- `_read_text_with_fallback(file_path)` — 编码检测 fallback 链

### 2c. utils/locale.py — 可选，后续再加

---

## 第 3 步：数据层（models/）

### 3a. models/task.py

**职责：** 异步任务状态管理
**参考：** MiroFish-Rep/backend/app/models/task.py
**核心内容：**
- `TaskStatus` 枚举：PENDING / PROCESSING / COMPLETED / FAILED
- `Task` dataclass：task_id, task_type, status, progress, message, result, error
- `TaskManager` 单例：create_task, get_task, update_task, complete_task, fail_task

### 3b. models/project.py

**职责：** 项目元数据持久化（JSON 文件）
**参考：** MiroFish-Rep/backend/app/models/project.py
**核心内容：**
- `ProjectStatus` 枚举
- `Project` dataclass + to_dict / from_dict
- `ProjectManager` 纯类方法：create, save, get, list, delete

---

## 第 4 步：服务层（services/）

按业务流程顺序：

| 顺序 | 文件 | 功能 | 依赖 |
|------|------|------|------|
| 4a | text_processor.py | 文本处理 | utils/file_parser |
| 4b | ontology_generator.py | LLM 生成本体 | utils/llm_client |
| 4c | graph_builder.py | Zep 图谱构建 | zep_cloud, models/task |
| 4d | zep_entity_reader.py | 实体读取过滤 | zep_cloud |
| 4e | oasis_profile_generator.py | Agent 人设生成 | LLM + Zep |
| 4f | simulation_config_generator.py | 模拟配置生成 | LLM |
| 4g | simulation_manager.py | 模拟状态管理 | 上面几个 service |
| 4h | simulation_ipc.py | 进程间通信 | 纯标准库 |
| 4i | simulation_runner.py | 模拟进程运行 | subprocess |
| 4j | zep_tools.py | Zep 检索工具 | zep_cloud + LLM |
| 4k | report_agent.py | ReACT 报告 Agent | LLM + zep_tools |
| 4l | zep_graph_memory_updater.py | 图谱更新（可选） | zep_cloud |

---

## 第 5 步：API 路由层（api/）

| 文件 | 前缀 | 主要接口 |
|------|------|---------|
| graph.py | /api/graph | POST /ontology/generate, POST /build, GET /project/list |
| simulation.py | /api/simulation | POST /create, POST /prepare, POST /start, POST /stop |
| report.py | /api/report | POST /generate, POST /chat, GET /<id> |

---

## 关键设计模式

| 模式 | 用在哪 | 说明 |
|------|--------|------|
| 应用工厂 | create_app() | 方便测试和多实例 |
| 蓝图分组 | api/ | 按功能模块组织路由 |
| 单例模式 | TaskManager | 全局唯一，线程安全 |
| 后台线程 | 所有异步服务 | threading.Thread(daemon=True) |
| 异步任务 | 图谱/模拟/报告 | 立即返回 task_id，前端轮询 |
| 文件 IPC | Flask ↔ 子进程 | JSON 文件命令/响应 |
| ReACT Agent | ReportAgent | 思考→行动→观察循环 |

---

## 学习笔记

### Python 基础已覆盖
- 字典、列表、f-string、解包、列表推导式
- 装饰器（@retry_with_backoff）、生成器（yield）
- dataclass、枚举、classmethod / staticmethod
- 文件 I/O、JSON、异常处理
- 模块、包、import 机制
- 并发基础（threading、Lock、ThreadPoolExecutor、subprocess、Queue）— 跳过，实战时深入
- Flask 路由、蓝图、请求/响应、CORS
- LLM 调用封装（OpenAI SDK）

### 用户特点
- 有其他编程语言基础（非零基础）
- 偏好边讲边练的学习方式
- 使用 DeepSeek API（非 OpenAI）
- 使用 Windows 环境

---

## 参考资料

- **PRD 文档：** MiroFish-Rep/PRD_BACKEND.md
- **MiroFish 源码：** MiroFish-Rep/backend/app/
- **学习路线：** MiroFish-Rep/BACKEND_LEARNING_ROADMAP.md

---

*最后更新：2026-05-08*
