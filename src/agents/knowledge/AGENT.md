## Knowledge Agent

### Overview

The Knowledge Agent manages memory operations using an MCP-backed memory
service (OpenMemory) and a LangGraph "ReAct" agent. It stores, retrieves,
updates, deletes, and summarizes information with semantic search and
tag/category filtering, while exposing an A2A-compatible interface for
standardized interactions.

### Responsibilities

- Store memories with categories, tags, and metadata
- Retrieve memories using semantic search and filters
- Update or delete existing memories while preserving history when applicable
- Provide operation history and normalized summaries for UX
- Emit structured progress updates and final results via A2A

### Not in Scope

- Browser automation or code execution (handled by Browser/Executor agents)
- Long-term external persistence beyond the configured memory backend

### Architecture

- LangGraph implementation: `knowledge_agent_lg.py`
  - Built with `create_react_agent`
  - Loads OpenMemory MCP tools (store/retrieve/search/delete/health)
  - Uses a system prompt tailored for memory lifecycle management

- A2A wrapper: `knowledge_agent_a2a.py`
  - Normalizes inputs/outputs into A2A format
  - Manages thread identifiers and maps streaming events
  - Produces consolidated final results with operation summaries

- Entry point: `__main__.py`
  - Starts a Uvicorn server exposing A2A endpoints

### Input and Output (A2A)

- Input (selected fields):
  - `messages`: array of chat messages; the first user message provides the
    request and intent
  - For explicit operations:
    - `operation`: `save` | `retrieve` | `update` | `delete` | `health`
    - `data`: content or structured payload (for save/update)
    - `query`: semantic search or delete criteria (for retrieve/delete)
  - `conversation_id` or `context_id`: used as the A2A thread identifier

- Streaming events handled by the wrapper:
  - `on_llm_stream` → incremental text updates
  - `on_chain_start` → node/phase start notifications
  - `on_tool_start` → memory tool execution start
  - Completion detection → final "completed" event

- Final output structure:
  - `status`: completed | working | failed
  - `text_content`: concise operation summary
  - `data_content` (selected fields):
    - `saved_memories`: newly stored items
    - `retrieved_memories`: query results with metadata
    - `deleted_memories`: removed items (inferred from operation history)
    - `operation_history`: raw chronological actions
    - `memory_operations`: normalized counts (saved/retrieved/deleted)
  - `metadata`: timestamps and auxiliary info

### Memory Model and Categories

Common categories include `user_info`, `task_history`, `preferences`, `context`,
`technical`, and `knowledge`. Apply multiple tags to improve retrieval
precision. Include timestamps, brief titles, and structured fields where
appropriate to enable high-quality semantic and tag-based search.

### Configuration

Environment variables:
- `AGENT_HOST` (default: localhost or 0.0.0.0 in Docker)
- `AGENT_PORT` (default: 8002)
- `IS_DOCKER` (true/false)

### Run Locally

```bash
export PYTHONPATH="${PWD}/src"
uv run python -m agents.knowledge
```

### Files

- `__main__.py` – server startup
- `knowledge_agent_lg.py` – LangGraph agent (create_react_agent)
- `knowledge_agent_a2a.py` – A2A wrapper and server app builder

### Best Practices

- Use descriptive titles and sufficient tags for retrieval
- Prefer structured JSON content for complex items
- Avoid sensitive secrets; anonymize where necessary
- Verify operations and include counts in results for observability

### Related Documentation

- `src/agents/AGENT.md` – Agents overview
- `src/agents/supervisor/AGENT.md` – Orchestration model

