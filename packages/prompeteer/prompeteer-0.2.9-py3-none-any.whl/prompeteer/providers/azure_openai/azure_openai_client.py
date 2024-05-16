import logging
import os
from typing import Dict, Any

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

from prompeteer.providers.azure_openai.azure_llm_request import AzureLLMRequest
from prompeteer.providers.llm_client import ILLMClient

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureOpenAiClient(ILLMClient):
    def __init__(self):
        self.azure_resource_to_client_map: Dict[str, AzureOpenAI] = {}

    def call(self, llm_request: AzureLLMRequest) -> str:
        azure_resource_name = os.getenv('AZURE_OPENAI_RESOURCE_NAME')
        if azure_resource_name is None:
            logger.error("AZURE_OPENAI_RESOURCE_NAME environment variable is not set")
            raise Exception("AZURE_OPENAI_RESOURCE_NAME environment variable is not set")

        client = self.get_client_for_resource(azure_resource_name)

        params: Dict[str, Any] = {
            'messages': [{'role': msg.role, 'content': msg.content} for msg in llm_request.messages],
            'model': llm_request.model
        }

        # Add optional parameters only if they are not None
        if llm_request.temperature is not None:
            params['temperature'] = llm_request.temperature
        if llm_request.top_p is not None:
            params['top_p'] = llm_request.top_p
        if llm_request.n is not None:
            params['n'] = llm_request.n
        if llm_request.stream is not None:
            params['stream'] = llm_request.stream
        if llm_request.stop is not None:
            params['stop'] = llm_request.stop
        if llm_request.max_tokens is not None:
            params['max_tokens'] = llm_request.max_tokens
        if llm_request.presence_penalty is not None:
            params['presence_penalty'] = llm_request.presence_penalty
        if llm_request.frequency_penalty is not None:
            params['frequency_penalty'] = llm_request.frequency_penalty
        if llm_request.logit_bias is not None:
            params['logit_bias'] = llm_request.logit_bias
        if llm_request.user is not None:
            params['user'] = llm_request.user

        response: ChatCompletion = client.chat.completions.create(**params)

        if not response.choices:
            raise Exception('Failed to call Azure OpenAI Chat response')
        return response.choices[0].message.content

    def get_client_for_resource(self, azure_resource_name: str) -> AzureOpenAI:
        if azure_resource_name not in self.azure_resource_to_client_map:
            self.azure_resource_to_client_map[azure_resource_name] = AzureOpenAI(
                api_version="2024-02-01",
                azure_endpoint=f"https://{azure_resource_name}.openai.azure.com/",
                azure_ad_token_provider=token_provider
            )
        return self.azure_resource_to_client_map[azure_resource_name]
