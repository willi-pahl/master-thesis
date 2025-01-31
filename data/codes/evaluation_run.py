"""
Run the evaluations of the HumanEval-XL benchmark for the individual models.
"""

__VERSION__ = "0.0.1"

from src.evaluation.evaluation import DATA_BASE_PATH


from src.evaluation.evaluation import run

# Customize: path to benchmark German: PHP_German.jsonl or Englsh: PHP_English.jsonl"
problem_path: str = f"{DATA_BASE_PATH}/problems/PHP_English.jsonl"

# Customize: path to generated code from LLM.
answer_path: str = f"{DATA_BASE_PATH}/answers/gemini15"

# Customize: numbers of top for check.
num_consider_samples: int = 5

run(
    problem_path=problem_path,
    answer_path=answer_path,
    num_consider_samples=num_consider_samples,
)
