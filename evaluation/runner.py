"""Run a small prompt-evaluation dataset against a configurable LLM API."""
from __future__ import annotations
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from evaluation.metrics import evaluate_case

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "evaluation_cases.json"

def call_llm(question: str, prompt_template: str, context: str = "") -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Copy .env.example to .env and configure your key.")
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = prompt_template.format(question=question, context=context)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": "Follow the user's task carefully. Do not invent facts."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""

def main() -> None:
    load_dotenv(ROOT / ".env")
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    results = []
    for case in cases:
        prompt_template = case.get(
            "prompt_template",
            "Answer briefly and accurately. If context is supplied, use only it.\nContext: {context}\nQuestion: {question}",
        )
        prediction = call_llm(case["question"], prompt_template, case.get("context", ""))
        result = evaluate_case(case, prediction)
        results.append(result)
        print(f"{result['id']}: token_f1={result['token_f1']}, keyword_coverage={result['keyword_coverage']}, pass={result['passed_keywords']}")
    output_path = ROOT / "evaluation_results.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {len(results)} results to {output_path}")
    print("Metrics are heuristic. Review responses manually for correctness and context grounding.")

if __name__ == "__main__":
    main()
