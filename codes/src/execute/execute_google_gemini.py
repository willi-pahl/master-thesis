"""
Create answers by Google Gemini.
"""

__VERSION__ = "0.0.1"

from google import genai
from google.genai import types


MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TOP_P: float = 0.95
MODEL_SETTING_TEMP: float = 0.2


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
    return genai.Client(vertexai=True, project=GOOGLE_PROJECT, location=GOOGLE_LOCATION)


def execute_prompt(
    prompt: str,
    model_name: str,
    prompt_repetitions: int = 5,
) -> list[str]:
    """
    Execute model with problem.

    :param prompt (str): Prompts with sample.
    :param model_name (str): Model name.
    :param prompt_repetitions (int, optional): Count of repetitions. Defaults to 5.
    :return bool: Answers by model.
    """
    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    client = connect_client()
    answers: list[str] = []
    while current_count < max_count:
        answers.append(run_model(problem=prompt, client=client, model_name=model_name))
        current_count += 1

    return answers
