# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Universal AI Development Toolkit** (通用AI开发工具集) that provides automated code generation from requirements through a multi-layer architecture: MCP Servers (底层能力) → Agents (中层智能体) → Skills (高层工作流).

**Tech Stack**: Python 3.8+, Anthropic Claude API, Streamlit

**Core Features**: Requirement analysis, architecture design, API design, code generation, code review, self-healing

---

## 🚨 CRITICAL: Project Conventions

### File Naming Rules

**IMPORTANT**: All documentation files MUST use Chinese names, not English names.

✅ **Correct**:
- `项目概览.md`
- `快速开始.md`
- `API设计器优化文档-YAML格式降低Token消耗.md`
- `Token优化更新总结.md`

❌ **Incorrect**:
- `PROJECT_OVERVIEW.md`
- `QUICK_START.md`
- `API_DESIGNER_OPTIMIZATION.md`
- `TOKEN_OPTIMIZATION_SUMMARY.md`

**Exception**: Pure technical specifications or API references may use English names:
- `USAGE.md`, `API.md`, `ENHANCED_CODE_SKILL.md`

### File Organization Rules

**IMPORTANT**: Generated files MUST be placed in appropriate directories, NOT in the project root.

| File Type | Location | Example |
|-----------|----------|---------|
| Technical docs | `docs/` or `文档/开发文档/` | `API设计器优化文档-YAML格式降低Token消耗.md` |
| Update summaries | `docs/` or `文档/开发文档/` | `Token优化更新总结.md` |
| User guides | `文档/用户文档/` | `UI使用指南.md` |
| Generated code | `generated_project/src/` | `main.py`, `models/` |
| Generated tests | `generated_project/tests/` | `test_main.py` |
| Generated docs | `generated_project/docs/` | `requirement.json`, `api_spec.json` |

**Full conventions**: See `项目开发规范.md` for complete details.

---

## Environment Setup

**CRITICAL**: `ANTHROPIC_API_KEY` must be set before running any code.

```bash
# Set API key
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Or use .env file
echo "ANTHROPIC_API_KEY=your-api-key" > .env
```

---

## Architecture Overview

### Three-Layer Architecture

```
Layer 3: Skills (高层工作流)
  /code  /design  /review  /refactor  /self-healing
         ↓
Layer 2: Agents (中层智能体)
  RequirementAnalyst → SystemArchitect → APIDesigner →
  TaskPlanner → CodeGenerator → CodeReviewer
         ↓
Layer 1: MCP Servers (底层能力)
  Filesystem  Git  CLI  Feishu
```

### Key Components

1. **Skills** (`skills/`)
   - `enhanced_code_skill.py`: 6-stage code generation workflow
   - `self_healing_skill.py`: Auto-retry with error recovery
   - `design_skill.py`: Design-only workflow
   - `code_skill.py`: Basic code generation
   - `review_skill.py`: Code review
   - `refactor_skill.py`: Code refactoring

2. **Agents** (`agents/`)
   - `requirement_analyst.py`: Analyze requirements (identifies if API is needed)
   - `system_architect.py`: Design architecture (always required)
   - `api_designer.py`: Design API (conditional - uses YAML for efficiency)
   - `task_planner.py`: Plan implementation tasks
   - `code_generator.py`: Generate code
   - `code_reviewer.py`: Review code quality

3. **MCP Servers** (`mcp_servers/`)
   - `filesystem_server/`: File operations
   - `git_server/`: Git operations
   - `cli_server/`: Command execution
   - `feishu_server/`: Feishu integration

---

## Token Usage Tracking

**CRITICAL**: All Claude API calls MUST track token usage.

### Implementation Pattern

```python
response = self.client.messages.create(
    model=self.model,
    max_tokens=8000,
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}]
)

# Extract token usage
token_usage = {
    "input_tokens": response.usage.input_tokens,
    "output_tokens": response.usage.output_tokens,
    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
}

return {
    "success": True,
    "data": result,
    "token_usage": token_usage,
    "format": "yaml"  # or "json"
}
```

### Display Token Usage

**Console output**:
```python
if "token_usage" in result:
    tokens = result["token_usage"]
    print_safe(f"  ✅ Task completed ({result.get('format', 'unknown').upper()} format)")
    print_safe(f"     Tokens: {tokens['input_tokens']} input + {tokens['output_tokens']} output = {tokens['total_tokens']} total")
```

**UI display**: Token metrics are shown in the Streamlit UI status panel with cost estimation.

---

## Conditional API Design

**IMPORTANT**: Not all projects need API design. The workflow intelligently determines this.

### When API Design is Needed

| Project Type | Needs API | Rationale |
|--------------|-----------|-----------|
| Web backend/API service | ✅ Yes | REST API required |
| Mobile app with backend | ✅ Yes | Backend API needed |
| Web app with backend | ✅ Yes | Backend API needed |
| Microservices | ✅ Yes | Inter-service communication |
| Desktop application | ❌ No | Standalone, no REST API |
| Command-line tool | ❌ No | Local operation |
| Library/SDK | ❌ No | Programming interface, not REST API |
| Frontend-only web app | ❌ No | No backend |
| Script/automation tool | ❌ No | No REST API |

### How It Works

1. **Requirement Analysis** identifies if API is needed:
   ```json
   {
       "needs_api": true|false,
       "api_rationale": "Explanation..."
   }
   ```

2. **Design Stage** conditionally executes API design:
   - Architecture design: **Always executed** ✅
   - API design: **Conditional** (based on `needs_api`)

3. **Token Savings**: Projects without API save ~6,000 tokens and ~15 seconds

**Details**: See `docs/API设计可选化改进文档.md`

---

## API Designer Optimization

**IMPORTANT**: The API Designer uses YAML format by default for 66% token savings.

### Why YAML?

| Metric | JSON | YAML | Improvement |
|--------|------|------|-------------|
| Token usage | 18,234 | 6,127 | -66% |
| Generation time | 38s | 17s | -55% |
| Success rate | 40% | 100% | +150% |
| Cost per call | $0.454 | $0.272 | -40% |

### Configuration

```python
# Default: YAML mode (recommended)
designer = APIDesigner(api_key=api_key)
# designer.use_yaml = True (default)

# Switch to JSON (not recommended)
designer.use_yaml = False
```

**Details**: See `docs/API设计器优化文档-YAML格式降低Token消耗.md`

---

## Console Output Standards

**CRITICAL**: Always use `print_safe()` for console output (Windows compatibility).

### Format Standards

```python
from utils import print_safe

# Stage headers
print_safe("\n" + "=" * 70)
print_safe("🚀 Starting Workflow")
print_safe("=" * 70)

# Progress indicators
print_safe("\n[2/6] Design Phase")
print_safe("  [2.1] Designing architecture...")
print_safe("  ✅ Architecture designed")

# Token usage
print_safe(f"     Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} total")

# Summary
print_safe("\n📊 Workflow Summary:")
print_safe(f"   Stages Completed: 6/6")
print_safe(f"   🔢 Total Token Usage: {total_tokens:,} tokens")
```

---

## Return Value Standards

All agents and skills MUST follow this format:

### Success Response

```python
{
    "success": True,
    "data": {...},
    "token_usage": {
        "input_tokens": 1234,
        "output_tokens": 567,
        "total_tokens": 1801
    },
    "format": "yaml",  # or "json"
    "timestamp": "2026-01-29T10:30:00"
}
```

### Error Response

```python
{
    "success": False,
    "error": "Error description",
    "details": {...},
    "stage": "api_design",
    "timestamp": "2026-01-29T10:30:00"
}
```

---

## Running the System

### Web UI (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
echo "ANTHROPIC_API_KEY=your-api-key" > .env

# Start UI
streamlit run ui_app.py
```

### Python API

```python
from skills.self_healing_skill import SelfHealingSkill

skill = SelfHealingSkill(
    api_key="your-api-key",
    project_path="./generated_project",
    max_retries=3
)

result = skill.execute(requirement="生成一个登录注册的网页界面")

if result["success"]:
    print(f"✅ Success! Generated {len(result['generated_files'])} files")
    print(f"Token usage: {result['token_usage']['total_tokens']:,} tokens")
```

---

## Testing

```bash
# Set environment
export ANTHROPIC_API_KEY="your-api-key"

# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_api_designer.py
```

---

## Important Notes

- **File naming**: Use Chinese names for documentation
- **File location**: Place files in appropriate directories
- **Token tracking**: Track and display token usage everywhere
- **Console output**: Use `print_safe()` for Windows compatibility
- **YAML format**: Default for API specs (66% token savings)
- **Return format**: Follow standard success/error response format
- **Cost awareness**: Display token usage and estimated costs

---

## Documentation

- **Project conventions**: `项目开发规范.md` (MUST READ)
- **Optimization guide**: `docs/API设计器优化文档-YAML格式降低Token消耗.md`
- **Update summary**: `docs/Token优化更新总结.md`
- **User guide**: `README.md`
- **Quick start**: `快速开始.md`
- **UI guide**: `UI快速开始.md`

---

## Quick Reference

### File Naming
- ✅ Chinese: `项目概览.md`, `快速开始.md`
- ❌ English: `PROJECT_OVERVIEW.md`, `QUICK_START.md`

### File Location
- ✅ Docs: `docs/` or `文档/开发文档/`
- ✅ Code: `generated_project/src/`
- ❌ Root: Never place generated files in project root

### Token Tracking
- ✅ Always track: `token_usage = {...}`
- ✅ Always display: `print_safe(f"Tokens: {total}")`
- ✅ Include in return: `return {"token_usage": ...}`

### Console Output
- ✅ Use: `print_safe("message")`
- ❌ Don't use: `print("message")`

---

**Version**: 1.0
**Last Updated**: 2026-01-29
**Maintainer**: Project Team
