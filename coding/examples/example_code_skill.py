"""
Example: Using /code skill to generate a simple web application
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from env_config import get_api_key
from skills.code_skill import CodeSkill


def main():
    # Get API key using env_config (loads from .env file)
    api_key = get_api_key()
    if not api_key:
        return

    # Define requirement
    requirement = """
    开发一个简单的待办事项(Todo)Web应用:

    功能需求:
    1. 用户可以添加新的待办事项
    2. 用户可以标记待办事项为完成
    3. 用户可以删除待办事项
    4. 显示所有待办事项列表

    技术要求:
    - 后端: Python + Flask
    - 前端: HTML + JavaScript
    - 数据存储: SQLite
    - RESTful API设计

    非功能需求:
    - 代码简洁易读
    - 包含基本的错误处理
    - 提供单元测试
    """

    # Initialize skill
    print_safe("Initializing /code skill...")
    skill = CodeSkill(
        api_key=api_key,
        project_path="./todo_app"
    )

    # Execute workflow
    print_safe("\nExecuting /code workflow...")
    print_safe("This may take a few minutes...\n")

    result = skill.execute(
        requirement=requirement,
        mode="auto"
    )

    # Check result
    if result["success"]:
        print_safe("\n" + "="*60)
        print_safe("✅ Code generation completed successfully!")
        print_safe("="*60)

        results = result["results"]

        print_safe("\n📋 Generated Files:")
        for file in results.get("generated_files", []):
            print_safe(f"  - {file}")

        print_safe("\n📊 Code Review Score:")
        review = results.get("review", {})
        print_safe(f"  Overall Score: {review.get('overall_score', 'N/A')}/100")

        issues = review.get("issues", [])
        if issues:
            print_safe(f"\n⚠️  Issues Found: {len(issues)}")
            critical = [i for i in issues if i.get("severity") == "critical"]
            if critical:
                print_safe(f"  Critical: {len(critical)}")

        print_safe("\n📄 Documentation:")
        print_safe("  - docs/requirement.json")
        print_safe("  - docs/architecture.json")
        print_safe("  - docs/api_spec.json")
        print_safe("  - docs/code_review.json")

        print_safe("\n🎉 Project generated at: ./todo_app")
        print_safe("\nNext steps:")
        print_safe("  1. cd todo_app")
        print_safe("  2. pip install -r requirements.txt")
        print_safe("  3. python app.py")

    else:
        print_safe("\n❌ Code generation failed!")
        print_safe(f"Error: {result.get('error')}")


if __name__ == "__main__":
    main()
