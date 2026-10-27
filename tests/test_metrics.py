import unittest
from evaluation.metrics import token_f1, keyword_coverage, evaluate_case

class EvaluationMetricTests(unittest.TestCase):
    def test_identical_text_has_full_token_f1(self):
        self.assertEqual(token_f1("cloud run service", "Cloud Run service"), 1.0)

    def test_no_overlap_has_zero_f1(self):
        self.assertEqual(token_f1("cloud database", "banana spaceship"), 0.0)

    def test_keyword_coverage(self):
        self.assertEqual(keyword_coverage(["Python", "SQL"], "Python is used with SQL."), 1.0)

    def test_evaluate_case(self):
        case = {"id": "T1", "question": "What is Python?", "expected_answer": "Python language", "required_keywords": ["Python"]}
        result = evaluate_case(case, "Python is a programming language.")
        self.assertTrue(result["passed_keywords"])
        self.assertEqual(result["keyword_coverage"], 1.0)

if __name__ == "__main__":
    unittest.main()
