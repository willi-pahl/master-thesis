"""
Create answers for the benchmark by Ollama service models.
"""

__VERSION__ = "0.0.1"

from src.execute.execute_ollama import execute_prompt, INSTALLED_LLMS

for llm in INSTALLED_LLMS:
    execute_prompt(
        task_id=1,
        model_name=llm.get("model"),
        language="php",
        problem_filename="PHP_German.jsonl",
        answer_sub_folder=llm.get("answer_folder"),
        prompt_repetitions=5,
    )
