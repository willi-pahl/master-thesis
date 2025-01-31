"""
Create answers by local models.
"""

__VERSION__ = "0.0.1"

from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM

from langchain.prompts import PromptTemplate

from src.execute.execute import (
    read_problem,
    write_log,
    MODEL_SETTING_MAX_TOKEN,
    MODEL_SETTING_TEMP,
    MODEL_SETTING_TOP_P,
)

MODEL_BASE_PATH: str = "/home/pahl/huggingface/models"

SAVED_LLMS: list[dict] = [{"model": "tinyllama1.1b", "answer_folder": "tinyllama"}]


def run_model(problem: str, pipe: pipeline) -> str:
    """
    Connect to local model.

    :param problem (str): Prompt for model.

    :returns Result from model.
    """
    promt_template: PromptTemplate = PromptTemplate(
        input_variables=["user_prompt"],
        template="{user_prompt}",
    )

    prompt = promt_template.format(user_prompt=problem)

    generation_args = {
        "do_sample": True,
        "truncation": True,
        "max_new_tokens": MODEL_SETTING_MAX_TOKEN,
        "temperature": MODEL_SETTING_TEMP,
        "top_p": MODEL_SETTING_TOP_P,
    }

    output = pipe(prompt, **generation_args, pad_token_id=pipe.tokenizer.eos_token_id)

    if len(output) > 0:
        return output[0].get("generated_text", "")

    return ""


def connect_pipeline(model_name: str) -> pipeline:
    """
    Connect to local models.

    Args:
        model_name (str): Model name.

    Returns:
        pipeline: Pipeline with model and tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_BASE_PATH}/{model_name}")

    model = AutoModelForCausalLM.from_pretrained(
        f"{MODEL_BASE_PATH}/{model_name}", torch_dtype="auto", trust_remote_code=True
    )

    return pipeline("text-generation", model=model, tokenizer=tokenizer)


def execute_prompt(
    task_id: int,
    model_name: str,
    language: str,
    problem_filename: str,
    answer_sub_folder: str,
    prompt_repetitions: int = 5,
) -> bool:
    """
    Create prompts and save local.

    :param task_id (int): Problem id.
    :param model_name (str): Model name.
    :param language (str): Programming language.
    :param problem_filename (str): Name of benchmarkfile.
    :param answer_sub_folder (str): Subfolder for create answers.
    :param prompt_repetitions (int, optional): Numbers of repetitions. Defaults to 5.

    :returns bool: True prompt create else False.
    """
    problem: dict = read_problem(
        task_id=task_id, language=language, problem_filename=problem_filename
    )
    prompt: str = problem.get("prompt", None)

    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    pipe: pipeline = connect_pipeline(model_name=model_name)
    while current_count < max_count:
        answer = run_model(problem=prompt, pipe=pipe)
        write_log(
            answer=answer,
            key=f"result_{current_count}",
            task_id=f"{language}/{task_id}",
            sub_folder=answer_sub_folder,
        )
        current_count += 1
    return True
