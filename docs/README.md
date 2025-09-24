# ETERNITY — Virtual Assistant  
**A Virtual Assistant to automate many tasks**  

---  

## Table of Contents
1. [Overview](#overview)  
2. [Quick Start](#quick-start)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
6. [API Documentation](#api-documentation)  
7. [Examples](#examples)  
8. [Testing](#testing)  
9. [Contributing](#contributing)  
10. [License](#license)  
11. [Acknowledgements](#acknowledgements)  

---  

## Overview
**ETERNITY** is a modular, extensible virtual‑assistant framework written in Python 3.11+.  
It can:

* Understand natural‑language commands (via OpenAI, Anthropic, or local LLMs).  
* Execute system commands, manage files, send emails, schedule calendar events, control smart‑home devices, and more.  
* Be extended with custom “skills” (plugins) that expose new capabilities.  

The project follows a clean **core → plugin → CLI** architecture, making it easy to embed the assistant in other Python applications or run it as a standalone command‑line tool.

---  

## Quick Start
```bash
# Clone the repo
git clone https://github.com/your-org/ETERNITY---Virtual-Assistant.git
cd ETERNITY---Virtual-Assistant

# Install (recommended inside a virtualenv)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .            # editable install with all extras

# Set up environment variables (see Configuration)
cp .env.example .env
# edit .env → add your API keys, etc.

# Run the assistant
eternity chat               # interactive chat mode
# or
eternity run "Create a reminder for tomorrow at 9 am"
```

---  

## Installation  

### Prerequisites
| Requirement | Minimum version |
|-------------|-----------------|
| Python      | 3.11            |
| pip         | 23.0+           |
| git         | any             |
| (Optional) Docker | 20.10+   |

### 1. Clone the repository
```bash
git clone https://github.com/your-org/ETERNITY---Virtual-Assistant.git
cd ETERNITY---Virtual-Assistant
```

### 2. Create a virtual environment (highly recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install the package
```bash
# Core installation (no optional extras)
pip install -e .

# Install with all optional dependencies (LLM providers, smart‑home, etc.)
pip install -e .[all]

# Or install only the extras you need
pip install -e .[openai]      # OpenAI API support
pip install -e .[anthropic]   # Anthropic API support
pip install -e .[homeassistant] # Home Assistant integration
```

### 4. (Optional) Install via Docker
A Dockerfile is provided for isolated deployments.

```bash
docker build -t eternity-va .
docker run -it --rm \
    -v $(pwd)/.env:/app/.env \
    eternity-va chat
```

---  

## Configuration  

All runtime configuration lives in a **`.env`** file at the project root (or can be exported as environment variables).  
A template is provided: **`.env.example`**.

### Required keys
| Variable | Description |
|----------|-------------|
| `ETERNITY_LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default: `INFO`. |
| `ETERNITY_DEFAULT_MODEL` | Default LLM model identifier (e.g., `gpt-4o-mini`). |
| `OPENAI_API_KEY` | Your OpenAI API key (if using OpenAI). |
| `ANTHROPIC_API_KEY` | Your Anthropic API key (if using Claude). |
| `HOME_ASSISTANT_URL` | URL of your Home Assistant instance (optional). |
| `HOME_ASSISTANT_TOKEN` | Long‑lived token for Home Assistant (optional). |

### Example `.env`
```dotenv
ETERNITY_LOG_LEVEL=INFO
ETERNITY_DEFAULT_MODEL=gpt-4o-mini

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx

# Home Assistant (optional)
HOME_ASSISTANT_URL=http://homeassistant.local:8123
HOME_ASSISTANT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> **Tip:** Keep `.env` out of version control (`.gitignore` already contains it).

---  

## Usage  

ETERNITY ships with a **CLI** powered by `typer`. The entry point is the `eternity` command.

### 1. Interactive chat
```bash
eternity chat
```
* Type natural‑language commands.
* The assistant replies in the terminal and can ask follow‑up questions.
* Press `Ctrl‑C` to exit.

### 2. One‑shot execution
```bash
eternity run "Send an email to alice@example.com with the subject 'Report' and attach the latest PDF in ~/reports"
```
* Returns a concise textual summary of what was done.

### 3. Skill management
```bash
# List installed skills
eternity skills list

# Enable a disabled skill
eternity skills enable calendar

# Disable a skill
eternity skills disable file_manager
```

### 4. Server mode (REST API)
```bash
eternity serve --host 0.0.0.0 --port 8000
```
* Starts an ASGI server (FastAPI) exposing `/v1/chat`, `/v1/run`, and `/v1/skills` endpoints.
* Useful for integrating ETERNITY into other services or UI front‑ends.

### 5. Configuration overrides (CLI flags)
All settings can be overridden at runtime:

```bash
eternity run "What is the weather in Paris?" --model gpt-4o --temperature 0.7
```

---  

## API Documentation  

Below is a high‑level overview of the public Python API. Full docstrings are available in the source and can be rendered with `pdoc` or `mkdocstrings`.

### Core Packages
| Module | Description |
|--------|-------------|
| `eternity.core.assistant` | Main `Assistant` class – orchestrates LLM calls, skill routing, and response formatting. |
| `eternity.core.config` | `Config` singleton that loads `.env` and provides typed access to settings. |
| `eternity.core.logger` | Centralized logger (`eternity.logger`) configured by `ETERNITY_LOG_LEVEL`. |
| `eternity.core.exceptions` | Custom exception hierarchy (`EternityError`, `SkillError`, `LLMError`, …). |

### Skill System
*All skills inherit from `eternity.skills.base.SkillBase`.*

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `SkillBase` | Abstract base for all plugins. Handles registration, enable/disable, and metadata. | `execute(self, context, **kwargs)` |
| `FileManagerSkill` | File‑system operations (list, move, delete, read). | `list_dir`, `read_file`, `write_file` |
| `EmailSkill` | Send/receive email via SMTP/IMAP. | `send_email`, `search_mail` |
| `CalendarSkill` | Google Calendar / CalDAV integration. | `create_event`, `list_events` |
| `HomeAssistantSkill` | Control Home Assistant entities. | `call_service`, `get_state` |
| `CustomSkill` | Dynamically loaded from `plugins/` folder. | `execute` (user‑defined) |

#### Registering a new skill
```python
# plugins/my_gpt_skill.py
from eternity.skills.base import SkillBase

class MyGPTSkill(SkillBase):
    name = "my_gpt"
    description = "Runs a custom prompt against a private LLM."

    async def execute(self, context, prompt: str):
        # custom logic here
        return await self.llm_client.complete(prompt)
```

Add the file to `plugins/` and run:
```bash
eternity skills reload
```

### LLM Clients
| Class | Provider | Primary Methods |
|-------|----------|-----------------|
| `OpenAIClient` | OpenAI | `chat(messages, **kwargs)`, `complete(prompt, **kwargs)` |
| `AnthropicClient` | Anthropic