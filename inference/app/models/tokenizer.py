import tiktoken
import json

ENCODING = tiktoken.get_encoding("cl100k_base")

__all__ = [
    "estimate_input_tokens",
    "estimate_response_tokens",
    "string_tokens",
]


def _format_function_definitions(functions: list[dict]) -> str:
    lines = ["namespace functions {"]

    for func in functions:
        if func.get("description"):
            lines.append(f"// {func['description']}")

        if func["parameters"].get("properties"):
            lines.append(f"type {func['name']} = (_: {{")
            lines.append(_format_object_properties(func["parameters"], 0))
            lines.append("}) => any;")
        else:
            lines.append(f"type {func['name']} = () => any;")

        lines.append("")

    lines.append("} // namespace functions")
    return "\n".join(lines)


def _format_object_properties(parameters: dict, indent: int) -> str:
    indent_str = " " * indent
    lines = []

    properties = parameters.get("properties", {})
    required_properties = set(parameters.get("required", []))

    for name, param in properties.items():
        description = param.get("description")
        if description and indent < 2:
            lines.append(f"// {description}")
        is_required = name in required_properties
        type_annotation = _format_type(param, indent)
        lines.append(f"{name}{'?:' if not is_required else ':'} {type_annotation},")

    return "\n".join([indent_str + line for line in lines])


def _format_enum(enum, formatter=str):
    return " | ".join([formatter(v) for v in enum]) if enum else None


def _format_type(param: dict, indent: int) -> str:
    type_handlers = {
        "string": lambda p: _format_enum(p.get("enum"), formatter=lambda v: f'"{v}"'),
        "number": lambda p: _format_enum(p.get("enum")),
        "integer": lambda p: _format_enum(p.get("enum")),
        "array": lambda p: f"{_format_type(p['items'], indent)}[]" if p.get("items") else "any[]",
        "boolean": lambda p: "boolean",
        "null": lambda p: "null",
        "object": lambda p: "{\n" + _format_object_properties(p, indent + 2) + "\n}",
    }

    type_ = param["type"]
    formatted_enum = type_handlers.get(type_, lambda p: None)(param)
    return formatted_enum if formatted_enum is not None else type_


def _estimate_function_tokens(functions: list[dict]) -> int:
    tokens = len(functions)
    prompt_definitions = _format_function_definitions(functions)
    tokens += string_tokens(prompt_definitions)
    tokens += 9  # Add per completion
    return tokens


def string_tokens(string: str) -> int:
    global ENCODING
    return len(ENCODING.encode(string))


def _estimate_message_tokens(message: dict) -> int:
    tokens = 2  # each message adds 2 tokens
    components = []

    # Process and collect basic fields
    for key in ["role", "id"]:
        value = message.get(key)
        if value:
            components.append(value)
            if key == "id":
                tokens += 1

    # Handle the content field
    content = message.get("content")
    if isinstance(content, str):
        components.append(content)
    elif isinstance(content, list):
        for item in content:
            components.append(item.get("type"))
            if item.get("text"):
                components.append(item.get("text"))
            # TODO: Add token count for image

    # Handle function_calls field
    function_calls = message.get("function_calls")
    if function_calls:
        tokens += 3  # If there are function_calls, add 3 to tokens
        for call in function_calls:
            components += [call.get("id"), call.get("name"), json.dumps(call.get("arguments"), default=str)]

    # Calculate tokens
    tokens += sum(string_tokens(comp) for comp in components if comp is not None)

    # If role is function, adjust tokens
    if message.get("role") == "function":
        tokens -= 2

    return tokens


def estimate_input_tokens(messages: list[dict], functions: list[dict] = None, function_call=None) -> int:

    padded_system = False
    tokens = 0

    for msg in messages:
        if msg["role"] == "system" and functions and not padded_system:
            modified_message = {"role": msg["role"], "content": msg["content"] + "\n"}
            tokens += _estimate_message_tokens(modified_message)
            padded_system = True  # Mark system as padded
        else:
            tokens += _estimate_message_tokens(msg)

    tokens += 3  # Each completion has a 3-token overhead
    if functions:
        tokens += _estimate_function_tokens(functions)

    if functions and any(m["role"] == "system" for m in messages):
        tokens -= 4  # Adjust for function definitions

    if function_call and function_call != "auto":
        tokens += 1 if function_call == "none" else string_tokens(function_call) + 4

    return tokens


def estimate_response_tokens(response_message: dict) -> int:
    components = []
    tokens = 0
    if response_message.get("content"):
        tokens += 1
        components.append(response_message["content"])
    if response_message.get("function_calls"):
        tokens += 4
        for function_call in response_message["function_calls"]:
            components.append(function_call.get("name"))
            components.append(json.dumps(function_call.get("arguments")))
    components = [component for component in components if component]  # Filter out None values
    tokens += sum([string_tokens(component) for component in components])
    return tokens
