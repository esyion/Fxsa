# 随机提交功能设计

**日期：** 2026-05-30
**目标：** 添加随机提交模式

## 概述

用户可以选择每天提交固定次数或随机次数，让提交历史更自然。

## 配置项

| 配置项 | 环境变量 | 类型 | 默认值 | 说明 |
|--------|----------|------|--------|------|
| 作者名 | `FXSA_AUTHOR_NAME` | str | - | 必需 |
| 作者邮箱 | `FXSA_AUTHOR_EMAIL` | str | - | 必需 |
| 开始日期 | `FXSA_START_DATE` | date | 2026-01-01 | 可选 |
| 结束日期 | `FXSA_END_DATE` | date | 2026-01-31 | 可选 |
| 随机模式 | `FXSA_RANDOM` | bool | false | 可选 |
| 随机区间 | `FXSA_RANDOM_RANGE` | tuple | (1, 10) | 可选，格式 "min,max" |
| 固定次数 | `FXSA_COMMITS_PER_DAY` | int | 1 | 固定模式专用 |
| 分支名 | `FXSA_BRANCH` | str | main | 可选 |
| 提交小时 | `FXSA_HOUR` | int | 12 | 可选 |

## 逻辑

```python
if random_mode:
    commits_count = random.randint(range[0], range[1])
else:
    commits_count = commits_per_day
```

## 示例配置

**固定模式（默认）：**
```env
FXSA_AUTHOR_NAME=xxx
FXSA_AUTHOR_EMAIL=xxx@xxx.com
FXSA_COMMITS_PER_DAY=3
```

**随机模式：**
```env
FXSA_AUTHOR_NAME=xxx
FXSA_AUTHOR_EMAIL=xxx@xxx.com
FXSA_RANDOM=true
FXSA_RANDOM_RANGE=1,10
```

## 实现要点

1. `random_range` 解析 "min,max" 格式
2. `random.randint()` 生成随机次数
3. 默认关闭随机模式，兼容现有行为