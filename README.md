

# Simple AI Agent

Simple AI Agent is a minimal agent built with Gemini API for simple tasks and code execution. It is aimed to be a good start for anyone building AI agents.

## Key Features
- **Gemini API Integration:** Interact with Google’s Gemini models using your own API key.
- **Secure Tool Calls:** All file and directory operations are restricted to a configurable working directory for safety.
- **Easy Setup:** Step-by-step instructions for installing dependencies, configuring your API key, and running the agent.
- **Extensible Design:** Add new tools in the `tools/` directory and expand agent logic in `main.py`.
- **Testing Included:** Comprehensive test suite for all core functions and agent methods.
- **Flexible Dependency Management:** Supports both `pip` and `uv` for fast, reproducible installs.

Perfect for developers and researchers who want a lightweight, customizable AI agent with strong security guardrails and clear setup instructions.

# Project Setup Guide

This guide will help you set up the AI Agent project on your computer and get everything running.

## Prerequisites

- Python 3.12 or newer
- A Gemini API key get one from [Google AI Studio](https://aistudio.google.com/apikey)
- Recommended: [uv](https://github.com/astral-sh/uv) for fast dependency management


## Step 0: Clone the Repository

Clone this project to your local machine:
```zsh
git clone https://github.com/evaezekwem/aiagent.git
cd aiagent
```

## Step 1: Create and Activate a Virtual Environment

It is recommended to use a virtual environment to isolate your dependencies.

**Using pip (venv):**
```zsh
python -m venv .venv
source .venv/bin/activate
```

**Using uv:**
```zsh
uv venv
source .venv/bin/activate
```

## Step 2: Install Dependencies

You can use either pip or uv:

**Using pip:**
```zsh
pip install -r pyproject.toml
```

**Using uv:**
```zsh
uv pip install -r pyproject.toml
```

If you see errors about missing modules (e.g. `google`), install them directly:
```zsh
pip install google-genai==1.12.1 python-dotenv==1.1.0
```
or
```zsh
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
```

## Step 3: Configure Your API Key

Create a `.env` file in the project root with your Gemini API key:
```
GEMINI_API_KEY=your-key-here
```

IMPORTANT: Modify the `config.py` file in the `/config` directory and add the working directory you want the agent to have access to.
This will limit file access to this folder alone.

## Step 4: Run the Application

**Basic usage:**
```zsh
python main.py "What is the temperature in San Francisco"
```

**Verbose mode:**
```zsh
python main.py "What is the temperature in San Francisco" --verbose
```

**Using uv:**
```zsh
uv run main.py -- "yWhat is the temperature in San Francisco" --verbose
```

## Step 5: Run the Tests

**Using python:**
```zsh
python tests.py
```

**Using uv:**
```zsh
uv run tests.py
```

## Troubleshooting

- If you see `ModuleNotFoundError: No module named 'google'`, install the required package as shown above.
- Make sure your `.env` file is present and contains a valid API key.
- For other issues, check error messages for missing dependencies or invalid configuration.

## Next Steps

- To add new tools, create Python files in the `tools/` directory.
- To extend agent logic, update `main.py` and add tests in `tests.py`.

