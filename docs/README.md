# ETERNITY---Virtual-Assistant  
**A Virtual Assistant to automate many tasks**

---

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Quick Start / Usage](#quick-start--usage)  
6. [Configuration](#configuration)  
7. [API Documentation](#api-documentation)  
8. [Examples](#examples)  
9. [Testing](#testing)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Overview
`ETERNITY---Virtual-Assistant` is a modular, extensible Python‑based virtual assistant that can:

- Schedule meetings, set reminders, and manage calendars.  
- Interact with popular services (Google, Outlook, Slack, GitHub, etc.).  
- Execute system commands, run scripts, and automate repetitive workflows.  
- Provide natural‑language chat via OpenAI / local LLM back‑ends.  
- Be extended with custom “skills” (plugins) written in pure Python.

The project follows a **plug‑and‑play** architecture: core services are lightweight, and additional capabilities are added as optional modules.

---

## Features
| Category | Capability | Details |
|----------|------------|---------|
| **Core** | Speech‑to‑Text / Text‑to‑Speech | Uses `whisper.cpp` (local) or OpenAI Whisper API. |
| | Natural‑Language Understanding | Powered by OpenAI `gpt‑4o-mini` (default) or any OpenAI‑compatible endpoint. |
| | Task Scheduler | Cron‑like scheduler with persistence (SQLite). |
| **Integrations** | Google Calendar / Outlook | Create, update, delete events. |
| | Email (SMTP/IMAP) | Send, read, and filter messages. |
| | Slack / Discord | Post messages, react to commands. |
| | GitHub | Create issues, PRs, comment, and run actions. |
| **Extensibility** | Plugin System | Drop a Python module into `plugins/` and register a skill. |
| | CLI & REST API | Interact via terminal or HTTP. |
| **Security** | OAuth2 token storage (encrypted) | Uses `cryptography` to protect secrets. |
| | Rate‑limit handling | Automatic back‑off for external APIs. |

---

## Prerequisites
| Tool | Minimum Version | Why |
|------|----------------|-----|
| Python | **3.10** (≥3.11 recommended) | Type‑hints, `match` statements, `tomllib`. |
| pip | 23.0+ | Dependency management. |
| Git | 2.30+ | Cloning the repo. |
| ffmpeg | 4.4+ | Audio capture & conversion (speech). |
| (Optional) Docker | 20.10+ | Run the assistant in an isolated container. |
| (Optional) OpenAI API key | – | For LLM‑backed NLU. |
| (Optional) Google OAuth credentials | – | Calendar integration. |

> **Tip:** On Ubuntu/Debian you can install the system dependencies with:  
> ```bash  
> sudo apt-get update && sudo apt-get install -y python3-pip python3-venv ffmpeg git curl  
> ```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-org/ETERNITY---Virtual-Assistant.git
cd ETERNITY---Virtual-Assistant
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install core dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install optional extras (pick what you need)

| Extra | Command |
|-------|---------|
| **All** (full feature set) | `pip install ".[all]"` |
| **Google Calendar** | `pip install ".[google]"` |
| **Slack** | `pip install ".[slack]"` |
| **Docker support** | `pip install ".[docker]"` |
| **Testing** | `pip install ".[dev]"` |

> The `pyproject.toml` defines these extras; you can also edit the file to add your own.

### 5. (Optional) Install as a system‑wide command
```bash
pip install -e .
# Now you can run `eternity` from anywhere
```

### 6. Verify installation
```bash
eternity --version
# Expected output: ETERNITY---Virtual-Assistant vX.Y.Z
```

---

## Quick Start / Usage

### 1. Initialise configuration
```bash
eternity init
```
This command creates a `config.yaml` in the current directory (or `$HOME/.eternity/`). Follow the interactive prompts to:

- Set your **OpenAI API key** (or choose a local LLM).  
- Provide **OAuth credentials** for Google/Outlook (if you selected those extras).  
- Choose a **default voice** for TTS.

### 2. Run the assistant in interactive mode
```bash
eternity chat
```
You’ll see a prompt like:
```
[ETERNITY] > Hello! How can I help you today?
```
Type natural language commands, e.g.:

- `Schedule a meeting with Alice tomorrow at 10am about the Q3 report.`  
- `Send a Slack reminder to #dev-team: "Deploy at 5pm".`  
- `Run the script scripts/backup.sh and email me the log.`

### 3. Use the CLI for one‑off commands
```bash
# Create a calendar event
eternity calendar create \
    --title "Team Sync" \
    --start "2025-10-01 09:00" \
    --duration 60 \
    --participants alice@example.com,bob@example.com

# Send an email
eternity email send \
    --to john.doe@example.com \
    --subject "Daily Report" \
    --body "$(cat reports/daily.txt)"
```

### 4. Run the REST API server (optional)
```bash
eternity serve --host 0.0.0.0 --port 8080
```
The API is documented in the **API Documentation** section below. You can now POST JSON payloads to `http://localhost:8080/v1/command`.

---

## Configuration

The configuration file (`config.yaml`) lives in one of two locations (first found wins):

1. **Project root** – `./config.yaml` (useful for per‑project settings).  
2. **User home** – `$HOME/.eternity/config.yaml` (global defaults).

### Sample `config.yaml`

```yaml
# -------------------------------------------------
# Core settings
# -------------------------------------------------
assistant:
  name: "Eternity"
  language: "en-US"
  voice: "en_us_fox"
  llm:
    provider: "openai"
    model: "gpt-4o-mini"
    api_key: "${OPENAI_API_KEY}"   # can be env var reference
    temperature: 0.2
    max_tokens: 1024

# -------------------------------------------------
# Scheduler
# -------------------------------------------------
scheduler:
  db_path: "~/.eternity/schedule.db"
  timezone: "America/New_York"

# -------------------------------------------------
# Integrations
# -------------------------------------------------
google:
  enabled: true
  credentials_file: "~/.eternity/google_credentials.json"
  token_file: "~/.eternity/google_token.json"

slack:
  enabled: false
  bot_token: "${SLACK_BOT_TOKEN}"
  signing_secret: "${SLACK_SIGNING_SECRET}"

email:
  smtp:
    host: "smtp.gmail.com"
    port: 587
    user: "myassistant@gmail.com"
    password: "${SMTP_PASSWORD}"
  imap:
    host: "imap.gmail.com"
    port: 993
    user: "myassistant@gmail.com"
    password: "${IMAP_PASSWORD}"

# -------------------------------------------------
# Security
# -------------------------------------------------
security:
  secret_key: "${ETERNITY_SECRET}"   # used for encrypting tokens
  encryption_algo: "Fernet"
```

**Tips**

- Use environment variable interpolation (`${VAR_NAME}`) for secrets.  
- Run `eternity encrypt-secret <plain-text>` to generate a Fernet‑encrypted value.  
- The `eternity config edit` command opens the file in your `$EDITOR`.

---

## API Documentation

The assistant ships with a **RESTful JSON API** (FastAPI under the hood). The server can be started with `eternity serve`. All endpoints are versioned under `/v1`.

### Base URL
```
http://<host>:<port>/v1
```

### Authentication
- **API Key** – Provide `X-API-Key: <your-key>` header