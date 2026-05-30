# fxsa-commit 工程化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 fxsa-commit 从简单脚本改造为模块化的开源 CLI 工具

**Architecture:** 使用 pydantic-settings 管理配置，拆分为 config.py、git_client.py、main.py 三个模块

**Tech Stack:** Python 3.10+, pydantic>=2.0, pydantic-settings>=2.0, python-dotenv>=1.0

---

## 文件结构

```
src/
  __init__.py         # 包初始化
  config.py           # Pydantic 配置模型
  git_client.py       # Git 操作封装
  main.py             # 入口点
.env.example          # 环境变量模板
.env                 # 本地配置（不提交）
pyproject.toml       # 项目配置
```

---

## 实现任务

### Task 1: 更新 pyproject.toml 添加依赖

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: 更新 pyproject.toml**

```toml
[project]
name = "fxsa-commit"
version = "0.1.0"
description = "生成假 git 提交历史的 CLI 工具"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "python-dotenv>=1.0",
]

[project.scripts]
fxsa-commit = "src.main:main"
```

- [ ] **Step 2: 安装依赖**

Run: `pip install -e .`

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add pydantic-settings and python-dotenv dependencies"
```

---

### Task 2: 创建 .env.example 配置模板

**Files:**
- Create: `.env.example`

- [ ] **Step 1: 创建 .env.example**

```env
# 必需配置
FXSA_AUTHOR_NAME=your-name
FXSA_AUTHOR_EMAIL=your@email.com

# 可选配置
FXSA_START_DATE=2026-01-01
FXSA_END_DATE=2026-01-31
FXSA_COMMITS_PER_DAY=1
FXSA_COMMIT_TEMPLATE=Update on {date}
FXSA_REPO_PATH=.
FXSA_BRANCH=main
FXSA_HOUR=12
```

- [ ] **Step 2: 更新 .gitignore**

Run: `echo ".env" >> .gitignore`

- [ ] **Step 3: Commit**

```bash
git add .env.example .gitignore
git commit -m "feat: add .env.example template and update gitignore"
```

---

### Task 3: 创建 src/config.py 配置模块

**Files:**
- Create: `src/__init__.py`
- Create: `src/config.py`

- [ ] **Step 1: 创建 src/__init__.py**

```python
"""fxsa-commit: 生成假 git 提交历史的工具"""
```

- [ ] **Step 2: 创建 src/config.py**

```python
"""配置管理模块"""
from datetime import date
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """fxsa-commit 配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # 必需配置
    author_name: str = Field(..., min_length=1, description="Git 提交用户名")
    author_email: str = Field(..., min_length=1, description="Git 提交邮箱")

    # 可选配置
    start_date: date = Field(default=date(2026, 1, 1), description="开始日期")
    end_date: date = Field(default=date(2026, 1, 31), description="结束日期")
    commits_per_day: int = Field(default=1, ge=1, description="每天提交次数")
    commit_template: str = Field(default="Update on {date}", description="提交消息模板")
    repo_path: Path = Field(default=Path("."), description="仓库路径")
    branch: str = Field(default="main", description="分支名")
    hour: int = Field(default=12, ge=0, le=23, description="提交小时 (0-23)")

    def validate_dates(self) -> None:
        """验证日期范围"""
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")

    def get_date_range(self) -> list[date]:
        """获取日期范围内的所有日期"""
        from datetime import timedelta
        dates = []
        current = self.start_date
        while current <= self.end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates

    def format_commit_message(self, commit_date: date) -> str:
        """格式化提交消息"""
        return self.commit_template.format(date=commit_date.isoformat())
```

- [ ] **Step 3: Commit**

```bash
git add src/__init__.py src/config.py
git commit -m "feat: add config module with pydantic-settings"
```

---

### Task 4: 创建 src/git_client.py Git 客户端

**Files:**
- Create: `src/git_client.py`

- [ ] **Step 1: 创建 src/git_client.py**

```python
"""Git 操作封装模块"""
import os
import subprocess
from datetime import date, datetime
from pathlib import Path

from .config import Settings


class GitClient:
    """Git 操作客户端"""

    def __init__(self, config: Settings):
        self.config = config
        self.repo_path = config.repo_path

    def _run_git(self, *args: str) -> subprocess.CompletedProcess:
        """执行 git 命令"""
        cmd = ["git", "-C", str(self.repo_path)] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Git error: {result.stderr}")
        return result

    def init_repo(self) -> None:
        """初始化 git 仓库"""
        if not (self.repo_path / ".git").exists():
            self._run_git("init")
            self._run_git("checkout", "-b", self.config.branch)
        else:
            # 确保在正确的分支
            self._run_git("checkout", self.config.branch)

    def setup_author(self) -> None:
        """设置 git 作者信息"""
        os.environ["GIT_AUTHOR_NAME"] = self.config.author_name
        os.environ["GIT_AUTHOR_EMAIL"] = self.config.author_email
        os.environ["GIT_COMMITTER_NAME"] = self.config.author_name
        os.environ["GIT_COMMITTER_EMAIL"] = self.config.author_email

    def commit(self, message: str, commit_date: date) -> None:
        """创建提交"""
        author_date = f"{commit_date.isoformat()} {self.config.hour}:00:00"
        os.environ["GIT_AUTHOR_DATE"] = author_date
        os.environ["GIT_COMMITTER_DATE"] = author_date

        # 确保有文件变更
        marker_file = self.repo_path / ".commit_marker"
        marker_file.write_text(f"{message}\n")

        self._run_git("add", ".")

        result = subprocess.run(
            ["git", "-C", str(self.repo_path), "commit", "-m", message],
            capture_output=True,
            text=True,
            env={**os.environ, "GIT_AUTHOR_DATE": author_date, "GIT_COMMITTER_DATE": author_date},
        )
        if result.returncode != 0:
            raise RuntimeError(f"Commit failed: {result.stderr}")

    def get_commit_count(self) -> int:
        """获取提交数量"""
        result = self._run_git("rev-list", "--count", "HEAD")
        return int(result.stdout.strip())

    def run(self) -> int:
        """执行提交生成"""
        self.setup_author()
        self.init_repo()

        total_commits = 0
        for commit_date in self.config.get_date_range():
            for _ in range(self.config.commits_per_day):
                message = self.config.format_commit_message(commit_date)
                self.commit(message, commit_date)
                total_commits += 1

        return total_commits
```

- [ ] **Step 2: Commit**

```bash
git add src/git_client.py
git commit -m "feat: add GitClient for git operations"
```

---

### Task 5: 重构 src/main.py 入口点

**Files:**
- Create: `src/main.py`
- Delete: `main.py` (根目录的旧文件)

- [ ] **Step 1: 创建 src/main.py**

```python
"""fxsa-commit 入口点"""
import sys

from .config import Settings
from .git_client import GitClient


def main() -> int:
    """主函数"""
    try:
        config = Settings()
        config.validate_dates()

        print(f"开始生成提交历史...")
        print(f"作者: {config.author_name} <{config.author_email}>")
        print(f"日期范围: {config.start_date} - {config.end_date}")

        client = GitClient(config)
        count = client.run()

        print(f"完成！共生成 {count} 次提交")
        return 0

    except FileNotFoundError as e:
        print(f"错误: 仓库路径不存在 - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"错误: 配置无效 - {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"错误: Git 操作失败 - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 删除旧文件并移动到 src/**

```bash
mv main.py src/main.py
git add main.py  # 会被识别为删除
git add src/main.py
git commit -m "feat: move main.py to src/ module"
```

- [ ] **Step 3: 更新引用**

Run: `python -c "from src.main import main; print('import ok')"`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: complete module structure refactor"
```

---

## 验收检查

- [ ] `pip install -e .` 成功安装
- [ ] 缺少 FXSA_AUTHOR_NAME 或 FXSA_AUTHOR_EMAIL 时有清晰错误提示
- [ ] `.env.example` 包含所有配置项说明
- [ ] `python -m src.main` 能正常运行
- [ ] 生成的提交使用配置中的作者信息

---

**Plan complete.**