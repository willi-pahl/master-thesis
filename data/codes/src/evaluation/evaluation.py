"""
Evaluations of the HumanEval-XL benchmark for the individual models.
"""

__VERSION__ = "0.0.1"

import subprocess
import json
import os

from pass_at_k import pass_at_k


DATA_BASE_PATH: str = f"{os.path.dirname(os.path.realpath(__file__))}/../../data"


def get_file_content(
    file_name: str, count_problems: int, answer_path: str
) -> tuple[list[str], int]:
    """
    Get the content from JSONL answer file.

    :param file_name (str): File name with answers.
    :param count_problems (int): Number of first samples from each test to be tested.
    :param answer_path (str): Path to answer file.
    :return tuple[list[str], int]: Generated code snippets from LLM and count of snippets.
    """
    answers: list = []
    length: int = 0
    with open(f"{answer_path}/{file_name}.jsonl", encoding="utf-8") as answer_file:
        lines: str = answer_file.read()
        length = 5
        for line in lines.split("\n"):
            if line != "":
                answers.append(search_generated_code(line))
                if len(answers) >= count_problems:
                    return (answers, length)
    return (answers, length)


def search_generated_code(content: str) -> str:
    """
    Search the generated code in string, it is one line of file.

    Args:
        content (str): Answer from LLM.

    Returns:
        str: Generated code.
    """
    for index in range(0, 5):
        if content.startswith('{"result_' + str(index) + '":"'):
            generated_code: str = content.split('{"result_' + str(index) + '":"')[1]
            generated_code = generated_code[:-2]
            generated_code = generated_code.strip()

            if len(generated_code.split("```php")) > 1:
                generated_code = generated_code.split("```php")[1]
                generated_code = generated_code.split("```")[0]

            if generated_code.startswith("<?php"):
                generated_code = generated_code.split("<?php")[1]
                generated_code = generated_code.split("?>")[0]

            if len(generated_code.split(r"\n}\n")) > 0:
                generated_code = generated_code.split(r"\n}\n")[0] + "\n}\n"

            return generated_code
    return ""


def run(
    problem_path: str,
    answer_path: str,
    num_consider_samples: int,
):
    """
    Execute the ecaluation.

    :param problem_path (str): Path to problem.
    :param answer_path (str): Path to answers.
    :param num_consider_samples (int): Numbers of consider samples.
    """
    summary_answer_pass_at_k: list[float] = []
    with open(problem_path, "r", encoding="utf-8") as problems:
        lines: list = problems.read().split("\n")
        # 80 Problems.
        total_samples: int = 0
        correct_samples: int = 0
        answers_per_sample: int = 0
        for line in lines:
            problem_result: str = ""
            if line != "":
                answer_file_name: str = (
                    json.loads(line).get("task_id", "").replace("/", "-")
                )
                problem_result = (
                    json.loads(line).get("task_id", "")
                    + ";"
                    + str(num_consider_samples)
                )
                test: str = json.loads(line).get("test", "")
                content_tuple: tuple = get_file_content(
                    file_name=answer_file_name,
                    count_problems=num_consider_samples,
                    answer_path=answer_path,
                )
                answers: list[str] = content_tuple[0]
                answers_per_sample = content_tuple[1]

                count: int = 1
                # False == durchgefallen
                answer_result_fault: bool = False
                ready_count: int = 0
                total_samples += 1
                for answer in answers:
                    answer = answer.replace(r"\n", "\n")
                    answer = answer.replace(r"\"", '"')

                    test = test.replace(r"\"", '"')

                    try:
                        result = subprocess.run(
                            ["php", "-r", f"{test}{answer}"],
                            capture_output=True,
                            text=True,
                            check=False,
                            timeout=5,
                        )
                    except subprocess.TimeoutExpired:
                        pass

                    if result.stderr.strip() == "":
                        answer_result_fault = True
                        ready_count += 1

                    count += 1

                if answer_result_fault:
                    correct_samples += 1

                problem_result += ";" + str(ready_count)
                result_pass_at_k: float = pass_at_k(
                    num_total_samples_n=answers_per_sample,
                    num_correct_samples_c=ready_count,
                    k=num_consider_samples,
                )
                problem_result += ";" + str(result_pass_at_k)
                summary_answer_pass_at_k.append(result_pass_at_k)

            print(problem_result)

    print(f"total samples; {total_samples}")
    print(f"correct samples; {correct_samples}")
    print(f"answers per sample; {answers_per_sample}")
    print(f"k; {num_consider_samples}")
    print(f"Summary LLM; {(correct_samples / total_samples):.4f}")
