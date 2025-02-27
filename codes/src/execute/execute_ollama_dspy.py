"""
Create answers by Ollama with DSPy.
"""

__VERSION__ = "0.0.1"

import dspy


MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TOP_P: float = 0.95
MODEL_SETTING_TEMP: float = 0.8  # eigetlich 0.2

MODEL_CONNECT_HOST: str = "192.168.178.140"
MODEL_CONNECT_PORT: str = "11434"


class BasicProgramming(dspy.Signature):
    """
    Custom signature.

    Args:
        dspy (_type_): Base signature from dspy.
    """

    question: str = dspy.InputField(desc="Eine Frage zu PHP Programmierung")
    answer: str = dspy.OutputField(desc="Generiere Programmcode")


def run_model(prompt: str, model: dspy.LM) -> str:
    """
    Connect to ollama model server.

    :param prompt (str): Prompt there is send to ollama server.
    :return Result from ollama server by prompt.
    """
    model(messages=[{"role": "user", "content": "Du bist erfahrener PHP Entwickler"}])
    chain_elem = dspy.ChainOfThought(BasicProgramming)
    pred = chain_elem(question=prompt)

    return pred.answer


def connect_model(model_name: str) -> dspy.LM:
    """
    Connect Ollama hosted model

    :param model_name (str): Model name.
    :return OllamaLLM: Connected model.
    """
    llm: dspy.LM = dspy.LM(
        model=f"ollama_chat/{model_name}",
        api_base=f"http://{MODEL_CONNECT_HOST}:{MODEL_CONNECT_PORT}",
        api_key="",
        temperature=MODEL_SETTING_TEMP,
        cache=False,
        cache_in_memory=False,
        max_tokens=4096,
        num_retries=2,
    )
    dspy.configure(lm=llm)

    return llm


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
        answers.append(run_model(prompt=prompt, model=model))
        current_count += 1

    return answers
