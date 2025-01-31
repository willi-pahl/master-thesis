"""
Create answers for the benchmark by OpenAI models.
"""

__VERSION__ = "0.0.1"

from src.execute.execute_openai_gpt import execute_prompt, ALLOWED_LLMS


for llm in ALLOWED_LLMS:
    for index in range(0, 80):
        execute_prompt(
            task_id=index,
            model_name=llm.get("model"),
            language="php",
            problem_filename="PHP_German.jsonl",
            answer_sub_folder=llm.get("answer_folder"),
            prompt_repetitions=10,
        )
