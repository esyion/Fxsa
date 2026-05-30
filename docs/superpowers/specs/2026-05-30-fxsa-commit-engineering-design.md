# fxsa-commit 工程化设计

**日期：** 2026-05-30
**目标：** 将 fxsa-commit 从简单脚本改造为工程化的开源 CLI 工具

## 概述

将 `fxsa-commit` 改造为结构清晰、配置规范、易于维护和贡献的开源工具。

## 功能需求

### 配置项

| 配置项 | 环境变量 | 说明 | 默认值 |
|--------|----------|------|--------|
| 作者名 | `FXSA_AUTHOR_NAME` | Git 提交使用的用户名 | - |
| 作者邮箱 | `FXSA_AUTHOR_EMAIL` | Git 提交使用的邮箱 | - |
| 开始日期 | `FXSA_START_DATE` | 提交历史开始日期 (YYYY-MM-DD) | 2026-01-01 |
| 结束日期 | `FXSA_END_DATE` | 提交历史结束日期 (YYYY-MM-DD) | 2026-01-31 |
| 每天提交次数 | `FXSA_COMMITS_PER_DAY` | 每天生成的提交数 | 1 |
| 提交消息模板 | `FXSA_COMMIT_TEMPLATE` | 提交消息模板，{date} 会被替换 | "Update on {date}" |
| 仓库路径 | `FXSA_REPO_PATH` | Git 仓库路径 | "." (当前目录) |
| 分支名 | `FXSA_BRANCH` | 操作的分支名 | "main" |
| 提交时间 | `FXSA_HOUR` | 每天提交的小时 (0-23) | 12 |

## 技术方案

### 依赖

```toml
[project]
name = "fxsa-commit"
version = "0.1.0"
description = "生成假 git 提交历史的 CLI 工具"
requires-python = ">=3.10"
dependencies = [
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "python-dotenv>=1.0",
]
```

### 项目结构

```
src/
  __init__.py
  config.py       # Pydantic 配置模型
  git_client.py   # Git 操作封装
  main.py         # 入口点

.env.example      # 环境变量模板
pyproject.toml   # 项目配置
```

### 模块设计

#### config.py
- 使用 `pydantic-settings` 定义配置模型
- 自动从 `.env` 文件读取环境变量
- 配置验证和类型转换
- 必需字段校验（name、email）

#### git_client.py
- `GitClient` 类封装所有 Git 操作
- 方法：`init_repo()`, `commit()`, `get_commit_count()`
- 通过环境变量设置 author/committer 信息

#### main.py
- 读取配置
- 调用 `GitClient` 执行提交
- 简单的日志输出

### 配置加载顺序

1. 从 `.env` 文件加载环境变量
2. `pydantic-settings` 自动读取并验证
3. 缺失必填配置时报错退出

### 错误处理

- 缺少必填配置（name/email）：明确提示需要配置哪些变量
- Git 仓库问题：清晰的错误信息
- 日期格式错误：提示正确格式

## 实现步骤

1. 更新 `pyproject.toml` 添加依赖
2. 创建 `.env.example` 配置模板
3. 重构 `src/config.py` 配置模块
4. 创建 `src/git_client.py` Git 客户端
5. 重构 `src/main.py` 入口点
6. 测试完整流程

## 验收标准

- [ ] 所有配置通过 `.env` 文件读取
- [ ] 缺少必填配置时有清晰错误提示
- [ ] 类型转换正确（日期、整数）
- [ ] Git 提交信息正确显示配置的作者
- [ ] `.env.example` 可作为配置向导