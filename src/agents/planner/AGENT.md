# Planner Agent

## Overview

The Planner Agent is responsible for decomposing complex user requests into structured, executable plans for the multi-agent system.

## Responsibilities

### Task Decomposition

- Analyzes complex user requests
- Breaks down tasks into step-by-step execution plans
- Identifies appropriate agents for each step
- Generates structured JSON plans

### Plan Structure

Each plan must contain:

```json
{
  "steps": [
    {
      "step_number": 1,
      "agent_to_use": "data_collector",
      "prompt": "Collect data from source X"
    }
  ]
}
```

## Architecture

### State Management

- Maintains conversation history
- Tracks planning context
- Preserves user intent throughout decomposition

### Planning Strategy

- Semantic analysis of user requests
- Agent capability matching
- Dependency resolution between steps
- Optimization of execution order

## Implementation Details

- **Files**:
  - `planner_agent_a2a.py` - A2A server implementation
  - `planner_agent_lg.py` - LangGraph implementation
- **Base Class**: Inherits from `BaseGraphAgent`
- **Nodes**: `plan_generation`, `plan_validation`, `plan_output`
- **Output**: Structured JSON plan

## Best Practices

### Plan Generation

- Keep prompts clear and specific
- Ensure agent assignments match capabilities
- Validate plan structure before output
- Consider execution dependencies

### Error Handling

- Validate user request completeness
- Handle ambiguous requests gracefully
- Provide fallback planning strategies

-----

## =� Related Documentation

### Navigation

- [**Back to Agent Implementations**](../Agents.md) - Return to agents documentation
- [**Source Architecture**](../../Agents.md) - Return to source code documentation
- [**Main Architecture**](../../../Agents.md) - Return to main documentation
