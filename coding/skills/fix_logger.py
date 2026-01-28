"""
Fix Logger
Records all fix attempts and results
"""
import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime


class FixLogger:
    """Logs all fix attempts and results"""

    def __init__(self, project_path: str):
        """
        Initialize fix logger

        Args:
            project_path: Path to project directory
        """
        self.project_path = Path(project_path)
        self.log_file = self.project_path / "docs" / "fix_log.json"
        self.fix_records = []

    def log_attempt(self, stage: str, error_context: Dict[str, Any],
                   fix_strategy: str, attempt_number: int):
        """
        Log a fix attempt

        Args:
            stage: Stage where error occurred
            error_context: Error context information
            fix_strategy: Strategy being applied
            attempt_number: Attempt number
        """
        record = {
            "stage": stage,
            "attempt": attempt_number,
            "timestamp": datetime.now().isoformat(),
            "error": error_context,
            "fix_strategy": fix_strategy,
            "status": "attempting"
        }
        self.fix_records.append(record)

    def log_success(self, stage: str, attempt_number: int):
        """
        Log successful fix

        Args:
            stage: Stage that was fixed
            attempt_number: Attempt number that succeeded
        """
        # Find the record and update it
        for record in reversed(self.fix_records):
            if record["stage"] == stage and record["attempt"] == attempt_number:
                record["status"] = "success"
                record["resolved_at"] = datetime.now().isoformat()
                break

    def log_failure(self, stage: str, attempt_number: int, reason: str):
        """
        Log failed fix attempt

        Args:
            stage: Stage that failed
            attempt_number: Attempt number that failed
            reason: Reason for failure
        """
        for record in reversed(self.fix_records):
            if record["stage"] == stage and record["attempt"] == attempt_number:
                record["status"] = "failed"
                record["failure_reason"] = reason
                record["failed_at"] = datetime.now().isoformat()
                break

    def save(self):
        """Save fix log to file"""
        # Ensure docs directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "fix_records": self.fix_records,
                "summary": self._generate_summary()
            }, f, indent=2)

    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics

        Returns:
            Summary dictionary
        """
        total_attempts = len(self.fix_records)
        successful = sum(1 for r in self.fix_records if r.get("status") == "success")
        failed = sum(1 for r in self.fix_records if r.get("status") == "failed")

        return {
            "total_attempts": total_attempts,
            "successful_fixes": successful,
            "failed_fixes": failed,
            "success_rate": f"{(successful / total_attempts * 100):.1f}%" if total_attempts > 0 else "0%"
        }

    def get_summary(self) -> str:
        """
        Get human-readable summary

        Returns:
            Summary string
        """
        summary = self._generate_summary()
        return (f"Fix Attempts: {summary['total_attempts']} | "
                f"Successful: {summary['successful_fixes']} | "
                f"Failed: {summary['failed_fixes']} | "
                f"Success Rate: {summary['success_rate']}")
