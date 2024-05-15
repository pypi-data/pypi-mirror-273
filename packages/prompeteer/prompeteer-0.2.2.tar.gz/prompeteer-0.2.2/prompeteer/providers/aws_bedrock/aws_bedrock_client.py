import json
import logging
from typing import Dict, Any

import boto3

from prompeteer.providers.aws_bedrock.aws_llm_request import AWSLLMRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from prompeteer.providers.llm_client import ILLMClient


def _init_aws_bedrock_client():
    pass


class AwsBedrockClient(ILLMClient):
    def __init__(self):
        self.client = _init_aws_bedrock_client()

    def call(self, llm_request: AWSLLMRequest) -> str:

        params: Dict[str, Any] = {
            'messages': [{'role': msg.role, 'content': msg.content} for msg in llm_request.messages],
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': llm_request.max_tokens
        }

        # Add optional parameters only if they are not None
        if llm_request.temperature is not None:
            params['temperature'] = llm_request.temperature
        if llm_request.top_p is not None:
            params['top_p'] = llm_request.top_p
        if llm_request.top_k is not None:
            params['top_k'] = llm_request.top_k
        if llm_request.stop_sequence is not None:
            params['stop_sequence'] = llm_request.stop_sequence

        bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        response = bedrock_runtime.invoke_model(body=json.dumps(params), modelId=llm_request.model)
        response_body = json.loads(response.get('body').read())

        return response_body
