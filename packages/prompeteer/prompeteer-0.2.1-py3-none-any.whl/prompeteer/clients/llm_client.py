import logging
from abc import abstractmethod, ABC
from typing import Dict

from prompeteer.clients.llm_request import ILLMRequest
from prompeteer.prompt.prompt import LLMProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ILLMClient(ABC):
    @abstractmethod
    def call(self, llm_request: ILLMRequest) -> str:
        raise NotImplementedError("LLM provider not implemented")


clients: Dict[str, ILLMClient] = {}


def _init_llm_client(provider: LLMProvider) -> ILLMClient:
    if provider == LLMProvider.azure:
        logger.info("Initializing Azure OpenAI LLM Client")
        from prompeteer.clients.azure_openai.azure_openai_client import AzureOpenAiClient
        return AzureOpenAiClient()
    elif provider == LLMProvider.aws:
        raise NotImplementedError("implement aws!")
    else:
        logger.error(f"Unknown LLM Provider {provider}")
        raise Exception(f"Unknown LLM Provider {provider}")


def get_llm_client(provider: LLMProvider) -> ILLMClient:
    assert provider is not None, "Provider must be provided"
    global clients
    if provider not in clients:
        clients[provider.value] = _init_llm_client(provider)
        logger.info(f"LLM Client for {provider} successfully initialized")
    return clients[provider.value]
