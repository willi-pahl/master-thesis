"""
Create answers by OpenAI models.

curl example:
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer <<OPEN_AI_KEY>>" \
  -H "OpenAI-Organization: <<OPEN_AI_ORG>>" \
  -H "OpenAI-Project: <<OPEN_AI_PROJECT>>"
"""

__VERSION__ = "0.0.1"

from openai import OpenAI

from src.execute.execute import (
    read_problem,
    write_log,
    MODEL_SETTING_MAX_TOKEN,
    MODEL_SETTING_TOP_P,
    MODEL_SETTING_TEMP,
)

OPEN_AI_KEY: str = "{openai-key}"
OPEN_AI_ORG: str = "org-{openai-organisation-id}"
OPEN_AI_PROJECT: str = "proj_{openai-project-id}"

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
    task_id: int,
    model_name: str,
    language: str,
    problem_filename: str,
    answer_sub_folder: str,
    prompt_repetitions: int = 10,
) -> bool:
    """
    Execute model.

    :param task_id (int): Problem id.
    :param model_name (str): Model name.
    :param language (str): Programming language.
    :param problem_filename (str): Benchmark file name.
    :param answer_sub_folder (str): Subfolder name for saving answers.
    :param prompt_repetitions (int, optional): Number of repetitions. Defaults to 5.

    :return bool: True answer create else False.
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
