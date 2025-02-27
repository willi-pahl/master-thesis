"""
The script downloads and temporarily saves a model of Hugging Face and provides the prompt.
"""

__VERSION__ = "0.0.1"

from transformers import AutoModelForCausalLM, AutoTokenizer


def run_local_model_after_download(root_name: str, vendor_name: str, prompt: str) -> list:
    """
    Load model from Hugging Face and call the model with prompt.

    Args:
        root_name (str): Model root name.
        vendor_name (str): Model vendor name.
        prompt (str): Prompt for model.

    Returns:
        list: Answer from model.
    """
    model_name: str = f"{root_name}/{vendor_name}"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    messages = [
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(**model_inputs, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

# Example: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
run_local_model_after_download(
    root_name="TinyLlama",
    vendor_name="TinyLlama-1.1B-Chat-v1.0",
    prompt="Write a quick sort algorithm.",
)

# Example: https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
run_local_model_after_download(
    root_name="Qwen",
    vendor_name="Qwen2.5-Coder-32B-Instruct",
    prompt="Write a quick sort algorithm.",
)
