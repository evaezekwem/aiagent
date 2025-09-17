aiagent/
├── main.py
├── tools/
│   ├── evaluate_math_expression.py
│   ├── get_current_temperature.py
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── config/
│   ├── agent_tools.py
│   ├── config.py
|   └── prompts.py
├── tests.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .github/copilot-instructions.md

# Project Setup Guide

This guide will help you set up the AI Agent Gemini Python project on your computer and get everything running.

## Prerequisites

- Python 3.12 or newer
- A Gemini API key get one from [Google AI Studio](https://aistudio.google.com/apikey)
- Recommended: [uv](https://github.com/astral-sh/uv) for fast dependency management

## Step 1: Clone the Repository

Clone this project to your local machine:
```zsh
git clone https://github.com/evaezekwem/aiagent.git
cd aiagent
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
python main.py "your prompt here"
```

**Verbose mode:**
```zsh
python main.py "your prompt here" --verbose
```

**Using uv:**
```zsh
uv run main.py -- "your prompt here" --verbose
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

