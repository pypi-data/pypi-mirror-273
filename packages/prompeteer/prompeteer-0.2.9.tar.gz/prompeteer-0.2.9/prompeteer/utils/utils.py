# Author: Yoaz Menda
import re
from typing import List, Dict

from prompeteer.prompt.prompt import DeclaredVariable, Variable, Message


def camel_to_snake(name):
    """Convert camelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def normalize_keys(obj):
    """Recursively convert all keys in the dictionary from camelCase to snake_case."""
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = camel_to_snake(k)
            new_dict[new_key] = normalize_keys(v)
        return new_dict
    elif isinstance(obj, list):
        return [normalize_keys(item) for item in obj]
    else:
        return obj


def create_declared_variable_list(variables: List[dict]) -> List[DeclaredVariable]:
    declared_variables = []
    for info in variables:
        variable = DeclaredVariable(name=info['name'], required=info['required'])
        declared_variables.append(variable)
    return declared_variables


def inject_variables(messages: List[Dict], declared_variables: List[DeclaredVariable],
                     variables_to_inject: List[Variable]) -> List[Message]:
    # Convert variables_to_inject to a dictionary for easy lookup
    variables_dict = {var.name: var.value for var in variables_to_inject}

    # Create a set of declared variable names for validation
    declared_variable_names = {var.name for var in declared_variables}

    # Validate and replace placeholders
    results: List[Message] = []
    for msg in messages:
        content = msg['content']
        for var in declared_variables:
            placeholder = f"{{{var.name}}}"
            if placeholder in content:
                if var.name in variables_dict:
                    # Replace placeholder with variable value
                    content = content.replace(placeholder, variables_dict[var.name])
                else:
                    if var.required:
                        # Raise an exception if a required variable is missing
                        raise ValueError(f"Missing required variable: {var.name}")
                    else:
                        # Replace placeholder with an empty string for optional variables
                        content = content.replace(placeholder, "")

        results.append(Message(content=content, role=msg['role']))

    # Additional validations
    for var in declared_variables:
        placeholder = f"{{{var.name}}}"
        if var.required and not any(placeholder in msg['content'] for msg in messages):
            raise ValueError(f"Required placeholder {{{var.name}}} not found in any message content")

    for msg in messages:
        for word in msg['content'].split():
            if word.startswith('{') and word.endswith('}'):
                var_name = word[1:-1]
                if var_name not in declared_variable_names:
                    raise ValueError(f"Undefined placeholder {{{var_name}}} in message content")

    return results
