# 更新日志

本项目的所有重要变更记录在此。

## [Unreleased] · 2026-08-06

### ✨ 改进 / 新功能
- 意见反馈：支持不选药材直接提交；支持多图上传（前端逗号拼接、后端单字段存）
- 知识库搜索新增"选择模式"：勾选框 + 底部"确认选择"操作栏，关联药材回填意见反馈页
- 学习足迹改为按日登录去重记录（`studyLog`），进入"学习" tab 即写入，更符合直觉
- 微信小程序配置清理：移除废弃的 `permission` 声明

### 🐛 修复
- **反馈提交 422**：后端 `herb_id: int = None` 改为 `Optional[int] = None`（Pydantic v2 兼容 null）
- **反馈图片上传 404**：新增 `POST /api/upload` 通用图片上传接口（需登录）
- **反馈页"保存失败"按钮卡住**：通过 `getCurrentPages().length` 智能判断 `navigateBack` 还是 `switchTab`
- **关联药材点不中 / "请先选择药材"**：用基本类型 `selectedId` / `selectedName` 替代 `ref({})`，绕过 Vue 响应式 proxy 在小程序端的解包异常
- **资料保存 405**：后端 `/api/user/profile` 由 PUT 改为 POST，与前端对齐
- **资料保存 `TypeError: 'set' on proxy`**：Pinia `nickname` / `avatar` 是 getter，改为更新 `userStore.userInfo` 对象本身
- **学习足迹不亮**：必须浏览过详情页才会点亮的旧逻辑移除，改为按日记录进入学习页

### 🛠 重构
- 搜索页选择模式用 storage + 全局事件双通道返回（兼容 H5 / 小程序 onShow 时序差异）
- 清理临时调试脚本 `backend/check_favorites.py`、`backend/check_herb_category.py`

### 📚 文档
- README 增补"最近更新"章节，按 4 条业务线说明本次迭代内容
- README API 表补充 `/api/upload` 接口，更新 `/api/feedback` 行为说明
- 新增本 CHANGELOG.md

---

## 历史

详见 `git log --oneline`。
</content>
</invoke>