# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a three-layer AI Agent requirement processing system (三层AI Agent需求处理系统) that transforms vague user requirements into structured PRD documents and UI design proposals through a coordinated workflow.

**Tech Stack**: LangChain, LangGraph, Claude (Anthropic), Python 3.8+

**Core Workflow**: User Input → Agent 1 (Requirement Clarification) → Agent 2 (PRD Generation) → Agent 3 (Prototype Design)

## Environment Setup

**CRITICAL**: `WORKSPACE_PATH` and `ANTHROPIC_API_KEY` must be set before running any code.

```bash
# Set the workspace path environment variable (required)
export WORKSPACE_PATH=/path/to/project

# Set Anthropic API Key (required)
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## Running Tests

All tests require environment variables to be set first.

```bash
# Set environment variables
export WORKSPACE_PATH=$(pwd)
export ANTHROPIC_API_KEY="your-api-key"

# Test agent construction only
python tests/simple_test.py

# Test step-by-step workflow execution
python tests/test_step_by_step.py

# Test complete workflow end-to-end
python tests/test_complete_workflow.py

# Test workflow coordinator functions
python tests/test_workflow.py
```

## Architecture Overview

### Three-Layer Agent System

The system consists of three specialized agents that work sequentially:

1. **Agent 1: Requirement Clarifier** (`agent1_requirement_clarifier.py`)
   - Converts vague user ideas into structured requirement summaries
   - Uses 5W2H framework for intelligent questioning
   - Supports multi-turn dialogue with 60-message window
   - Classifies requirements into 5 types: growth/feature/optimization/strategy/data

2. **Agent 2: PRD Builder** (`agent2_prd_builder.py`)
   - Transforms requirement summaries into complete PRD documents
   - Supports 5 PRD templates based on requirement type
   - Generates user stories, acceptance criteria, risk analysis

3. **Agent 3: Prototype Assistant** (`agent3_prototype_assistant.py`)
   - Generates UI design proposals from PRD documents
   - Creates page lists, detailed descriptions, AI drawing prompts
   - Provides design system recommendations (colors, fonts, components)
   - Uses 80-message window for complex design discussions

### Workflow Coordination

**WorkflowCoordinator** (`workflow_coordinator.py`) orchestrates the three agents:
- **Full mode**: Executes all three agents sequentially with automatic data passing
- **Stage modes**: Execute individual agents (stage1, stage2, or stage3)
- **Interactive mode**: Allows human review between stages

Key coordinator methods:
- `run_full_workflow()` - Complete three-stage pipeline
- `run_stage1_only()`, `run_stage2_only()`, `run_stage3_only()` - Individual stages
- `continue_stage1()` - Multi-turn conversation support for Agent 1

### Memory Management

**Memory Architecture** (`storage/memory/memory_saver.py`):
- Primary: PostgreSQL-based checkpointing (via LangGraph PostgresSaver)
- Fallback: In-memory checkpointing (MemorySaver) if DB unavailable
- Automatic retry logic with 15-second timeout per attempt
- Thread-based isolation: each agent uses `{thread_id}_agent{N}` namespace

**Message Windows**:
- Agent 1: 60 messages (30 turns) - needs more dialogue rounds
- Agent 2: 60 messages (30 turns)
- Agent 3: 80 messages (40 turns) - complex design discussions
- Implemented via `_windowed_messages()` reducer in AgentState

### Agent Construction Pattern

All agents follow this pattern in their `build_agent()` function:
1. Load config from `config/agent{N}_config.json`
2. Read `ANTHROPIC_API_KEY` from environment
3. Create ChatAnthropic with model configuration (temperature, max_tokens, timeout)
4. Configure extended thinking mode if enabled in config
5. Use `create_agent()` from LangChain with:
   - Model + system prompt from config
   - Empty tools list (no tool calling)
   - Memory checkpointer from `storage.memory.memory_saver.get_memory_saver()`
   - Custom AgentState with message windowing via `_windowed_messages()` reducer

### Configuration System

Each agent has a JSON config file in `config/` with these fields:
- `config.model`: Model ID (e.g., "claude-sonnet-4-5", "claude-opus-4")
- `config.temperature`: Randomness (0.6-0.7 recommended)
- `config.top_p`: Nucleus sampling (0.9)
- `config.max_completion_tokens`: Max output tokens (8000-12000)
- `config.timeout`: Request timeout in seconds (600)
- `config.thinking`: Enable/disable extended thinking mode ("enabled"/"disabled")
- `sp`: System prompt (extensive, defines entire agent behavior including 5W2H frameworks)

## Working with the Workflow

### Using WorkflowCoordinator

```python
from src.agents.workflow_coordinator import run_requirement_workflow

# Full workflow (all three agents)
results = await run_requirement_workflow(
    user_input="需求描述",
    mode="full",
    thread_id="project_id"
)

# Access outputs
requirement_summary = results["stage1"]["requirement_summary"]
prd_document = results["stage2"]["prd_document"]
design_document = results["stage3"]["design_document"]

# Single stage with custom input
result = await run_requirement_workflow(
    user_input="",
    mode="stage2",
    thread_id="project_id",
    input_data="existing requirement summary..."
)
```

### Data Flow Between Agents

1. **Stage 1 Output**: `_extract_summary_from_agent1()` finds messages with "需求摘要" keyword
2. **Stage 2 Output**: `_extract_prd_from_agent2()` returns last AI message
3. **Stage 3 Output**: `_extract_design_from_agent3()` returns last AI message
4. **Data Passing**: Each stage's output is prefixed with instructions and passed as HumanMessage to next agent

**Note**: In non-interactive full workflow mode, Agent 1 automatically requests summary generation after initial response.

## Modifying Agent Behavior

- **Dialogue style**: Edit the `sp` (system prompt) field in config JSON
- **Output length**: Adjust `config.max_completion_tokens` in config
- **Creativity**: Tune `config.temperature` (lower = more deterministic, higher = more creative)
- **Memory size**: Change `MAX_MESSAGES` constant in agent file (default: 60 for Agent 1/2, 80 for Agent 3)

## Adding a New Agent

1. Create `src/agents/agent{N}_{name}.py` following the build_agent() pattern
2. Create `config/agent{N}_config.json` with model config and system prompt
3. Set appropriate MAX_MESSAGES based on expected dialogue length
4. Import and integrate in `workflow_coordinator.py`

## Database and Memory

Database URL is obtained via `storage.database.db.get_db_url()`. The system gracefully falls back to MemorySaver if:
- Database URL is unavailable or empty
- Connection attempts fail (2 retries × 15 seconds each)
- Schema/table creation fails

Thread IDs are suffixed with `_agent{N}` to maintain separate conversation histories per agent.

## Important Notes

- All agents use Claude models (Sonnet 4.5 or Opus 4) with extended thinking capability
- System prompts in config files are extensive (especially Agent 1's 5W2H framework)
- Thread-based isolation ensures each agent maintains its own conversation history
- Extended thinking mode can be enabled/disabled via config for deep reasoning tasks
- For more details, see `docs/USAGE.md`
