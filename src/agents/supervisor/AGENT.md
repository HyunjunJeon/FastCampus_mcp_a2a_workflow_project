# Supervisor Agent

## Overview

The Supervisor Agent is the central orchestrator of the multi-agent workflow automation system, responsible for coordinating task execution across all worker agents.

## Responsibilities

### Workflow Orchestration

- Receives user requests and determines workflow patterns
- Coordinates execution across multiple worker agents
- Manages task state and progress tracking
- Handles workflow completion and result aggregation

### Workflow Patterns

The Supervisor implements three main patterns:

1. **DATA_ONLY**: Data collection without analysis
2. **DATA_ANALYSIS**: Data collection followed by analysis
3. **FULL_WORKFLOW**: Complete workflow including trading operations

## Architecture

### State Management

- Uses `TaskManager` for tracking workflow progress
- Maintains metadata including workflow phase and current step
- Implements state transitions based on task outcomes

### A2A Communication

- Acts as primary A2A client
- Manages connections to all worker agents
- Handles request routing and response processing

## Implementation Details

- **File**: `supervisor_agent_a2a.py`
- **Base Class**: Inherits from `BaseGraphAgent`
- **Nodes**: `process_input`, `data_collection`, `analysis`, `trading`, `complete`
- **State**: Manages messages, task manager, and workflow metadata

## Configuration

Requires environment variables for agent URLs:

- `PLANNER_URL`
- `DATA_COLLECTOR_URL`
- `ANALYSIS_URL`
- `TRADING_URL`

-----

## =� Related Documentation

### Navigation

- [**Back to Agent Implementations**](../Agents.md) - Return to agents documentation
- [**Source Architecture**](../../Agents.md) - Return to source code documentation
- [**Main Architecture**](../../../Agents.md) - Return to main documentation
