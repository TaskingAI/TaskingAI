import os
import re
from enum import Enum

sample_code_dict = {}

resource_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


class SampleCodeModule(str, Enum):
    ASSISTANT = "assistant"
    MODEL = "model"
    COLLECTION = "collection"


def trim_prefix(s: str):
    # Find the index of the first '_' character
    index = s.find("_")
    # If '-' is found, return the substring starting from the next character to the end
    if index != -1:
        return s[index + 1 :]

    # Return an empty string if '_' is not found
    return ""


def get_sample_codes(module: SampleCodeModule):
    global sample_code_dict
    if module not in sample_code_dict:
        sample_code_dict[module] = load_sample_code_for_module(module)
    return sample_code_dict[module]


def load_sample_code_for_module(module: SampleCodeModule):
    result = []
    assistant_directory_path = f"{resource_dir}/resources/code_templates/{module.value}"
    language_directory_paths = {}

    for entry in os.listdir(assistant_directory_path):
        full_path = os.path.join(assistant_directory_path, entry)
        if os.path.isdir(full_path):  # Check if it's a directory
            language_directory_paths[trim_prefix(entry)] = full_path

    for language in language_directory_paths:
        parts = []
        language_folder_path = language_directory_paths[language]

        for entry in os.listdir(language_folder_path):
            directory_path = os.path.join(language_folder_path, entry)
            part_name = trim_prefix(entry)
            templates = []

            for entry2 in os.scandir(directory_path):
                content = load_code_template(entry2.path)
                templates.append(
                    {
                        "template_name": reformat_string_to_headline(trim_prefix(entry2.name.replace(".md", ""))),
                        "content": content,
                        "variables": find_dollar_enclosed_substrings(content),
                    }
                )

            parts.append(
                {
                    "part_name": reformat_string_to_headline(part_name),
                    "templates": templates,
                }
            )

        result.append({"language_name": reformat_string_to_headline(language), "parts": parts})

    return result


def load_code_template(code_template_path: str):
    with open(code_template_path, "r") as file:
        return file.read()


def find_dollar_enclosed_substrings(s):
    # Define the regular expression pattern
    pattern = r"(\$\$.*?\$\$)"
    # Find all non-overlapping matches in the string
    matches = re.findall(pattern, s)
    # Return the list of matches
    return list(set(matches))


def reformat_string_to_headline(input_string):
    # Replace underscores with spaces
    formatted_string = input_string.replace("_", " ")
    # Capitalize the first letter of the sentence
    formatted_string = formatted_string.capitalize()
    return formatted_string.replace("python", "Python").replace("api", "API").replace("Api", "API")
