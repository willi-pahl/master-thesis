"""
Create answers by Ollama.
"""

__VERSION__ = "0.0.1"

from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate


MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TOP_P: float = 0.95
MODEL_SETTING_TEMP: float = 0.2

MODEL_CONNECT_HOST: str = "192.168.178.140"
MODEL_CONNECT_PORT: str = "11434"


def run_model(problem: str, model: OllamaLLM) -> str:
    """
    Connect to ollama model server.

    :param problem (str): Prompt there is send to ollama server.
    :param model (OllamaLLM) Connected model.
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
    prompt: str,
    model_name: str,
    prompt_repetitions: int = 5,
) -> list[str]:
    """
    Create prompts and save local.

    :param problem (str): Problem or prompt.
    :param model_name (str): Ollama model name.
    :param prompt_repetitions (int, optional): _description_. Defaults to 5.
    :return (str): Model answer.
    """
    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    model = connect_model(model_name=model_name)
    answers: list[str] = []
    while current_count < max_count:
        answers.append(run_model(problem=prompt, model=model))
        current_count += 1

    return answers
