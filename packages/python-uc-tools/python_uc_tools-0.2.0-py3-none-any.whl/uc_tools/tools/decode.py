import base64


def base64_decode(input_: str, encoding: str = 'utf-8') -> str:
    """
    Decode a base64-encoded string into a regular string.

    Args:
        input (str): The base64-encoded string to decode.
        encoding (str): The encoding to use when decoding the bytes.

    Returns:
        str: The decoded string.
    """
    decoded_bytes: bytes = base64.b64decode(input_)
    return decoded_bytes.decode(encoding)
