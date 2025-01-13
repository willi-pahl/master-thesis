__VERSION__ = "0.0.1"

from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate

from src.execute.execute import (
    read_problem,
    write_log,
    MODEL_SETTING_MAX_TOKEN,
    MODEL_SETTING_TEMP,
    MODEL_SETTING_TOP_P,
)

MODEL_CONNECT_HOST: str = "192.168.178.140"
MODEL_CONNECT_PORT: str = "11434"


INSTALLED_LLMS: list[dict] = [
    {"model": "qwen2.5-coder:32b", "answer_folder": "qwen25_coder"},
    # more models ...
]

def run_model(problem: str, model: OllamaLLM) -> str:
    """
    Connect to ollama model server.

    :param problem (str): Prompt there is send to ollama server.
    :return Result from ollama server by prompt.
    """
    promt_template: PromptTemplate = PromptTemplate(
        input_variables=["user_prompt"],
        template="{user_prompt}",
    )
    prompt = promt_template.format(user_prompt=problem)

    return model.invoke(prompt)

def connect_model(model_name: str) -> OllamaLLM:
    """
    Connect Ollama hosted model

    :param model_name (str): Model name.
    :return OllamaLLM: Connected model.
    """
    return OllamaLLM(
        base_url=f"{MODEL_CONNECT_HOST}:{MODEL_CONNECT_PORT}",
        model=model_name,
        max_token=MODEL_SETTING_MAX_TOKEN,
        temperature=MODEL_SETTING_TEMP,
        top_p=MODEL_SETTING_TOP_P,
    )

def execute_prompt(
    task_id: int,
    model_name: str,
    language: str,
    problem_filename: str,
    answer_sub_folder: str,
    prompt_repetitions: int = 10,
) -> bool:
    """
    Create prompts and save local.

    :param task_id (int): Problem id
    :param model_type (str): Type of model.
    :returns bool: True prompt create.
    """
    problem: dict = read_problem(
        task_id=task_id, language=language, problem_filename=problem_filename
    )
    prompt: str = problem.get("prompt", None)

    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    model = connect_model(model_name=model_name)
    while current_count < max_count:
        answer = run_model(problem=prompt, model=model)
        write_log(
            answer=answer,
            key=f"result_{current_count}",
            task_id=f"{language}/{task_id}",
            sub_folder=answer_sub_folder,
        )
        current_count += 1
    return True