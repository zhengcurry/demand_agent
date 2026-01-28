"""
Launch script for Enhanced Code Skill UI
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("="*70)
    print("Enhanced Code Skill - Web UI")
    print("="*70)
    print("\nStarting Streamlit application...")
    print("The UI will open in your browser automatically.\n")
    print("Press Ctrl+C to stop the server.\n")
    print("="*70)

    # Get the directory of this script
    script_dir = Path(__file__).parent
    ui_app_path = script_dir / "ui_app.py"

    # Launch streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(ui_app_path),
        "--server.port=8501",
        "--server.headless=false"
    ])

if __name__ == "__main__":
    main()
