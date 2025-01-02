"""
Create answers.
"""

import os
import json

from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM

from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate

NUMBERS_OF_PROBLEMS: int = 80

START_NUMBER_OF_PROBLEMS: int = 0
STOP_NUMBER_OF_PROBLEMS: int = 80

PROBLEM_FILE_NAME: str = "PHP_German.jsonl"
PROBLEM_LANGUAGE: str = "php"

MODEL_NAME: str = "qwen2.5-coder:32b"
SUBFOLDER_NAME: str = "qwen25-coder"
MODEL_PATH = f"/huggingface/models/{MODEL_NAME.replace('-', '_')}"

PROMPT_REPETITIONS: int = 10


def read_problem(task_id: int, language: str) -> dict | None:
    """
    Read file with problem description and get the problem by task_id.

    Args:
        task_id (int): Task id.
        language (str): Coding/Programming language.

    Returns:
        dict | None: Prompt and problem.
    """
    jsonl = open(
        f"{os.path.dirname(os.path.realpath(__file__))}/problems/{PROBLEM_FILE_NAME}",
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


def run_server_model(problem: str):
    """
    Connect to ollama model server.

    :param problem (str): Prompt there is send to ollama server.

    :returns: Result from ollama server by prompt.
    """
    ollama = OllamaLLM(
        base_url="192.168.178.140:11434",
        model=MODEL_NAME,
    )

    promt_template: PromptTemplate = PromptTemplate(
        input_variables=["user_prompt"],
        template="{user_prompt}",
    )

    prompt = promt_template.format(user_prompt=problem)

    return ollama.invoke(prompt)


def run_local_model(problem: str):
    """
    Connect to local model.

    :param problem (str): Prompt for model.

    :returns Result from model.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, torch_dtype="auto", trust_remote_code=True
    )

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    promt_template: PromptTemplate = PromptTemplate(
        input_variables=["user_prompt"],
        template="{user_prompt}",
    )

    prompt = promt_template.format(user_prompt=problem)

    generation_args = {
        "max_new_tokens": 600,
        "return_full_text": False,
        "do_sample": False,
    }

    output = pipe(prompt, **generation_args, pad_token_id=tokenizer.eos_token_id)
    if len(output) > 0:
        return output[0].get("generated_text", "")

    return ""


def write_log(answer: str, key: str, task_id: str) -> None:
    """
    Write the proompt result in JSON file.

    :param answer (str): _description_
    :param key (str): _description_
    :param task_id (str): _description_
    """
    file_name: str = f"{os.path.dirname(os.path.realpath(__file__))}/answer/"
    file_name = f"{file_name}/{SUBFOLDER_NAME}/{task_id.replace('/', '-')}.json"

    answer = answer.replace("\n", r"\n")
    answer = answer.replace('"', r"\"")
    answer = f'"{key}":"{answer}"'

    with open(file_name, "a", encoding="utf-8") as file:
        file.write("{" + answer + "}\n")


def execute_prompt(task_id: int, model_type: str) -> bool:
    """
    Create prompts and save local.

    :param task_id (int): Problem id
    :param model_type (str): Type of model.

    :returns bool: True prompt create.
    """
    language: str = PROBLEM_LANGUAGE

    problem: dict = read_problem(task_id=task_id, language=language)
    prompt: str = problem.get("prompt", None)

    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = PROMPT_REPETITIONS
    while current_count < max_count:
        answer: str = ""
        if model_type == "local":
            answer = run_local_model(problem=prompt)
        elif model_type == "server":
            answer = run_server_model(problem=prompt)
        write_log(
            answer=answer,
            key=f"result_{current_count}",
            task_id=f"{language}/{task_id}",
        )
        current_count += 1
    return True
