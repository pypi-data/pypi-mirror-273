from abc import abstractmethod, ABC


class ILLMRequest(ABC):
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def get_prompt_text(self) -> str:
        raise NotImplementedError
