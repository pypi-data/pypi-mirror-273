import logging
from typing import List, Dict, Any

import yaml

from prompeteer.providers.aws_bedrock.aws_llm_request import AWSLLMRequest
from prompeteer.providers.azure_openai.azure_llm_request import AzureLLMRequest
from prompeteer.providers.llm_request import ILLMRequest
from prompeteer.prompt.prompt import LLMProvider, DeclaredVariable, Variable
from prompeteer.utils.utils import normalize_keys, create_declared_variable_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptConfig:
    def __init__(self, version: str, name: str, llm_provider: LLMProvider, llm_request_config: Dict[str, Any],
                 variables: List[Dict], schema_version: str):
        self.version: str = version
        self.name: str = name
        self.schema_version: str = schema_version
        self.llm_provider: LLMProvider = llm_provider
        self.llm_request_config: Dict[str, Any] = llm_request_config
        self.declared_variables: List[DeclaredVariable] = create_declared_variable_list(variables)

    def to_llm_request(self, variables_to_inject: List[Variable]) -> ILLMRequest:
        if self.llm_provider == LLMProvider.azure:
            return AzureLLMRequest(variables_to_inject, self.declared_variables, **self.llm_request_config)
        elif self.llm_provider == LLMProvider.aws:
            return AWSLLMRequest(variables_to_inject, self.declared_variables, **self.llm_request_config)
        else:
            logger.error("Unsupported LLM")
            raise ValueError("Unsupported LLM")


def load_prompt_config(prompt_config_file_path) -> PromptConfig:
    with open(prompt_config_file_path, 'r') as file:
        prompt_config = yaml.safe_load(file)
        # Normalize keys to snake_case
        prompt_config = normalize_keys(prompt_config)

        name = prompt_config['name']
        version = prompt_config['version']
        schema_version = prompt_config['schema_version']
        try:
            provider = LLMProvider[prompt_config['provider']]
        except KeyError as e:
            logger.error(f"LLM Provider key missing: {e}")
            raise
        except ValueError as e:
            logger.error(f"LLM Provider not supported: {e}")
            raise
        request = prompt_config['request']
        variables = prompt_config['variables']
        return PromptConfig(name=name,
                            version=version,
                            llm_provider=provider,
                            llm_request_config=request,
                            variables=variables,
                            schema_version=schema_version)
