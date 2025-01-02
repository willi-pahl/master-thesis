"""
Work with Hugging Face models.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model_from_huggingface(root_name: str, vendor_name: str) -> None:
    """
    Load model from Hugging Face and save local.

    Args:
        root_name (str): Root name of model
        vendor_name (str): Vendor name of model
    """
    # Personal access token from Hugging Face.
    access_token = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    model_path_to_save = f"/huggingface/models/{vendor_name.replace('-', '_')}"

    tokenizer = AutoTokenizer.from_pretrained(f"{root_name}/{vendor_name}")
    model = AutoModelForCausalLM.from_pretrained(
        f"{root_name}/{vendor_name}", is_decoder=True, token=access_token
    )

    tokenizer.save_pretrained(model_path_to_save)
    model.save_pretrained(model_path_to_save)


# Example from https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct.
load_model_from_huggingface(root_name="Qwen", vendor_name="Qwen2.5-Coder-32B-Instruct")
