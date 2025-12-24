"""Python wrapper that calls pyodide & deno for code execution.

This module is based on langchain-sandbox (Apache 2.0 License).
Original source: https://github.com/langchain-ai/langchain-sandbox

Copyright 2024 LangChain, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Modifications:
- Removed langchain-core dependencies (BaseTool, callbacks, etc.)
- Kept only core sandbox execution functionality
"""

import asyncio
import dataclasses
import json
import logging
import subprocess
import time

from typing import Any, Literal


logger = logging.getLogger(__name__)


Status = Literal["success", "error"]


@dataclasses.dataclass(kw_only=True)
class CodeExecutionResult:
    """Container for code execution results."""

    result: Any = None
    stdout: str | None = None
    stderr: str | None = None
    status: Status
    execution_time: float
    session_metadata: dict | None = None
    session_bytes: bytes | None = None

    @property
    def output(self) -> str | None:
        """Alias for stdout for backward compatibility."""
        return self.stdout

    @property
    def error(self) -> str | None:
        """Alias for stderr for backward compatibility."""
        return self.stderr


# Published package name
PKG_NAME = "jsr:@langchain/pyodide-sandbox@0.0.4"


def build_permission_flag(
    flag: str,
    *,
    value: bool | list[str],
) -> str | None:
    """Build a permission flag string based on the provided setting.

    Args:
        flag: The base permission flag (e.g., "--allow-read").
        value: Either a boolean (True for unrestricted access, False for no access)
                 or a list of allowed items.

    Returns:
        A string with the permission flag and items, or None if no permission should
        be added.
    """
    if value is True:
        return flag
    if isinstance(value, list) and value:
        return f"{flag}={','.join(value)}"
    return None


class BasePyodideSandbox:
    """Base class for PyodideSandbox implementations.

    This class provides the common initialization and configuration logic for both
    synchronous and asynchronous PyodideSandbox implementations.

    The sandbox leverages Deno's security model to create a secure runtime for
    executing untrusted Python code. It works by spawning a Deno subprocess that loads
    Pyodide (Python compiled to WebAssembly) and executes the provided code in an
    isolated environment.

    Security features:
    - Configurable permissions for file system, network, and environment access
    - Support for execution timeouts to prevent infinite loops
    - Memory usage monitoring
    - Process isolation via Deno's security sandbox
    """

    def __init__(
        self,
        *,
        stateful: bool = False,
        allow_env: list[str] | bool = False,
        allow_read: list[str] | bool = False,
        allow_write: list[str] | bool = False,
        allow_net: list[str] | bool = False,
        allow_run: list[str] | bool = False,
        allow_ffi: list[str] | bool = False,
        node_modules_dir: str = "auto",
        skip_deno_check: bool = False,
    ) -> None:
        """Initialize the sandbox with specific Deno permissions.

        Args:
            stateful: Whether to use a stateful session.
            allow_env: Environment variable access configuration.
            allow_read: File system read access configuration.
            allow_write: File system write access configuration.
            allow_net: Network access configuration.
            allow_run: Subprocess execution configuration.
            allow_ffi: Foreign Function Interface access configuration.
            node_modules_dir: Directory for Node.js modules.
            skip_deno_check: If True, skip the check for Deno installation.
        """
        self.stateful = stateful
        self.permissions = []

        if not skip_deno_check:
            try:
                subprocess.run(
                    ["deno", "--version"],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                msg = "Deno is installed, but running it failed."
                raise RuntimeError(msg) from e
            except FileNotFoundError as e:
                msg = "Deno is not installed or not in PATH."
                raise RuntimeError(msg) from e

        perm_defs = [
            ("--allow-env", allow_env, None),
            ("--allow-read", allow_read, ["node_modules"]),
            ("--allow-write", allow_write, ["node_modules"]),
            ("--allow-net", allow_net, None),
            ("--allow-run", allow_run, None),
            ("--allow-ffi", allow_ffi, None),
        ]

        self.permissions = []
        for flag, value, defaults in perm_defs:
            perm = build_permission_flag(flag, value=value)
            if perm is None and defaults is not None:
                default_value = ",".join(defaults)
                perm = f"{flag}={default_value}"
            if perm:
                self.permissions.append(perm)

        self.permissions.append(f"--node-modules-dir={node_modules_dir}")

    def _build_command(
        self,
        code: str,
        *,
        session_bytes: bytes | None = None,
        session_metadata: dict | None = None,
        memory_limit_mb: int | None = None,
    ) -> list[str]:
        """Build the Deno command with all necessary arguments.

        Args:
            code: The Python code to execute
            session_bytes: Optional session state bytes
            session_metadata: Optional session metadata
            memory_limit_mb: Optional memory limit in MB

        Returns:
            List of command arguments for subprocess execution
        """
        cmd = [
            "deno",
            "run",
        ]

        cmd.extend(self.permissions)

        if memory_limit_mb is not None and memory_limit_mb > 0:
            cmd.append(f"--v8-flags=--max-old-space-size={memory_limit_mb}")

        cmd.append(PKG_NAME)
        cmd.extend(["-c", code])

        if self.stateful:
            cmd.extend(["-s"])

        if session_bytes:
            bytes_array = list(session_bytes)
            cmd.extend(["-b", json.dumps(bytes_array)])

        if session_metadata:
            cmd.extend(["-m", json.dumps(session_metadata)])

        return cmd


class PyodideSandbox(BasePyodideSandbox):
    """Asynchronous implementation of PyodideSandbox.

    This class provides an asynchronous interface for executing Python code in a
    sandboxed Deno environment using Pyodide.
    """

    async def execute(
        self,
        code: str,
        *,
        session_bytes: bytes | None = None,
        session_metadata: dict | None = None,
        timeout_seconds: float | None = None,
        memory_limit_mb: int | None = None,
    ) -> CodeExecutionResult:
        """Execute Python code asynchronously in a sandboxed Deno subprocess.

        Args:
            code: The Python code to execute in the sandbox
            session_bytes: Optional bytes containing session state
            session_metadata: Optional metadata for session state
            timeout_seconds: Maximum execution time in seconds
            memory_limit_mb: Maximum memory usage in MB

        Returns:
            CodeExecutionResult containing execution results and metadata
        """
        start_time = time.time()
        stdout = ""
        stderr = ""
        result = None
        status: Literal["success", "error"] = "success"

        cmd = self._build_command(
            code,
            session_bytes=session_bytes,
            session_metadata=session_metadata,
            memory_limit_mb=memory_limit_mb,
        )

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_seconds,
            )
            stdout = stdout_bytes.decode("utf-8", errors="replace")

            if stdout:
                full_result = json.loads(stdout)
                stdout = full_result.get("stdout", None)
                stderr = full_result.get("stderr", None)
                result = full_result.get("result", None)
                status = "success" if full_result.get("success", False) else "error"
                session_metadata = full_result.get("sessionMetadata", None)
                session_bytes_array = full_result.get("sessionBytes", None)
                session_bytes = (
                    bytes(session_bytes_array) if session_bytes_array else None
                )
            else:
                stderr = stderr_bytes.decode("utf-8", errors="replace")
                status = "error"
        except TimeoutError:
            process.kill()
            await process.wait()
            status = "error"
            stderr = f"Execution timed out after {timeout_seconds} seconds"
        except asyncio.CancelledError:
            pass
        end_time = time.time()

        return CodeExecutionResult(
            status=status,
            execution_time=end_time - start_time,
            stdout=stdout or None,
            stderr=stderr or None,
            result=result,
            session_metadata=session_metadata,
            session_bytes=session_bytes,
        )


class SyncPyodideSandbox(BasePyodideSandbox):
    """Synchronous version of PyodideSandbox.

    This class provides a synchronous interface to the PyodideSandbox functionality.
    """

    def execute(
        self,
        code: str,
        *,
        session_bytes: bytes | None = None,
        session_metadata: dict | None = None,
        timeout_seconds: float | None = None,
        memory_limit_mb: int | None = None,
    ) -> CodeExecutionResult:
        """Execute Python code synchronously in a sandboxed Deno subprocess.

        Args:
            code: The Python code to execute in the sandbox
            session_bytes: Optional bytes containing session state
            session_metadata: Optional metadata for session state
            timeout_seconds: Maximum execution time in seconds
            memory_limit_mb: Maximum memory usage in MB

        Returns:
            CodeExecutionResult containing execution results and metadata
        """
        start_time = time.time()
        stdout = ""
        result = None
        stderr: str
        status: Literal["success", "error"]

        cmd = self._build_command(
            code,
            session_bytes=session_bytes,
            session_metadata=session_metadata,
            memory_limit_mb=memory_limit_mb,
        )

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=False,
                timeout=timeout_seconds,
                check=False,
            )

            stdout_bytes = process.stdout
            stderr_bytes = process.stderr

            stdout = stdout_bytes.decode("utf-8", errors="replace")

            if stdout:
                full_result = json.loads(stdout)
                stdout = full_result.get("stdout", None)
                stderr = full_result.get("stderr", None)
                result = full_result.get("result", None)
                status = "success" if full_result.get("success", False) else "error"
                session_metadata = full_result.get("sessionMetadata", None)
                session_bytes_array = full_result.get("sessionBytes", None)
                session_bytes = (
                    bytes(session_bytes_array) if session_bytes_array else None
                )
            else:
                stderr = stderr_bytes.decode("utf-8", errors="replace")
                status = "error"

        except subprocess.TimeoutExpired:
            status = "error"
            stderr = f"Execution timed out after {timeout_seconds} seconds"

        end_time = time.time()

        return CodeExecutionResult(
            status=status,
            execution_time=end_time - start_time,
            stdout=stdout or None,
            stderr=stderr or None,
            result=result,
            session_metadata=session_metadata,
            session_bytes=session_bytes,
        )
