import multiprocessing
import time
import traceback
import io
import json
import psutil
from typing import Dict, Any, Tuple
from contextlib import redirect_stdout, redirect_stderr
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FuturesTimeoutError
import atexit


def _execute_function(code: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute function in a worker process.
    This runs in the worker process from the pool.
    """
    try:
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Create restricted globals
        restricted_globals = {
            "__builtins__": __builtins__,
            "json": json,
        }

        # Execute the user code to define the function
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, restricted_globals)

            # Find the function (assume single function definition)
            func = None
            for name, obj in restricted_globals.items():
                if callable(obj) and not name.startswith("_"):
                    func = obj
                    break

            if func is None:
                raise ValueError("No callable function found in code")

            # Execute the function
            start_time = time.time()
            result = func(**params)
            execution_time = (time.time() - start_time) * 1000  # Convert to ms

        # Get memory usage
        process = psutil.Process()
        memory_mb = process.memory_info().rss / (1024 * 1024)

        return {
            "status": "success",
            "output": result,
            "execution_time_ms": execution_time,
            "memory_used_mb": memory_mb,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue(),
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "traceback": traceback.format_exc(),
        }


class FunctionExecutor:
    """Execute Python functions in a process pool with resource limits."""

    def __init__(self, max_workers: int = None):
        """
        Initialize the executor with a process pool.

        Args:
            max_workers: Maximum number of worker processes.
                        Defaults to min(32, cpu_count() + 4)
        """
        if max_workers is None:
            # Default: min(32, cpu_count + 4) - good balance for I/O and CPU
            max_workers = min(32, (multiprocessing.cpu_count() or 1) + 4)

        self.max_workers = max_workers
        self.pool = ProcessPoolExecutor(max_workers=max_workers)

        # Register cleanup on exit
        atexit.register(self.shutdown)

        print(f"✓ Process pool initialized with {max_workers} workers")

    def execute(
        self,
        code: str,
        params: Dict[str, Any],
        timeout_seconds: int,
        memory_limit_mb: int
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Execute a function with resource limits using the process pool.

        Args:
            code: Python function code as string
            params: Dictionary of parameters to pass to function
            timeout_seconds: Maximum execution time
            memory_limit_mb: Maximum memory usage (currently for monitoring only)

        Returns:
            Tuple of (status, result_dict)
            status: "success", "error", or "timeout"
            result_dict: Contains output, execution metrics, or error details
        """
        try:
            # Submit task to process pool
            future = self.pool.submit(_execute_function, code, params)

            # Wait for result with timeout
            result = future.result(timeout=timeout_seconds)

            # Extract status
            status = result.pop("status")

            # Check memory limit (warning only for now)
            if "memory_used_mb" in result and result["memory_used_mb"] > memory_limit_mb:
                result["memory_warning"] = f"Memory usage ({result['memory_used_mb']:.2f}MB) exceeded limit ({memory_limit_mb}MB)"

            return status, result

        except FuturesTimeoutError:
            # Timeout occurred
            # Note: The worker process will continue running until task completes
            # but we return timeout to the caller immediately
            return "timeout", {
                "error_message": f"Execution exceeded timeout of {timeout_seconds} seconds",
                "timeout_seconds": timeout_seconds
            }
        except Exception as e:
            # Unexpected error
            return "error", {
                "error_message": f"Executor error: {str(e)}",
                "traceback": traceback.format_exc()
            }

    def shutdown(self, wait: bool = True):
        """Shutdown the process pool."""
        if hasattr(self, 'pool'):
            self.pool.shutdown(wait=wait)
            print("✓ Process pool shut down")


# Global executor instance
executor = FunctionExecutor()
