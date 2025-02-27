"""
Create answers by Hugging Face models.
"""

from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM

MODEL_PATH = "/huggingface/models/"

MODEL_SETTING_MAX_TOKEN: int = 600
MODEL_SETTING_TOP_P: float = 0.95
MODEL_SETTING_TEMP: float = 0.2


def run_local_model(prompt: str, model_name: str) -> str:
    """
    Connect to local model.

    :param problem (str): Prompt for model.

    :returns Result from model.
    """
    model_path: str = f"{MODEL_PATH}{model_name.replace('-', '_')}"

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype="auto", trust_remote_code=True
    )

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    generation_args = {
        "max_new_tokens": MODEL_SETTING_MAX_TOKEN,
        "temperature": MODEL_SETTING_TEMP,
        "top_p": MODEL_SETTING_TOP_P,
        "return_full_text": False,
        "do_sample": False,
    }

    output = pipe(prompt, **generation_args, pad_token_id=tokenizer.eos_token_id)
    if len(output) > 0:
        return output[0].get("generated_text", "")

    return ""


def execute_prompt(
    prompt: str, model_name: str, prompt_repetitions: int = 5
) -> list[str]:
    """
    Create prompts and save local.

    :param task_id (int): Problem id

    :returns bool: True prompt create.
    """
    if prompt is None:
        return False

    current_count: int = 0
    max_count: int = prompt_repetitions
    answers: list[str] = []
    while current_count < max_count:
        answers.append(run_local_model(prompt=prompt, model_name=model_name))
        current_count += 1

    return answers
