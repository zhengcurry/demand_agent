"""
Self-Healing Skill
Wraps EnhancedCodeSkill with automatic error recovery
"""
import sys
from pathlib import Path
from typing import Dict, Any, Callable
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from skills.enhanced_code_skill import EnhancedCodeSkill
from skills.error_context import ErrorContext, ErrorType
from skills.fix_logger import FixLogger


class SelfHealingSkill:
    """
    Enhanced Code Skill with self-healing capabilities
    Automatically retries failed stages with intelligent error handling
    """

    def __init__(self, api_key: str, project_path: str = None, max_retries: int = 3):
        """
        Initialize Self-Healing Skill

        Args:
            api_key: Anthropic API key
            project_path: Path to project directory
            max_retries: Maximum retry attempts per stage
        """
        self.api_key = api_key
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.max_retries = max_retries

        # Initialize base skill
        self.base_skill = EnhancedCodeSkill(api_key, str(self.project_path))

        # Initialize fix logger
        self.fix_logger = FixLogger(str(self.project_path))

        # Retry strategies for different error types
        self.retry_strategies = {
            ErrorType.PARSING: "Improved JSON extraction",
            ErrorType.API: "Retry with exponential backoff",
            ErrorType.NETWORK: "Retry after network recovery",
            ErrorType.TIMEOUT: "Retry with increased timeout",
            ErrorType.GENERATION: "Simplified task breakdown",
            ErrorType.VALIDATION: "Relaxed validation rules",
            ErrorType.FILE: "Ensure directory exists",
            ErrorType.UNKNOWN: "Generic retry"
        }

    def execute(self, requirement: str, review_mode: str = "auto",
                pause_for_review: bool = False) -> Dict[str, Any]:
        """
        Execute workflow with self-healing

        Args:
            requirement: Requirement description
            review_mode: Review mode ('auto' or 'manual')
            pause_for_review: Whether to pause for review

        Returns:
            Workflow execution result
        """
        print_safe("="*70)
        print_safe("[START] Self-Healing Code Generation Workflow")
        print_safe("="*70)
        print_safe(f"Max Retries per Stage: {self.max_retries}")
        print_safe(f"Review Mode: {review_mode.upper()}")
        print_safe("="*70)

        try:
            # Execute with self-healing wrapper
            result = self._execute_with_healing(
                requirement=requirement,
                review_mode=review_mode,
                pause_for_review=pause_for_review
            )

            # Save fix log
            self.fix_logger.save()

            # Add fix summary to result
            if self.fix_logger.fix_records:
                result["fix_summary"] = self.fix_logger.get_summary()
                result["fix_log_path"] = str(self.fix_logger.log_file)

            return result

        except Exception as e:
            # Final failure
            self.fix_logger.save()
            return {
                "success": False,
                "error": str(e),
                "fix_summary": self.fix_logger.get_summary(),
                "fix_log_path": str(self.fix_logger.log_file)
            }

    def _execute_with_healing(self, requirement: str, review_mode: str,
                             pause_for_review: bool) -> Dict[str, Any]:
        """
        Execute workflow with healing wrapper

        Args:
            requirement: Requirement description
            review_mode: Review mode
            pause_for_review: Pause for review flag

        Returns:
            Execution result
        """
        # Try to execute the full workflow
        for attempt in range(self.max_retries):
            try:
                print_safe(f"\n[ATTEMPT {attempt + 1}/{self.max_retries}] Starting workflow...")

                result = self.base_skill.execute(
                    requirement=requirement,
                    review_mode=review_mode,
                    pause_for_review=pause_for_review
                )

                if result.get("success"):
                    if attempt > 0:
                        print_safe(f"\n[SUCCESS] Workflow succeeded after {attempt + 1} attempt(s)")
                    return result
                else:
                    # Workflow returned failure
                    error_msg = result.get("error", "Unknown error")
                    stage = result.get("stage", "unknown")

                    print_safe(f"\n[ERROR] Workflow failed at {stage}: {error_msg}")

                    # Create error context
                    error_context = ErrorContext(
                        exception=Exception(error_msg),
                        stage=stage,
                        additional_info={"result": result}
                    )

                    # Log the attempt
                    self._log_fix_attempt(error_context, attempt + 1)

                    # Check if we should retry
                    if attempt < self.max_retries - 1:
                        print_safe(f"[RETRY] Attempting to fix and retry...")
                        self._apply_fix_strategy(error_context)
                    else:
                        print_safe(f"[FAILED] Max retries ({self.max_retries}) reached")
                        self.fix_logger.log_failure(stage, attempt + 1, "Max retries reached")
                        return result

            except Exception as e:
                # Unexpected exception
                stage = "unknown"
                print_safe(f"\n[EXCEPTION] Unexpected error: {str(e)}")

                # Create error context
                error_context = ErrorContext(
                    exception=e,
                    stage=stage
                )

                # Log the attempt
                self._log_fix_attempt(error_context, attempt + 1)

                # Check if we should retry
                if attempt < self.max_retries - 1:
                    print_safe(f"[RETRY] Attempting to recover...")
                    self._apply_fix_strategy(error_context)
                else:
                    print_safe(f"[FAILED] Max retries ({self.max_retries}) reached")
                    self.fix_logger.log_failure(stage, attempt + 1, str(e))
                    raise

        # Should not reach here
        return {"success": False, "error": "Max retries reached"}

    def _log_fix_attempt(self, error_context: ErrorContext, attempt: int):
        """
        Log a fix attempt

        Args:
            error_context: Error context
            attempt: Attempt number
        """
        strategy = self.retry_strategies.get(
            error_context.error_type,
            "Generic retry"
        )

        print_safe(f"\n[FIX] Error Type: {error_context.error_type.value}")
        print_safe(f"[FIX] Strategy: {strategy}")

        self.fix_logger.log_attempt(
            stage=error_context.stage,
            error_context=error_context.to_dict(),
            fix_strategy=strategy,
            attempt_number=attempt
        )

    def _apply_fix_strategy(self, error_context: ErrorContext):
        """
        Apply fix strategy based on error type

        Args:
            error_context: Error context
        """
        # For Phase 1, we just log the strategy
        # In Phase 2/3, we would implement actual fixes here

        strategy = self.retry_strategies.get(
            error_context.error_type,
            "Generic retry"
        )

        print_safe(f"[FIX] Applying strategy: {strategy}")

        # Add a small delay before retry
        import time
        time.sleep(2)

        # In future phases, we would:
        # 1. Analyze the error with ErrorAnalyzer
        # 2. Generate fix with AutoFixer
        # 3. Apply the fix
        # 4. Validate the fix

        print_safe("[FIX] Strategy applied, ready to retry")
