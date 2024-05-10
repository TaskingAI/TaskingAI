import base64

__all__ = ["encode_text_to_base64", "decode_base64_to_text"]


def encode_text_to_base64(input_string, exclude_padding=False):
    """
    Encodes a given input text string to a Base64 encoded string.

    :param input_string: str - The string to be encoded.
    :param exclude_padding: bool - Whether to exclude the padding characters '=' from the output.
    :return: str - The Base64 encoded string.
    """

    # Convert the input string to bytes
    input_bytes = input_string.encode("utf-8")

    # Encode these bytes and then decode the result to get a string
    base64_bytes = base64.b64encode(input_bytes)
    base64_string = base64_bytes.decode("utf-8")

    # Optionally exclude the padding characters
    if exclude_padding:
        base64_string = base64_string.rstrip("=")

    return base64_string


def decode_base64_to_text(base64_string):
    """
    Decodes a Base64 encoded string back into a normal string.

    :param base64_string: str - The Base64 encoded string to be decoded.
    :return: str - The decoded string.
    """

    # Add padding characters to the base64 string if necessary
    padding = "=" * (-len(base64_string) % 4)
    base64_string_with_padding = base64_string + padding

    # Encode these bytes and then decode the result to get a string
    base64_bytes = base64_string_with_padding.encode("utf-8")

    # Decode the base64 bytes and then decode the result to get a string
    input_bytes = base64.b64decode(base64_bytes)
    input_string = input_bytes.decode("utf-8")

    return input_string
