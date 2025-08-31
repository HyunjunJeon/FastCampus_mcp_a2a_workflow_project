## Task Executor Agent

### Overview

The Task Executor Agent performs general-purpose automation by combining
code execution in a sandboxed environment and Notion workspace operations via
MCP tools. It is implemented as a LangGraph "ReAct" agent with an A2A-compatible
wrapper that standardizes inputs, streaming updates, and final results.

### Responsibilities

- Execute Python/JavaScript code in a secure sandbox (WebAssembly)
- Manage Notion content (create/update pages, append blocks, query databases)
- Orchestrate multi-step execution with retries and result aggregation
- Provide structured progress events and final outputs through A2A

### Not in Scope

- Browser automation or page interactions (use the Browser Agent)
- Long-running system-level jobs outside the sandbox

### Architecture

- LangGraph implementation: `task_executor_agent_lg.py`
  - Built with `create_react_agent`
  - Loads MCP tools (LangChain Sandbox, Notion) via configuration
  - Uses a detailed system prompt describing tool usage and constraints

- A2A wrapper: `task_executor_agent_a2a.py`
  - Normalizes inputs/outputs to the A2A protocol
  - Handles thread identifiers and request context
  - Emits streaming updates mapped from agent/tool events

- Entry point: `__main__.py`
  - Starts a Uvicorn server that exposes A2A endpoints

### Input and Output (A2A)

- Input (selected fields):
  - `messages`: array of chat messages; the first user message provides the
    task description and context
  - `code_to_execute`: optional source code for execution
  - `language`: `python` or `javascript` (default: `python`)
  - `notion_config`: parameters for Notion operations
  - `conversation_id` or `context_id`: used as the A2A thread identifier

- Streaming events handled by the wrapper:
  - `on_llm_stream` → incremental text updates
  - `on_chain_start` → node/task phase start
  - `on_tool_start` → tool execution start (e.g., sandbox, notion)
  - `code_execution` → code execution preview and metadata
  - `notion_operation` → Notion operation summary
  - Completion detection → final "completed" event

- Final output structure:
  - `status`: completed | working | failed
  - `text_content`: summarized execution result or last AI message
  - `data_content` (selected fields):
    - `final_result`: top-level outcome if provided
    - `code_outputs`: per-execution details (language, output, error, time)
    - `notion_operations`: normalized Notion actions and success flags
    - `file_operations`: created/modified artifacts reported by the agent
    - `execution_stats`: counts, timings, and success/failure breakdown
    - `tool_usage`: aggregated tool usage statistics
  - `metadata`: workflow phase, task type, timestamps

### Notion Parent Validation

When creating pages in Notion, provide a valid parent. The agent sanitizes and
expects one of the following parent forms:

- `parent.page_id`: hyphenated UUID
- `parent.database_id`: hyphenated UUID
- `parent.workspace`: true (fallback only when no specific parent is available)

If a 32-character UUID is provided, it should be converted to the hyphenated
format before use. Avoid non-UUID placeholders (e.g., "root"). Prefer adding
content via `append_block` with a `markdown` argument; if using `children`, they
must be valid Notion block objects, not raw strings.

### Code Execution Guidelines (Sandbox)

- WebAssembly sandbox does not capture `print()` output; return a value as the
  last expression to produce output
- Handle errors explicitly and keep code self-contained
- Keep memory and execution time bounded

### Configuration

Environment variables:
- `AGENT_HOST` (default: localhost or 0.0.0.0 in Docker)
- `AGENT_PORT` (default: 8003)
- `IS_DOCKER` (true/false)

### Run Locally

```bash
export PYTHONPATH="${PWD}/src"
uv run python -m agents.executor
```

### Files

- `__main__.py` – server startup
- `task_executor_agent_lg.py` – LangGraph agent (create_react_agent)
- `task_executor_agent_a2a.py` – A2A wrapper and server app builder

### Best Practices

- Prefer returning structured results for downstream processing
- Validate Notion parents and avoid raw `children` strings
- Keep steps small and verify success before moving on
- Capture and report artifacts and timings for observability

### Related Documentation

- `src/agents/AGENT.md` – Agents overview
- `src/agents/supervisor/AGENT.md` – Orchestration model

