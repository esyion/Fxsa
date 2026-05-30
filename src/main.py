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