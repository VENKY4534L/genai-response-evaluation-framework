# Generative AI Response Evaluation Framework

A small Python project for running LLM prompts against a repeatable test set and reviewing the resulting responses with transparent, heuristic metrics.

## Features

- Configurable LLM API and model name through environment variables.
- JSON-based evaluation cases with question, context, expected answer, and required keywords.
- Prompt templates and repeatable test cases.
- Token-overlap F1 and required-keyword coverage.
- JSON report output.
- Unit tests for the evaluation metrics.

## Important limitations

Token F1 and keyword coverage are simple heuristics. They do not prove factual correctness, safety, semantic equivalence, or groundedness. Always manually inspect outputs. The API runner requires a valid provider API key and may incur charges.

## Requirements

- Python 3.10+
- An API key compatible with the OpenAI Python SDK if you want to run live model evaluations.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your own `OPENAI_API_KEY`. Never commit `.env` or share your key.

## Run evaluation

```powershell
python -m evaluation.runner
```

The script calls the configured model for each test case and writes `evaluation_results.json`. This generated report is excluded from Git by `.gitignore`.

## Run unit tests

```powershell
python -m unittest discover -s tests -v
```

Tests do not require an API key.

## GitHub

Create a new repository, for example `genai-response-evaluation-framework`, then from this folder:

```bash
git init
git add .
git commit -m "Add Generative AI response evaluation framework"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/genai-response-evaluation-framework.git
git push -u origin main
```

## Resume wording (after you run and verify it)

**Generative AI Response Evaluation Framework | Python, LLM API, Prompt Engineering, JSON**
- Built a repeatable test runner for evaluating LLM responses against predefined questions and expected criteria.
- Implemented token-overlap F1 and keyword-coverage metrics to provide basic response-quality signals.
- Exported structured evaluation results to JSON and added unit tests for metric behavior.
