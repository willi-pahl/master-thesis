__VERSION__ = "0.0.1"

from google import genai
from google.genai import types

from src.execute.execute import (
    read_problem,
    write_log,
    MODEL_SETTING_MAX_TOKEN,
    MODEL_SETTING_TOP_P,
    MODEL_SETTING_TEMP,
)

GOOGLE_PROJECT: str = "XX-XXXxx"
GOOGLE_LOCATION: str = "us-central1"

ALLOWED_LLMS: list[dict] = [
    {"model": "gemini-1.5-pro-002", "answer_folder": "gemini15"},
    {"model": "gemini-2.0-flash-exp", "answer_folder": "gemini2"},
]

def run_model(problem: str, client: genai.Client, model_name: str) -> str:
    """
    Run Google model.

    :param problem (str): Problem or prompt.
    :param client (genai.Client): Gemini client.
    :param model_name (str): Gemini model name.
    :return (str): Model answer.
    """
    generate_content_config = types.GenerateContentConfig(
        temperature=MODEL_SETTING_TEMP,
        top_p=MODEL_SETTING_TOP_P,
        max_output_tokens=MODEL_SETTING_MAX_TOKEN,
        response_modalities=["TEXT"],
    )

    text: str = ""
    for chunk in client.models.generate_content_stream(
        model=model_name,
        contents=[problem],
        config=generate_content_config,
    ):
        text += chunk.text

    return text.rstrip()

def connect_client() -> genai.Client:
    """
    Get Gemini client.

    :return genai.Client: Gemini client.
    """
    return genai.Client(vertexai=True, project=GOOGLE_PROJECT,
                        location=GOOGLE_LOCATION)

def execute_prompt(
    task_id: int,
    model_name: str,
    language: str,
    problem_filename: str,
    answer_sub_folder: str,
    prompt_repetitions: int = 10,
) -> bool:
    """
    Execute model with problem.

    :param task_id (int): Problem task id.
    :param model_name (str): Model name.
    :param language (str): Programming language.
    :param problem_filename (str): File name with problem content.
    :param answer_sub_folder (str): Sub folder for save answer.
    :param prompt_repetitions (int, optional): Count of repetitions. Defaults to 10.
    :return bool: _description_
    """
    problem: dict = read_problem(
        task_id=task_id, language=language, problem_filename=problem_filename
    )
    prompt: str = problem.get("prompt", None)

    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    client = connect_client()
    while current_count < max_count:
        answer: str = ""
        answer = run_model(problem=prompt, client=client, model_name=model_name)
        write_log(
            answer=answer,
            key=f"result_{current_count}",
            task_id=f"{language}/{task_id}",
            sub_folder=answer_sub_folder,
        )
        current_count += 1
    return True
