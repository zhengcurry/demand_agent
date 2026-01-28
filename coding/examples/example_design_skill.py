"""
Example: Using /design skill to create design documents
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from env_config import get_api_key
from skills.design_skill import DesignSkill


def main():
    api_key = get_api_key()
    if not api_key:
        return

    requirement = """
    设计一个在线教育平台:

    核心功能:
    1. 课程管理 - 教师可以创建、编辑课程
    2. 学生学习 - 学生可以浏览、购买、学习课程
    3. 视频播放 - 支持视频课程播放
    4. 作业系统 - 教师布置作业,学生提交作业
    5. 讨论区 - 课程讨论和问答

    技术要求:
    - 微服务架构
    - 支持高并发
    - 视频CDN加速
    - 移动端适配
    """

    print_safe("Initializing /design skill...")
    skill = DesignSkill(api_key=api_key, project_path="./education_platform")

    print_safe("\nExecuting /design workflow...\n")
    result = skill.execute(requirement)

    if result["success"]:
        print_safe("\n✅ Design completed successfully!")
        print_safe("\n📄 Design documents created:")
        print_safe("  - docs/requirement.json")
        print_safe("  - docs/architecture.json")
        print_safe("  - docs/api_spec.json")
    else:
        print_safe(f"\n❌ Design failed: {result.get('error')}")


if __name__ == "__main__":
    main()
