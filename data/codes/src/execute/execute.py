"""
Create answers.
"""

__VERSION__ = "0.0.1"

import os
import json

DATA_BASE_PATH: str = f"{os.path.dirname(os.path.realpath(__file__))}/../../data"

MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TEMP: float = 0.2
MODEL_SETTING_TOP_P: float = 0.95


def read_problem(task_id: int, language: str, problem_filename: str) -> dict | None:
    """
    Read file with problem description and get the problem by task_id.

    :param task_id (int): Task id.
    :param language (str): Coding/Programming language.

    :returns dict | None: Prompt and problem.
    """
    jsonl = open(
        f"{DATA_BASE_PATH}/problems/{problem_filename}",
        "r",
        encoding="utf-8",
    )
    lines = jsonl.readlines()
    problem: dict = None
    for line in lines:
        problem = json.loads(line)
        if problem.get("task_id", None) == f"{language}/{task_id}":
            break
    jsonl.close()

    return problem


def write_log(answer: str, key: str, task_id: str, sub_folder: str) -> None:
    """
    Write the proompt result in JSON file.

    :param answer (str): _description_
    :param key (str): _description_
    :param task_id (str): _description_
    """
    file_name = (
        f"{DATA_BASE_PATH}/answers/{sub_folder}/{task_id.replace('/', '-')}.jsonl"
    )

    answer = answer.replace("\n", r"\n")
    answer = answer.replace('"', r"\"")
    answer = f'"{key}":"{answer}"'

    with open(file_name, "a", encoding="utf-8") as file:
        file.write("{" + answer + "}\n")
