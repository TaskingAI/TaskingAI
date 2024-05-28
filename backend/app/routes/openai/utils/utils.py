from tkhelper.utils import generate_random_id

__all__ = [
    "generate_random_function_call_id",
    "generate_random_chat_completion_id",
]


def generate_random_function_call_id():
    """
    Generate a random function call ID.
    :return: The random function call ID.
    """
    return "P3lf" + generate_random_id(20)


def generate_random_chat_completion_id():
    """
    Generate a random chat completion ID.
    :return: The random chat completion ID.
    """
    return "chatcmpl-" + generate_random_id(29)
