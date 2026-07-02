# Herb Vision · 中草药智能识别小程序

> 基于 uni-app + FastAPI 的中草药 AI 智能识别与知识库系统

Herb Vision 是一款面向中医药教学、临床参考与大众科普的中草药智能识别微信小程序。用户通过拍照或上传图片，由多模态大模型（阶跃星辰 Step 3.7 Flash）进行识别，并返回符合《中国药典》规范的药材结构化信息；同时配套药材知识库、相似药材对比、个性化学习与用户反馈等功能，形成"识别 — 学习 — 对比 — 反馈"的完整闭环。

---

## 一、项目背景与意义

中药材种类繁多、外形相近，传统鉴定高度依赖专家经验，存在以下痛点：

1. **鉴定门槛高**：基层从业者、学生难以快速准确识别药材；
2. **易混淆药材多**：如人参与西洋参、川贝与平贝等，误用易引发安全问题；
3. **知识分散**：药典内容专业、检索不便，缺乏移动端便捷工具；
4. **学习反馈缺失**：传统学习无法记录个人识别历史，难以复盘提升。

本项目借助多模态大模型的视觉理解能力，结合结构化知识库，为用户提供随时可用的"AI 中药鉴定助手"，旨在降低中药鉴定门槛、辅助教学与科普、并通过用户反馈持续优化识别质量。

---

## 二、功能特性

### 核心功能
- 📷 **AI 拍照识药**：上传中草药图片，调用阶跃星辰 Step 3.7 Flash 多模态模型识别，返回药典标准名称、来源、性味归经、功效主治、用法用量、禁忌、外观特征、真伪鉴别要点、易混淆药材等结构化结果；
- 🔍 **智能置信度**：识别结果附带高/中/低置信度标注，低置信度时提示用户复核；
- 🗂️ **药材知识库**：内置药材数据库，支持按部位/功效分类筛选、关键词搜索、分页浏览；
- ⚖️ **相似药材对比**：选择两种药材并排对比性味、功效、外观、鉴别要点等关键字段；
- 📚 **个性化学习**：自动记录用户的识别历史与收藏，便于复习复盘；
- 💬 **用户反馈**：支持识别纠错、数据缺失、其他问题三类反馈，形成数据闭环。

### 系统特性
- 前后端分离架构，RESTful API 设计；
- JWT 鉴权 + 微信小程序登录（code 换 openid）；
- 异步调用大模型 API（httpx），10MB 图片大小限制；
- SQLAlchemy ORM + SQLite（可平滑切换 MySQL/PostgreSQL）；
- 完整的 Pydantic 请求/响应模型校验。
- 阶跃星辰 Step 3.7 Flash 接口兼容 OpenAI 格式，便于后续替换其他大模型；

---

## 三、技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | uni-app (Vue 3) | 一次开发，多端运行，主要面向微信小程序 |
| 前端状态管理 | Pinia | 用户状态、药材状态管理 |
| 前端构建 | Vite | 快速冷启动与 HMR |
| 后端 | FastAPI | 高性能异步 Web 框架，自动生成 OpenAPI 文档 |
| ORM | SQLAlchemy 2.0 | 数据库访问层 |
| 数据库 | SQLite | 开发环境默认，可切换 |
| 鉴权 | JWT (python-jose) + 微信登录 | 无状态令牌鉴权 |
| 密码 | passlib[bcrypt] | 密码哈希（预留） |
| AI 模型 | 阶跃星辰 Step 3.7 Flash | 多模态图像识别 + 文本模糊搜索（OpenAI 兼容接口） |
| HTTP 客户端 | httpx | 异步调用第三方 API |
| 图片处理 | Pillow | 图片校验与处理 |

---

## 四、系统架构

```
┌─────────────────────────┐        ┌──────────────────────────────────┐
│   微信小程序 (uni-app)   │        │         FastAPI 后端              │
│                         │        │                                  │
│  ┌───────────────────┐  │  HTTP  │  ┌────────────┐  ┌────────────┐  │
│  │  识别  知识库     │  │ ──────▶│  │  路由层    │─▶│  服务层    │  │
│  │  对比  学习       │  │  JSON  │  │  routers/  │  │  services/ │  │
│  │  反馈  我的       │  │ ◀──────│  └────────────┘  └─────┬──────┘  │
│  └───────────────────┘  │        │                        │         │
│         Pinia 状态管理  │        │  ┌────────────┐  ┌─────▼──────┐  │
└─────────────────────────┘        │  │  SQLAlchemy│  │  阶跃星辰   │  │
                                   │  │  ORM       │  │  Step 3.7   │  │
                                   │  └─────┬──────┘  └────────────┘  │
                                   │        │                         │
                                   │  ┌─────▼──────┐                  │
                                   │  │  SQLite DB │                  │
                                   │  └────────────┘                  │
                                   └──────────────────────────────────┘
```

---

## 五、目录结构

```
herb-vision/
├── backend/                       # 后端 FastAPI 服务
│   ├── app/
│   │   ├── main.py                # 应用入口、CORS、路由注册
│   │   ├── config.py              # 配置加载（pydantic-settings）
│   │   ├── database/              # 数据库连接与会话
│   │   ├── models/                # ORM 模型
│   │   │   ├── user.py            # 用户表
│   │   │   ├── herb.py            # 药材知识库表
│   │   │   ├── identify_record.py # 识别记录表
│   │   │   └── feedback.py        # 用户反馈表
│   │   ├── routers/               # API 路由
│   │   │   ├── user.py            # 登录/资料/记录/收藏
│   │   │   ├── identify.py        # 图片识别
│   │   │   ├── knowledge.py       # 知识库查询/搜索/对比
│   │   │   └── feedback.py        # 反馈提交与管理
│   │   ├── services/              # 业务服务层
│   │   │   ├── ai_service.py      # 阶跃星辰大模型调用（识别/模糊搜索）
│   │   │   └── knowledge_service.py# 知识库业务逻辑
│   │   └── utils/                 # 工具（JWT 鉴权等）
│   ├── requirements.txt
│   ├── .env.example               # 环境变量模板
│   └── ...
│
├── frontend/                      # 前端 uni-app 小程序
│   ├── src/
│   │   ├── pages/                 # 页面
│   │   │   ├── identify/          # 拍照识别 + 结果展示
│   │   │   ├── knowledge/         # 知识库列表/详情/搜索
│   │   │   ├── compare/           # 药材对比
│   │   │   ├── learn/             # 学习/收藏
│   │   │   ├── feedback/          # 用户反馈
│   │   │   ├── mine/              # 个人中心
│   │   │   └── index/             # 首页
│   │   ├── api/                   # 接口封装
│   │   ├── store/                 # Pinia 状态管理
│   │   ├── components/            # 公共组件
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 六、数据库设计

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `users` | 用户表 | id, openid, nickname, avatar_url, phone, created_at |
| `herbs` | 药材知识库 | id, name, aliases, family, source, part_used, nature_taste, meridian_tropism, efficacy, indications, usage_dosage, contraindications, appearance_*, authenticity_tips, confusable_herbs, category_part, category_efficacy ... |
| `identify_records` | 识别记录 | id, user_id, image_path, herb_name, confidence, result_json, is_favorited, created_at |
| `feedbacks` | 用户反馈 | id, user_id, herb_id, feedback_type, content, image_path, status, admin_reply, created_at |

---

## 七、核心 API 接口

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/api/auth/wx-login` | 微信小程序登录 |
| GET  | `/api/user/profile` | 获取用户信息 |
| PUT  | `/api/user/profile` | 更新用户信息 |
| GET  | `/api/user/records` | 识别记录列表（分页） |
| DELETE | `/api/user/records/{id}` | 删除识别记录 |
| GET/POST/DELETE | `/api/user/favorites` | 收藏管理 |
| POST | `/api/identify` | 上传图片识别中药 |
| GET  | `/api/herbs` | 药材列表（分页+筛选） |
| GET  | `/api/herbs/search` | 关键词搜索药材 |
| GET  | `/api/herbs/compare` | 对比两种药材 |
| GET  | `/api/herbs/{id}` | 药材详情 |
| POST | `/api/feedback` | 提交反馈 |
| GET  | `/api/feedback` | 反馈列表（管理端） |

启动后端后访问 `http://localhost:8000/docs` 可查看完整的 Swagger 自动文档。

---

## 八、AI 识别流程

1. 用户在小程序端拍摄或选择中草药图片；
2. 前端将图片通过 `multipart/form-data` 上传至 `/api/identify`；
3. 后端校验文件类型与大小（≤10MB），将图片保存至 `uploads/identify/`；
4. 后端将图片转 base64，构造阶跃星辰 Step 3.7 Flash 多模态请求，附带《中国药典》标准的结构化提示词；
5. 大模型返回 JSON 结构化识别结果（名称、性味、功效、鉴别要点、易混淆药材、置信度等）；
6. 后端将结果写入 `identify_records` 表，并返回给前端展示；
7. 用户可对结果进行收藏、反馈纠错，形成数据闭环。

---

## 九、快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/sily-ui/herb-vision.git
cd herb-vision
```

### 2. 后端启动
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env          # Windows
# cp .env.example .env          # macOS/Linux
# 填入微信 appid/secret 与阶跃星辰 API_KEY

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
访问 `http://localhost:8000/docs` 查看 API 文档。

### 3. 前端启动
```bash
cd frontend
npm install
npm run dev:mp-weixin           # 微信小程序开发模式
```
使用 **微信开发者工具** 导入 `frontend/dist/dev/mp-weixin` 目录即可预览。

---

## 十、环境变量说明

见 `backend/.env.example`：

| 变量 | 说明 |
|------|------|
| `DATABASE_URL` | 数据库连接字符串 |
| `WX_APPID` / `WX_SECRET` | 微信小程序凭据 |
| `STEP_API_KEY` | 阶跃星辰平台 API Key |
| `STEP_MODEL` | 多模态模型名称（默认 step-3.7-flash） |
| `STEP_API_URL` | 阶跃星辰接口地址（OpenAI 兼容） |
| `JWT_SECRET` | JWT 签名密钥（请务必修改） |
| `JWT_EXPIRE_MINUTES` | 令牌有效期（默认 1440 分钟） |
| `HOST` / `PORT` / `DEBUG` | 服务监听配置 |

---

## 十一、项目亮点（开题参考）

1. **多模态大模型落地**：将阶跃星辰 Step 3.7 Flash 视觉大模型应用于中医药垂直领域，输出符合药典规范的结构化结果，而非通用图像描述；
2. **结构化提示词工程**：精心设计的系统提示词约束模型按《中国药典》规范输出 13+ 字段，包括真伪鉴别与易混淆药材；
3. **闭环数据流**：识别 → 收藏 → 反馈，用户纠错可作为后续优化数据来源；
4. **教学辅助定位**：通过识别历史、收藏、相似药材对比等功能，服务中医药教学与自学场景；
5. **工程化实践**：前后端分离、异步架构、ORM、JWT 鉴权、配置化管理，具备完整的工程结构。

---

## 十二、后续规划

- [ ] 接入更多大模型（通义千问 VL、文心一言等）并做效果对比；
- [ ] 基于用户反馈数据微调/检索增强（RAG）提升识别准确率；
- [ ] 增加显微鉴别图谱与条码溯源功能；
- [ ] 完善管理后台，支持药材知识库的增删改查与反馈处理；
- [ ] 接入向量数据库，实现以图搜图（相似药材检索）。

---

## 十三、License

本项目仅用于学习与毕业设计，数据来源于公开药典资料，如有侵权请联系删除。
