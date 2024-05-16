# Author: Yoaz Menda
import re
from typing import List

from prompeteer.prompt.prompt import DeclaredVariable


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
