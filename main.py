def main():
    """生成假 git 提交历史"""
    import os
    from datetime import datetime, timedelta

    REPO_DIR = "."  # 当前目录
    os.chdir(REPO_DIR)

    # 初始化 git（如果还没初始化）
    if not os.path.exists(".git"):
        os.system("git init")

    # 设置作者信息
    os.environ["GIT_AUTHOR_NAME"] = "esyion"
    os.environ["GIT_AUTHOR_EMAIL"] = "qingboup@gmail.com"

    START_DATE = datetime(2025, 3, 1)
    END_DATE = datetime(2026, 3, 1)
    current = START_DATE

    while current <= END_DATE:
        date_str = current.strftime("%Y-%m-%d")
        commit_msg = f"Update on {date_str}"

        # 写入文件触发变更
        with open("commit_log.txt", "w") as f:
            f.write(f"Commit for {date_str}\n")

        # 添加文件
        os.system("git add .")

        # 设置环境变量并提交
        author_date = f"{date_str} 12:00:00"
        os.environ["GIT_AUTHOR_DATE"] = author_date
        os.environ["GIT_COMMITTER_DATE"] = author_date

        os.system(f'git commit -m "{commit_msg}"')

        current += timedelta(days=1)

    # 统计
    os.system("echo '完成！共 $(git rev-list --count HEAD) 次提交'")
    os.system("git log --oneline --reverse")

if __name__ == "__main__":
    main()
