## Browser Agent

### Overview

The Browser Agent performs web automation and information extraction using
Playwright MCP tools, orchestrated through a LangGraph "ReAct" agent and an
A2A-compatible wrapper. It can navigate to pages, fill forms, interact with
elements, capture screenshots, and extract structured data in a sequential and
reliable manner.

### Responsibilities

- Navigate to target web pages and verify load completion
- Interact with page elements (click, type, select)
- Extract structured data from pages
- Capture screenshots for auditing or debugging
- Report progress and final results via the A2A protocol

### Not in Scope

- Arbitrary code execution or local file operations (use the Executor Agent)
- Non-deterministic parallel browser actions (the agent enforces sequential
  execution)

### Architecture

- LangGraph implementation: `browser_use_agent_lg.py`
  - Built with `create_react_agent`
  - Loads Playwright MCP tools through MCP configuration
  - Uses a system prompt that enforces strictly sequential actions

- A2A wrapper: `browser_use_agent_a2a.py`
  - Normalizes inputs/outputs to the A2A protocol
  - Maps streaming events to A2A "working" updates
  - Produces a consolidated final A2A result (status, text, data, metadata)

- Entry point: `__main__.py`
  - Starts a Uvicorn server exposing A2A endpoints

### Input and Output (A2A)

- Input (selected fields):
  - `messages`: array of chat messages; the first user message provides the
    request
  - `target_url`: page to visit (optional)
  - `extraction_targets`: selectors or instructions for data extraction
  - `form_data`: mapping of field locators to values (for form scenarios)
  - `conversation_id` or `context_id`: used as the A2A thread identifier

- Streaming events (mapped by the A2A wrapper):
  - `on_llm_stream` → incremental text updates
  - `on_chain_start` → node start notifications
  - `on_tool_start` → tool execution notifications (Playwright)
  - `browser_action` → custom browser action events from Playwright MCP
  - Completion detection → final "completed" event

- Final output structure:
  - `status`: completed | working | failed
  - `text_content`: last AI message or a concise summary
  - `data_content`: extracted data, executed actions, screenshots metadata,
    final URL, execution time
  - `metadata`: workflow phase, task type, timestamps

### Sequential Execution Policy

All browser operations are performed strictly in sequence:

1) Navigate → 2) Wait → 3) Find element → 4) Interact → 5) Verify → 6) Extract.
This prevents race conditions and ensures deterministic behavior with dynamic
pages.

### Configuration

Environment variables:

- `AGENT_HOST` (default: localhost or 0.0.0.0 in Docker)
- `AGENT_PORT` (default: 8005)
- `IS_DOCKER` (true/false)

### Run Locally

```bash
export PYTHONPATH="${PWD}/src"
uv run python -m agents.browser
```

### Files

- `__main__.py` – server startup
- `browser_use_agent_lg.py` – LangGraph agent (create_react_agent)
- `browser_use_agent_a2a.py` – A2A wrapper and server app builder

### Best Practices

- Always wait for page readiness between actions
- Verify element presence before interaction
- Use explicit waits for dynamic content
- Keep extraction targets specific and structured
- Capture screenshots to support debugging when needed

### Related Documentation

- `src/agents/AGENT.md` – Agents overview
- `src/agents/supervisor/AGENT.md` – Orchestration model
