"""
Create answers for the benchmark by local models.
"""

__VERSION__ = "0.0.1"

from src.execute.execute_local import execute_prompt

execute_prompt(
    task_id=1,
    model_name="phi_2",
    language="php",
    problem_filename="PHP_German.jsonl",
    answer_sub_folder="phi2",
    prompt_repetitions=2,
)
