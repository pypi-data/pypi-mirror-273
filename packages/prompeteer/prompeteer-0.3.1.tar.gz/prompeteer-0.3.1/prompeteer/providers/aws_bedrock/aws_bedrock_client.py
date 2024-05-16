import json
import logging
from typing import Dict, Any

import boto3

from prompeteer.providers.aws_bedrock.aws_llm_request import AWSLLMRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from prompeteer.providers.llm_client import ILLMClient


class AwsBedrockClient(ILLMClient):
    def __init__(self):
        self.client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

    @retry(stop=stop_after_attempt(7), wait=wait_exponential(multiplier=1, min=2, max=10),
           retry=retry_if_exception(lambda e: True))
    def call(self, llm_request: AWSLLMRequest) -> str:
        try:
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

            response = self.client.invoke_model(body=json.dumps(params), modelId=llm_request.model)
            response_body = json.loads(response.get('body').read())

            if len(response_body['content']) == 0:
                raise ValueError("Empty response content, retrying...")

            return response_body['content'][0]['text']

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e
