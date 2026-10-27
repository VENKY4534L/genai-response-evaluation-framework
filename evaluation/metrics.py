"""Simple transparent evaluation metrics for LLM response test cases."""
from __future__ import annotations
import re
from collections import Counter

def normalize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", (text or "").lower())

def token_f1(reference: str, prediction: str) -> float:
    """Token-overlap F1: useful as a rough signal, not a semantic truth metric."""
    ref = normalize(reference)
    pred = normalize(prediction)
    if not ref or not pred:
        return 0.0
    ref_counts, pred_counts = Counter(ref), Counter(pred)
    overlap = sum((ref_counts & pred_counts).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred)
    recall = overlap / len(ref)
    return 2 * precision * recall / (precision + recall)

def keyword_coverage(required_keywords: list[str], prediction: str) -> float:
    """Fraction of required keywords that appear in a response, case-insensitive."""
    if not required_keywords:
        return 1.0
    text = (prediction or "").lower()
    found = sum(1 for word in required_keywords if word.lower() in text)
    return found / len(required_keywords)

def evaluate_case(case: dict, prediction: str) -> dict:
    expected = case.get("expected_answer", "")
    keywords = case.get("required_keywords", [])
    f1 = token_f1(expected, prediction)
    coverage = keyword_coverage(keywords, prediction)
    return {
        "id": case.get("id", ""),
        "question": case.get("question", ""),
        "prediction": prediction,
        "expected_answer": expected,
        "token_f1": round(f1, 3),
        "keyword_coverage": round(coverage, 3),
        "passed_keywords": coverage >= 0.7,
        "note": "Heuristic metrics only; manually review factual correctness and context grounding.",
    }
