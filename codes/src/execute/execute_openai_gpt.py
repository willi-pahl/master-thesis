"""
Create answers by OpenAI ChatGPT.
"""

__VERSION__ = "0.0.1"

from openai import OpenAI

MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TOP_P: float = 0.95
MODEL_SETTING_TEMP: float = 0.2

OPEN_AI_KEY: str = "OPEN_AI_PERSONAL_KEY"
OPEN_AI_ORG: str = "org-XXXX"
OPEN_AI_PROJECT: str = "proj_YYYY"

ALLOWED_LLMS: list[dict] = [
    {"model": "gpt-3.5-turbo", "answer_folder": "gpt35"},
    {"model": "gpt-4-turbo", "answer_folder": "gpt4"},
]


def run_model(problem: str, client: OpenAI, model_name: str) -> str:
    """
    Run OpoenAI models.

    :param problem (str): Problem or prompt
    :param client (OpenAI): OpenAI client.
    :param model_name (str): OpenAI model name.
    :return str: Model answer.
    """
    completion = client.chat.completions.create(
        model=model_name,
        max_tokens=MODEL_SETTING_MAX_TOKEN,
        temperature=MODEL_SETTING_TEMP,
        top_p=MODEL_SETTING_TOP_P,
        messages=[
            {
                "role": "user",
                "content": problem,
            },
        ],
    )

    return completion.choices[0].message.content


def connect_client() -> OpenAI:
    """
    Get OpenAI client.

    :return OpenAI: OpenAI client.
    """
    return OpenAI(
        api_key=OPEN_AI_KEY,
        organization=OPEN_AI_ORG,
        project=OPEN_AI_PROJECT,
    )


def execute_prompt(
    prompt: str,
    model_name: str,
    prompt_repetitions: int = 10,
) -> list[str]:
    """
    Execute model.

    :param prompt (): Sample.
    :param model_name (str): Model name.
    :param prompt_repetitions (int, optional): _description_. Defaults to 5.
    :return bool: Answers.
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
