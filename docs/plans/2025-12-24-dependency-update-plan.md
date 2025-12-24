# UV Dependencies Update Plan

**Date**: 2025-12-24
**Author**: Claude Code
**Status**: COMPLETED

## Overview

이 계획은 프로젝트의 모든 의존성을 최신 버전으로 업데이트하고, 코드 호환성을 검증하는 작업을 다룹니다.

### Version Changes Summary

| Package | Current | Target | Risk Level | Notes |
|---------|---------|--------|------------|-------|
| a2a-sdk | 0.3.3 | 0.3.22 | MEDIUM | 19 versions behind, API changes possible |
| langchain-mcp-adapters | 0.1.9 | 0.2.1 | HIGH | Minor version bump (0.1 -> 0.2) |
| openai | 1.101.0 | 2.14.0 | HIGH | Major version change |
| langgraph-checkpoint | 2.1.1 | 3.0.1 | HIGH | Major version change |
| langgraph | 0.6.6 | 0.6.11 | LOW | Patch updates |
| langchain-openai | 0.3.31 | 0.3.35 | LOW | Patch updates |
| mcp | 1.13.1 | 1.25.0 | MEDIUM | Significant minor update |
| pydantic | 2.11.7 | 2.12.5 | LOW | Minor update |

---

## Phase 1: Preparation (Pre-Update)

### Task 1.1: Create Backup Branch

**File**: N/A (Git operations)
**Verification**: Branch exists and is up to date

```bash
# Execute from project root
git checkout -b feature/dependency-update-2025-12-24
git push -u origin feature/dependency-update-2025-12-24
```

### Task 1.2: Document Current Working State

**File**: N/A
**Verification**: All tests pass on current version

```bash
# Run existing tests to establish baseline
uv run pytest tests/ -v --tb=short

# Run lint check
uv run ruff check src/

# Document any existing issues
```

---

## Phase 2: Core Dependency Updates

### Task 2.1: Update pyproject.toml

**File**: `/pyproject.toml`
**Verification**: `uv lock` succeeds without errors

Replace the dependencies section:

```toml
# BEFORE
dependencies = [
    "a2a-sdk[grpc,http-server]>=0.3.3",
    "fastmcp>=2.11.3",
    "langchain>=0.3.27",
    "langchain-mcp-adapters>=0.1.9",
    "langchain-openai>=0.3.31",
    "langchain-sandbox>=0.0.6",
    "langgraph>=0.6.6",
    "langgraph-supervisor>=0.0.29",
    "python-dotenv>=1.1.1",
    "pytz>=2025.2",
    "structlog>=25.4.0",
    "uvloop>=0.21.0",
]

# AFTER
dependencies = [
    "a2a-sdk[grpc,http-server]>=0.3.22",
    "fastmcp>=2.14.1",
    "langchain>=0.3.27",
    "langchain-mcp-adapters>=0.2.0",
    "langchain-openai>=0.3.35",
    "langchain-sandbox>=0.0.6",
    "langgraph>=0.6.11",
    "langgraph-supervisor>=0.0.29",
    "python-dotenv>=1.2.1",
    "pytz>=2025.2",
    "structlog>=25.4.0",
    "uvloop>=0.21.0",
]
```

### Task 2.2: Update Lock File

**File**: `uv.lock`
**Verification**: Lock file regenerated successfully

```bash
# Remove old lock and regenerate
rm uv.lock
uv lock

# Verify lock succeeded
echo $?  # Should be 0
```

### Task 2.3: Install Updated Dependencies

**File**: N/A
**Verification**: All packages installed without conflicts

```bash
uv sync
uv sync --dev
```

---

## Phase 3: Code Compatibility Fixes

### Task 3.1: A2A SDK Compatibility Check (HIGH PRIORITY)

**Affected Files**:
- `src/a2a_integration/a2a_lg_client_utils.py`
- `src/base/a2a_interface.py`
- `src/a2a_integration/a2a_lg_server_utils.py`
- `src/a2a_integration/executor.py`
- `src/agents/*/\*_agent_a2a.py` (6 files)

**Verification**: Import all a2a modules without errors

```python
# Test script: tests/test_a2a_imports.py
"""Test A2A SDK import compatibility."""
import pytest

def test_a2a_client_imports():
    """Test all A2A client imports work."""
    from a2a.client import (
        A2ACardResolver,
        A2AClientError,
        ClientConfig,
        ClientFactory,
    )
    from a2a.client.auth.credentials import CredentialService
    from a2a.client.auth.interceptor import AuthInterceptor
    from a2a.client.helpers import create_text_message_object
    assert True

def test_a2a_types_imports():
    """Test all A2A types imports work."""
    from a2a.types import (
        AgentCard,
        DataPart,
        FilePart,
        FileWithBytes,
        FileWithUri,
        Message,
        Part,
        Role,
        TextPart,
        TransportProtocol,
        TaskQueryParams,
    )
    assert True
```

**Potential Breaking Changes to Check**:
1. `ClientConfig` parameter changes
2. `TransportProtocol` enum values
3. `Message` constructor signature
4. `TaskQueryParams` fields

### Task 3.2: langchain-mcp-adapters Compatibility (HIGH PRIORITY)

**Affected Files**:
- `src/base/base_graph_agent.py:6-11`
- `src/mcp_config_module/mcp_config.py`
- `src/agents/browser/browser_use_agent_lg.py`

**Verification**: MCP client initialization works

**Current Code** (`src/base/base_graph_agent.py:6-11`):
```python
from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
)
from langchain_mcp_adapters.sessions import (
    StreamableHttpConnection,
)
```

**Potential Fix** (if imports changed in 0.2.x):
```python
# Check if import paths changed
# Option A: Same imports (likely compatible)
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection

# Option B: If restructured in 0.2.x
# from langchain_mcp_adapters import MultiServerMCPClient
# from langchain_mcp_adapters.transport import StreamableHttpConnection
```

**Test Script**:
```python
# tests/test_mcp_imports.py
"""Test MCP adapter import compatibility."""
import pytest

def test_mcp_client_import():
    """Test MultiServerMCPClient import."""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    assert MultiServerMCPClient is not None

def test_mcp_session_import():
    """Test StreamableHttpConnection import."""
    from langchain_mcp_adapters.sessions import StreamableHttpConnection
    assert StreamableHttpConnection is not None

@pytest.mark.asyncio
async def test_mcp_client_initialization():
    """Test MCP client can be instantiated."""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_mcp_adapters.sessions import StreamableHttpConnection

    connections = {
        "test": StreamableHttpConnection(url="http://localhost:8080/mcp")
    }
    client = MultiServerMCPClient(connections=connections)
    assert client is not None
```

### Task 3.3: LangGraph Checkpoint Migration (HIGH PRIORITY)

**Affected Files**:
- `src/base/base_graph_agent.py`
- Any files using `BaseCheckpointSaver`

**Verification**: Graph compilation with checkpointer works

**Current Code**:
```python
from langgraph.checkpoint.base import BaseCheckpointSaver
```

**Check Required**:
```python
# tests/test_langgraph_imports.py
"""Test LangGraph import compatibility."""
import pytest

def test_checkpoint_import():
    """Test checkpoint imports."""
    from langgraph.checkpoint.base import BaseCheckpointSaver
    assert BaseCheckpointSaver is not None

def test_graph_imports():
    """Test core graph imports."""
    from langgraph.graph import StateGraph
    from langgraph.graph.state import CompiledStateGraph
    from langgraph.cache.base import BaseCache
    from langgraph.store.base import BaseStore
    from langgraph.types import RetryPolicy
    assert True

def test_prebuilt_imports():
    """Test prebuilt agent imports."""
    from langgraph.prebuilt import create_react_agent
    assert create_react_agent is not None
```

### Task 3.4: OpenAI Package Compatibility (INDIRECT)

**Note**: This project uses `langchain-openai` which wraps the `openai` package.
Direct `openai` imports are NOT found in the codebase.

**Verification**: langchain-openai works with new openai version

```python
# tests/test_langchain_openai.py
"""Test LangChain OpenAI integration."""
import pytest
import os

def test_openai_model_import():
    """Test ChatOpenAI import."""
    from langchain_openai import ChatOpenAI
    assert ChatOpenAI is not None

@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
def test_openai_model_instantiation():
    """Test ChatOpenAI can be instantiated."""
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    assert model is not None
```

---

## Phase 4: Integration Testing

### Task 4.1: Run Unit Tests

**Verification**: All existing tests pass

```bash
uv run pytest tests/ -v --tb=short
```

### Task 4.2: Agent Import Tests

**Verification**: All agents can be imported

```python
# tests/test_agent_imports.py
"""Test all agent imports work after update."""
import pytest

def test_supervisor_import():
    from src.agents.supervisor.supervisor_agent_lg import create_supervisor_agent
    assert create_supervisor_agent is not None

def test_planner_import():
    from src.agents.planner.planner_agent_lg import create_planner_agent
    assert create_planner_agent is not None

def test_executor_import():
    from src.agents.executor.task_executor_agent_lg import TaskExecutorAgent
    assert TaskExecutorAgent is not None

def test_browser_import():
    from src.agents.browser.browser_use_agent_lg import BrowserUseAgent
    assert BrowserUseAgent is not None

def test_knowledge_import():
    from src.agents.knowledge.knowledge_agent_lg import KnowledgeAgent
    assert KnowledgeAgent is not None
```

### Task 4.3: A2A Client Integration Test

**Verification**: A2A client can connect and communicate

```python
# tests/test_a2a_integration.py
"""Test A2A client integration after update."""
import pytest
from src.a2a_integration.a2a_lg_client_utils import (
    A2AClientManager,
    A2AMessageEngine,
    TextResponse,
)

def test_client_manager_instantiation():
    """Test A2AClientManager can be created."""
    manager = A2AClientManager(
        base_url="http://localhost:8000",
        streaming=False,
    )
    assert manager is not None
    assert manager.engine is not None

def test_message_engine_instantiation():
    """Test A2AMessageEngine can be created."""
    engine = A2AMessageEngine(
        base_url="http://localhost:8000",
        streaming=False,
    )
    assert engine is not None
```

### Task 4.4: Lint and Type Check

**Verification**: No new lint errors introduced

```bash
# Run ruff check
uv run ruff check src/

# Fix any auto-fixable issues
uv run ruff check src/ --fix

# Format code
uv run ruff format src/
```

---

## Phase 5: Docker Integration Testing

### Task 5.1: Build Docker Images

**Verification**: All images build successfully

```bash
docker compose -f docker-compose-full.yml build
```

### Task 5.2: Start Services

**Verification**: All services start and pass health checks

```bash
./1-run-docker.sh start

# Wait for services to be healthy
sleep 30

# Check service status
docker compose -f docker-compose-full.yml ps
```

### Task 5.3: End-to-End Test

**Verification**: Supervisor can communicate with all agents

```bash
# Test agent card retrieval
curl http://localhost:8000/.well-known/agent-card.json
curl http://localhost:8001/.well-known/agent-card.json
curl http://localhost:8004/.well-known/agent-card.json
curl http://localhost:8005/.well-known/agent-card.json
curl http://localhost:8006/.well-known/agent-card.json
```

---

## Phase 6: Cleanup and Documentation

### Task 6.1: Update CLAUDE.md if Needed

**File**: `CLAUDE.md`
**Verification**: Documentation reflects any API changes

If any import paths or API usage patterns changed, update the relevant sections.

### Task 6.2: Commit Changes

**Verification**: Clean commit history

```bash
git add pyproject.toml uv.lock
git add src/  # Only if code changes were needed
git commit -m "chore: Update dependencies to latest versions

- a2a-sdk: 0.3.3 -> 0.3.22
- langchain-mcp-adapters: 0.1.9 -> 0.2.0
- langgraph: 0.6.6 -> 0.6.11
- langchain-openai: 0.3.31 -> 0.3.35
- fastmcp: 2.11.3 -> 2.14.1
- python-dotenv: 1.1.1 -> 1.2.1

All tests pass, no breaking changes found."
```

---

## Rollback Plan

If critical issues are found:

```bash
# Restore original pyproject.toml
git checkout main -- pyproject.toml

# Regenerate lock file with original versions
rm uv.lock
uv lock
uv sync

# Verify rollback
uv run pytest tests/ -v
```

---

## Risk Assessment

### High Risk Items
1. **langchain-mcp-adapters 0.2.x**: Minor version bump may change import paths or API
2. **langgraph-checkpoint 3.x**: Major version change may affect checkpointing behavior
3. **openai 2.x**: Major version, but langchain-openai abstracts this

### Mitigation Strategies
1. Run comprehensive import tests before proceeding
2. Test each agent individually after update
3. Keep rollback branch ready
4. Test Docker builds early in the process

---

## Success Criteria

- [ ] All dependencies updated to latest versions
- [ ] `uv lock` completes without errors
- [ ] `uv sync` installs all packages
- [ ] All import tests pass
- [ ] All unit tests pass
- [ ] All agents start successfully
- [ ] Docker images build successfully
- [ ] End-to-end communication works
- [ ] No new lint warnings/errors

---

## Estimated Time

| Phase | Estimated Time |
|-------|---------------|
| Phase 1: Preparation | 10 min |
| Phase 2: Dependency Updates | 15 min |
| Phase 3: Code Compatibility | 30-60 min |
| Phase 4: Integration Testing | 20 min |
| Phase 5: Docker Testing | 30 min |
| Phase 6: Cleanup | 10 min |
| **Total** | **2-2.5 hours** |

---

## Appendix: Full Dependency Diff

```
Update a2a-sdk v0.3.3 -> v0.3.22
Update anyio v4.10.0 -> v4.12.0
Update attrs v25.3.0 -> v25.4.0
Update authlib v1.6.3 -> v1.6.6
Update cachetools v5.5.2 -> v6.2.4
Update certifi v2025.8.3 -> v2025.11.12
Update cffi v1.17.1 -> v2.0.0
Update click v8.2.1 -> v8.3.1
Update cryptography v45.0.6 -> v46.0.3
Update cyclopts v3.23.0 -> v4.4.1
Update dnspython v2.7.0 -> v2.8.0
Update fastapi v0.116.1 -> v0.127.0
Update fastmcp v2.11.3 -> v2.14.1
Update google-api-core v2.25.1 -> v2.28.1
Update google-auth v2.40.3 -> v2.45.0
Update grpcio v1.74.0 -> v1.76.0
Update langchain-core v0.3.74 -> v0.3.81
Update langchain-mcp-adapters v0.1.9 -> v0.2.0
Update langchain-openai v0.3.31 -> v0.3.35
Update langgraph v0.6.6 -> v0.6.11
Update langgraph-checkpoint v2.1.1 -> v3.0.1
Update langsmith v0.4.17 -> v0.5.0
Update mcp v1.13.1 -> v1.25.0
Update openai v1.101.0 -> v2.14.0
Update pydantic v2.11.7 -> v2.12.5
Update pytest v8.4.1 -> v9.0.2
Update python-dotenv v1.1.1 -> v1.2.1
Update ruff v0.12.10 -> v0.14.10
```
