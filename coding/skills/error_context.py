"""
Error Types and Context
Defines error classifications and context capture
"""
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
import traceback


class ErrorType(Enum):
    """Error type classification"""
    PARSING = "parsing"           # JSON parsing errors
    API = "api"                   # API call errors
    VALIDATION = "validation"     # Validation errors
    GENERATION = "generation"     # Code generation errors
    FILE = "file"                 # File operation errors
    NETWORK = "network"           # Network errors
    TIMEOUT = "timeout"           # Timeout errors
    UNKNOWN = "unknown"           # Unknown errors


class ErrorContext:
    """Captures detailed error context"""

    def __init__(self, exception: Exception, stage: str, additional_info: Dict[str, Any] = None):
        """
        Initialize error context

        Args:
            exception: The exception that occurred
            stage: The stage where error occurred
            additional_info: Additional context information
        """
        self.exception = exception
        self.stage = stage
        self.error_type = self._classify_error(exception)
        self.timestamp = datetime.now().isoformat()
        self.traceback = traceback.format_exc()
        self.additional_info = additional_info or {}

    def _classify_error(self, exception: Exception) -> ErrorType:
        """
        Classify error type based on exception

        Args:
            exception: The exception to classify

        Returns:
            ErrorType classification
        """
        error_msg = str(exception).lower()
        exception_type = type(exception).__name__

        # JSON parsing errors
        if "json" in error_msg or exception_type == "JSONDecodeError":
            return ErrorType.PARSING

        # API errors
        if "api" in error_msg or "anthropic" in error_msg or exception_type in ["APIError", "APIConnectionError"]:
            return ErrorType.API

        # Network errors
        if "network" in error_msg or "connection" in error_msg or exception_type in ["ConnectionError", "Timeout"]:
            return ErrorType.NETWORK

        # Timeout errors
        if "timeout" in error_msg or exception_type == "TimeoutError":
            return ErrorType.TIMEOUT

        # File errors
        if "file" in error_msg or exception_type in ["FileNotFoundError", "PermissionError", "IOError"]:
            return ErrorType.FILE

        # Validation errors
        if "validation" in error_msg or "invalid" in error_msg:
            return ErrorType.VALIDATION

        # Generation errors
        if "generation" in error_msg or "generate" in error_msg:
            return ErrorType.GENERATION

        return ErrorType.UNKNOWN

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error context to dictionary

        Returns:
            Dictionary representation
        """
        return {
            "stage": self.stage,
            "error_type": self.error_type.value,
            "error_message": str(self.exception),
            "exception_type": type(self.exception).__name__,
            "timestamp": self.timestamp,
            "traceback": self.traceback,
            "additional_info": self.additional_info
        }

    def get_short_description(self) -> str:
        """
        Get short error description

        Returns:
            Short description string
        """
        return f"[{self.error_type.value.upper()}] {type(self.exception).__name__}: {str(self.exception)[:100]}"
