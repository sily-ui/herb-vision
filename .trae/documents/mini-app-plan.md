# AI中药标本智能识别小程序 - 实施计划

## 一、项目概述

基于 **uni-app + Vue3** 开发微信小程序用户端，配合 **Python FastAPI** 后端，实现AI中药标本智能识别、知识库查询、学习辅助等核心功能。

## 二、当前状态

- 项目目录为空，需从零搭建
- 技术选型已确定：前端 uni-app + Vue3，后端 FastAPI，数据库 SQLite/PostgreSQL
- 知识库采用内置初始数据（约200味常用药材），后续可增量更新

## 三、项目架构

```
AI-medicine/
├── frontend/                  # uni-app 小程序前端
│   ├── src/
│   │   ├── pages/             # 页面
│   │   │   ├── index/         # 首页（识别入口）
│   │   │   ├── identify/      # AI识别页
│   │   │   ├── knowledge/     # 知识库页
│   │   │   ├── compare/       # 混淆药材对比页
│   │   │   ├── learn/         # 学习辅助页
│   │   │   ├── mine/          # 个人中心页
│   │   │   └── feedback/      # 反馈页
│   │   ├── components/        # 公共组件
│   │   ├── api/               # 接口请求封装
│   │   ├── store/             # Pinia状态管理
│   │   ├── utils/             # 工具函数
│   │   ├── static/            # 静态资源
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── manifest.json
│   │   ├── pages.json
│   │   └── uni.scss
│   ├── package.json
│   └── vite.config.js
├── backend/                   # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py            # FastAPI入口
│   │   ├── config.py          # 配置
│   │   ├── routers/           # 路由
│   │   │   ├── identify.py    # 识别接口
│   │   │   ├── knowledge.py   # 知识库接口
│   │   │   ├── user.py        # 用户接口
│   │   │   └── feedback.py    # 反馈接口
│   │   ├── services/          # 业务逻辑
│   │   │   ├── ai_service.py  # 大模型调用
│   │   │   └── knowledge_service.py
│   │   ├── models/            # 数据模型
│   │   ├── database/          # 数据库
│   │   │   ├── init_data/     # 初始药材数据JSON
│   │   │   └── db.py
│   │   └── utils/
│   ├── requirements.txt
│   └── .env
└── README.md
```

## 四、实施步骤

### 阶段1：项目初始化与基础框架搭建

#### 1.1 前端项目初始化
- 使用 HBuilderX/CLI 创建 uni-app Vue3 项目
- 配置 `pages.json` 页面路由与 tabBar（首页/知识库/学习/我的）
- 配置 `manifest.json` 微信小程序 appid 与权限（相机、相册、位置）
- 安装依赖：pinia（状态管理）、uni-ui（UI组件库）、luch-request（网络请求）
- 创建公共样式 `uni.scss`（主题色、字号、间距变量）
- 封装 API 请求模块 `api/request.js`（统一拦截、token注入、错误处理）

#### 1.2 后端项目初始化
- 创建 FastAPI 项目结构
- 配置 CORS、环境变量（`.env`）
- 数据库初始化（SQLite开发/PostgreSQL生产）
- 创建数据表：`herbs`（药材表）、`users`（用户表）、`identify_records`（识别记录）、`favorites`（收藏）、`feedback`（反馈）
- 编写 `requirements.txt`（fastapi, uvicorn, sqlalchemy, python-jose, httpx, python-multipart）

#### 1.3 初始药材数据准备
- 编写200味常用中药标本数据 JSON（按中国药典标准）
- 数据字段：id, name, aliases, family, source, part_used, properties(smell/channel), efficacy, indications, usage, contraindications, appearance(color/texture/fracture/odor), authenticity_tips, confusable_herbs, storage, processing, images(主图/显微图/炮制图), category(按部位/功效/科属分类标签)
- 分批写入：先完成50味核心药材的完整数据，其余后续补充

### 阶段2：AI中药标本识别功能（核心）

#### 2.1 前端 - 拍照识别页 `pages/identify/`
- 拍照按钮：调用 `uni.chooseImage({ sourceType: ['camera'] })`
- 相册上传：调用 `uni.chooseImage({ sourceType: ['album'], count: 9 })`
- 图片预览与裁剪组件（支持多图）
- 上传进度条显示
- 识别结果页：展示大模型多维度输出
  - 药材标准名称、别名、科属、来源
  - 性状鉴别：颜色、质地、断面、气味
  - 真伪鉴别要点、易混淆药材对比（可点击跳转对比页）
  - 性味归经、功效主治、用法用量、禁忌
  - 标本高清图谱、显微鉴别简图
- 识别结果支持：收藏、分享、反馈错误

#### 2.2 前端 - 识别历史记录
- 自动保存识别图片+结果到本地 + 服务端
- 历史列表页：时间排序、缩略图+药材名
- 支持删除（单条/批量）、收藏
- 离线查看已缓存的识别结果

#### 2.3 后端 - AI识别接口
- `POST /api/identify`：接收图片（base64/文件上传）
- 调用大模型 API（智谱GLM-4V / 通义千问VL）进行多模态推理
- Prompt工程：构造中药鉴定专业提示词
  - 系统提示：你是一位资深中药鉴定专家...
  - 要求输出结构化JSON：名称、科属、性状、真伪鉴别、性味归经、功效主治、禁忌
- 结果后处理：与本地知识库交叉验证，补充易混淆药材信息
- 图片压缩与存储（识别原图保存供历史查看）

### 阶段3：中药标本知识库

#### 3.1 前端 - 知识库首页 `pages/knowledge/`
- 顶部搜索栏：关键词搜索（药材名/别名/病症/特征文字）
- 分类导航卡片：
  - 按药用部位：根及根茎、花、果实、皮类、全草、动物药、矿物药
  - 按功效：清热、补益、活血、解表等
  - 按科属分类
- 药材列表：网格布局，缩略图+名称，支持下拉刷新、上拉加载

#### 3.2 前端 - 标本详情页 `pages/knowledge/detail`
- 顶部轮播图：标准标本实拍图、显微图谱、炮制前后对比图
- 基本信息区：药典标准名称、别名、科属、来源
- 性状鉴别区：颜色、质地、断面、气味特征描述
- 真伪鉴别区：伪品对照图+鉴别要点文字
- 药典标准区：采收加工、储存条件、性味归经、功效主治、用法用量、禁忌
- 底部操作：收藏、分享

#### 3.3 后端 - 知识库接口
- `GET /api/herbs`：药材列表（分页、分类筛选、关键词搜索）
- `GET /api/herbs/:id`：药材详情
- `GET /api/herbs/search`：模糊/语义搜索（支持外观描述如"黄白色、粉质、菊花心"）
- `GET /api/herbs/compare`：混淆药材对比（接受两个药材ID，返回对比数据）
- 模糊搜索实现：关键词匹配 + 大模型语义理解（外观描述→药材名映射）

### 阶段4：学习辅助模块

#### 4.1 前端 - 学习首页 `pages/learn/`
- 收藏夹：收藏的药材列表，支持按分类筛选
- 最近浏览：浏览过的药材记录
- 学习统计：识别次数、收藏数量等简单统计

#### 4.2 前端 - 收藏管理
- 收藏/取消收藏操作（药材详情页、识别结果页均可触发）
- 收藏列表：支持删除、分类查看
- 数据同步：本地缓存 + 服务端存储

### 阶段5：辅助实用功能

#### 5.1 模糊检索
- 搜索页增强：输入外观描述文字，调用大模型语义匹配
- 示例："黄白色、粉质、菊花心" → 推荐黄芪、甘草等
- 搜索结果展示：匹配度排序，显示匹配原因

#### 5.2 混淆药材对比页 `pages/compare/`
- 选择两种相似药材（提供常见混淆对快捷入口）
- 左右对比布局：图片、性状、鉴别要点并排显示
- 常见混淆对预设：赤芍/白芍、北沙参/南沙参、人参/西洋参、半夏/水半夏等

#### 5.3 离线缓存
- 标记"常用"药材 → 下载其完整数据（图片+文字）到本地
- 离线检测：无网络时自动切换为离线模式
- 离线模式可用：已缓存药材的详情查看、收藏夹、识别历史

### 阶段6：用户中心

#### 6.1 前端 - 个人中心页 `pages/mine/`
- 微信一键授权登录（`uni.getUserProfile` + `uni.login`）
- 用户信息展示：头像、昵称
- 功能入口：
  - 识别记录
  - 我的收藏
  - 离线缓存管理（查看已缓存、清除缓存）
  - 清除缓存
  - 意见反馈
  - 关于

#### 6.2 后端 - 用户接口
- `POST /api/auth/wx-login`：微信登录（code换openid+session_key）
- `GET /api/user/profile`：用户信息
- `PUT /api/user/profile`：修改个人信息
- `GET /api/user/records`：识别记录列表
- `DELETE /api/user/records/:id`：删除识别记录
- `GET /api/user/favorites`：收藏列表
- `POST/DELETE /api/user/favorites`：添加/取消收藏

### 阶段7：反馈管理

#### 7.1 前端 - 反馈页 `pages/feedback/`
- 反馈类型选择：识别错误、资料缺失、其他
- 关联药材选择
- 文字描述 + 图片上传（可选）
- 提交反馈

#### 7.2 后端 - 反馈接口
- `POST /api/feedback`：提交反馈
- `GET /api/feedback`：反馈列表（管理端用）
- `PUT /api/feedback/:id`：审核反馈（管理端用）

## 五、关键实现细节

### 5.1 大模型调用策略
- **识别模型**：使用多模态视觉大模型（GLM-4V / Qwen-VL），直接输入图片+提示词
- **语义搜索**：使用文本大模型（GLM-4 / Qwen），将用户描述映射为药材特征关键词
- **Prompt模板**：预置专业中药鉴定提示词，要求结构化JSON输出
- **兜底策略**：大模型识别结果与知识库比对，不一致时标注"建议人工复核"

### 5.2 图片处理
- 上传前压缩：`uni.compressImage` 限制最大 1MB
- 支持格式：JPG、PNG
- 识别图存储：服务端保存原图供历史回溯

### 5.3 离线缓存实现
- 使用 `uni.setStorage` 存储药材文字数据
- 使用 `uni.downloadFile` + `uni.saveFile` 存储药材图片
- 缓存管理：记录缓存列表与大小，支持一键清除

### 5.4 微信小程序权限
- `scope.camera`：拍照识别
- `scope.album`：相册上传
- `scope.userLocation`：可选，位置标注

## 六、开发优先级

| 优先级 | 功能 | 说明 |
|--------|------|------|
| P0 | 前后端项目初始化 | 基础搭建 |
| P0 | AI拍照/上传识别 | 核心功能，项目价值所在 |
| P0 | 识别结果展示 | 核心交互体验 |
| P1 | 知识库浏览与搜索 | 高频使用功能 |
| P1 | 标本详情页 | 信息展示核心 |
| P1 | 用户登录与个人中心 | 基础功能 |
| P2 | 识别历史记录 | 用户体验提升 |
| P2 | 收藏夹 | 学习辅助 |
| P2 | 混淆药材对比 | 实用功能 |
| P2 | 模糊检索 | 特色功能 |
| P3 | 离线缓存 | 体验优化 |
| P3 | 反馈管理 | 运营支持 |
| P3 | 学习统计 | 锦上添花 |

## 七、验证步骤

1. 前端项目可正常编译运行至微信开发者工具
2. 后端API可通过Swagger文档测试
3. AI识别功能端到端可用（拍照→上传→返回结果→展示）
4. 知识库搜索、分类、详情页数据正常展示
5. 微信授权登录流程完整
6. 收藏、历史记录功能正常
7. 离线模式可查看已缓存数据
8. 混淆对比页数据正确对比展示
