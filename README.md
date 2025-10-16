# uv-based Environment (Optional)

This repository can be managed with **uv** instead of venv/pip.

## Install uv
Follow official instructions: https://docs.astral.sh/uv/getting-started/installation/

## Create and activate a virtual environment
```bash
uv venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

## Install dependencies (from pyproject.toml)
```bash
uv pip install -U pip
uv pip install -r <(uv pip compile pyproject.toml)
# or simply
uv pip install -e .
```

## Run each exercise
```bash
uv run python ex1_llm.py
uv run python ex2_embedding.py
uv run python ex3_vector_db.py
uv run python ex4_chatbot.py
```

## Environment variables
Copy the example and set your credentials:
```bash
cp .env.example .env
# set LITELLM_KEY and (optionally) BASE_URL=https://llmproxy.ai.orange
```

> Do not commit `.env`. The `.gitignore` is configured to exclude it.