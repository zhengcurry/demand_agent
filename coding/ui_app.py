"""
Enhanced Code Skill - Web UI
Simple graphical interface for code generation workflow
"""
import streamlit as st
import os
from pathlib import Path
import sys

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from env_config import get_api_key
from skills.enhanced_code_skill import EnhancedCodeSkill
from utils import print_safe


def init_session_state():
    """Initialize session state variables"""
    if 'workflow_running' not in st.session_state:
        st.session_state.workflow_running = False
    if 'workflow_result' not in st.session_state:
        st.session_state.workflow_result = None
    if 'status_messages' not in st.session_state:
        st.session_state.status_messages = []


def add_status_message(message: str):
    """Add a status message to the display"""
    st.session_state.status_messages.append(message)


def main():
    st.set_page_config(
        page_title="Enhanced Code Skill",
        page_icon="🚀",
        layout="wide"
    )

    init_session_state()

    # Header
    st.title("🚀 Enhanced Code Skill")
    st.markdown("### AI-Powered Code Generation Workflow")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=get_api_key() or "",
            help="Your Anthropic API key"
        )

        # Project directory
        default_project_path = str(Path.cwd() / "generated_project")
        project_path = st.text_input(
            "Project Directory",
            value=default_project_path,
            help="Where to generate the code"
        )

        # Review mode
        review_mode = st.selectbox(
            "Review Mode",
            options=["auto", "manual"],
            index=0,
            help="Auto: automatic review, Manual: pause for review"
        )

        # Pause for review
        pause_for_review = st.checkbox(
            "Pause for Review",
            value=False,
            help="Pause after design stage for manual review"
        )

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool uses a 6-stage workflow:
        1. 📋 Requirement Analysis
        2. 🏗️ Design (Architecture + API)
        3. 🔍 Design Review
        4. 📝 Task Planning
        5. 💻 Code Generation
        6. ✅ Code Review
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Requirement Input")

        # Input method selection
        input_method = st.radio(
            "Input Method",
            options=["Text Input", "File Upload", "URL"],
            horizontal=True
        )

        requirement_text = ""

        if input_method == "Text Input":
            requirement_text = st.text_area(
                "Enter your requirement",
                height=200,
                placeholder="Example:\n开发一个简单的计算器API:\n\n功能需求:\n1. 支持加法、减法、乘法、除法\n2. 输入验证\n3. 错误处理\n\n技术要求:\n- 后端: Python + FastAPI\n- 返回JSON格式"
            )

        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload requirement file",
                type=["txt", "md"]
            )
            if uploaded_file is not None:
                requirement_text = uploaded_file.read().decode("utf-8")
                st.text_area("File content", value=requirement_text, height=200, disabled=True)

        elif input_method == "URL":
            requirement_url = st.text_input(
                "Enter requirement URL",
                placeholder="https://example.com/requirement.txt"
            )
            if requirement_url:
                st.info("URL input will be implemented in future version")
                # TODO: Implement URL fetching

        # Generate button
        st.markdown("---")
        generate_button = st.button(
            "🚀 Generate Code",
            type="primary",
            disabled=st.session_state.workflow_running or not requirement_text or not api_key,
            use_container_width=True
        )

        if not api_key:
            st.warning("⚠️ Please enter your Anthropic API key in the sidebar")
        elif not requirement_text:
            st.info("💡 Please enter a requirement to get started")

    with col2:
        st.header("📊 Status")

        # Status display
        if st.session_state.workflow_running:
            st.info("🔄 Workflow is running...")
        elif st.session_state.workflow_result:
            result = st.session_state.workflow_result
            if result.get("success"):
                st.success("✅ Workflow completed successfully!")
                st.metric("Final Score", f"{result.get('final_score', 0)}/100")
                st.metric("Generated Files", result.get('generated_files', 0))
            else:
                st.error(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
        else:
            st.info("⏳ Ready to start")

    # Status messages area
    if st.session_state.status_messages:
        st.markdown("---")
        st.header("📋 Workflow Log")
        status_container = st.container()
        with status_container:
            for msg in st.session_state.status_messages:
                st.text(msg)

    # Handle generate button click
    if generate_button:
        st.session_state.workflow_running = True
        st.session_state.status_messages = []
        st.session_state.workflow_result = None

        # Create progress placeholder
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        try:
            with st.spinner("Initializing workflow..."):
                add_status_message("🚀 Starting Enhanced Code Skill workflow...")
                add_status_message(f"📁 Project directory: {project_path}")
                add_status_message(f"⚙️ Review mode: {review_mode}")

                # Initialize skill
                skill = EnhancedCodeSkill(
                    api_key=api_key,
                    project_path=project_path
                )
                add_status_message("✅ Enhanced Code Skill initialized")

                # Execute workflow
                add_status_message("\n" + "="*70)
                add_status_message("Starting 6-stage workflow...")
                add_status_message("="*70)

                result = skill.execute(
                    requirement=requirement_text,
                    review_mode=review_mode,
                    pause_for_review=pause_for_review
                )

                st.session_state.workflow_result = result
                st.session_state.workflow_running = False

                if result.get("success"):
                    add_status_message("\n✅ Workflow completed successfully!")
                    add_status_message(f"📊 Final Score: {result.get('final_score')}/100")
                    add_status_message(f"📁 Generated Files: {len(result.get('generated_files', []))}")
                    add_status_message(f"📄 Reports saved in: {project_path}/docs/")
                else:
                    add_status_message(f"\n❌ Workflow failed: {result.get('error')}")

        except Exception as e:
            st.session_state.workflow_running = False
            st.session_state.workflow_result = {
                "success": False,
                "error": str(e)
            }
            add_status_message(f"\n❌ Error: {str(e)}")

        # Rerun to update UI
        st.rerun()


if __name__ == "__main__":
    main()

