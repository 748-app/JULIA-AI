# JULIA AI - Phase 1: Skeleton

**Version:** 0.1.0  
**Status:** Online  
**Phase:** 1 (Skeleton)

## Overview

JULIA AI is a multi-agent autonomous system for software engineering. This repository contains the Phase 1 skeleton: a minimal but functional foundation with an Orchestrator, configuration system, and logging.

## What's Included (Phase 1)

- **Orchestrator**: Central brain of the system (skeleton)
- **Configuration**: API keys, model routing map, settings
- **Logging**: File-based logging with console output in debug mode
- **Tests**: Phase 1 validation suite

## Structure

```
julia_ai/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration + MODEL_ROUTING
├── core/
│   ├── __init__.py
│   └── orchestrator.py      # The Brain
├── tests/
│   └── test_phase1.py       # Validation tests
├── logs/                    # Runtime logs (git-ignored)
├── main.py                  # Entry point
├── run.bat                  # Windows launcher
├── requirements.txt         # Dependencies
├── .env.example            # API keys template
├── .gitignore
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
cd julia_ai
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
DEEPSEEK_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### Run

**Linux/Mac:**
```bash
python main.py
```

**Windows:**
```bash
run.bat
```

### Test

```bash
python tests/test_phase1.py
```

Expected output: `TEST PHASE 1: PASSED`

## Model Routing (Phase 1: Configuration Only)

The `MODEL_ROUTING` map in `config/settings.py` defines which LLM to use for each task type:

| Task Type | Model | Purpose |
|-----------|-------|---------|
| reasoning | deepseek-v4-pro | Deep reasoning, planning, architecture |
| coding | codestral-latest | Code generation, completion |
| fast | mistral-small | Quick responses |
| analysis | mistral-large-latest | Text analysis |
| fallback | mistral-medium | Backup model |

**Note:** Actual dynamic routing will be implemented in Phase 3.

## Windows Compatibility

This project is designed for Windows first:

- All paths use `pathlib.Path` (no hardcoded slashes)
- `run.bat` provided for easy launching
- UTF-8 encoding explicit everywhere
- No Linux-only dependencies

## Next Phases

- **Phase 2**: Memory (SQLite + vector store)
- **Phase 3**: Specialized Agents (Analysis, Code, Critique)
- **Phase 4**: Tools (File system, web search, sandbox)
- **Phase 5**: Frontend & Integration (FastAPI + React)

## Rules

1. **Think before acting**: Every file must have a clear purpose
2. **Zero over-engineering**: Minimal viable structure only
3. **Windows compatibility**: pathlib.Path everywhere
4. **Discipline**: One file = one responsibility
5. **Multi-agent ready**: Orchestrator is the single decision-maker

## License

MIT
