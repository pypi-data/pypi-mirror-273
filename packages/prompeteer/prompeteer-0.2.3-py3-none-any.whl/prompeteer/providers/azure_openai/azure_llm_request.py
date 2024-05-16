import json
from typing import List, Optional, Union, Dict

from prompeteer.providers.llm_request import ILLMRequest
from prompeteer.prompt.prompt import Message, Variable, DeclaredVariable


class AzureLLMRequest(ILLMRequest):

    def __init__(self,
                 variables_to_inject: List[Variable],
                 declared_variables: List[DeclaredVariable],
                 model: str,
                 messages: List[Dict],
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 n: Optional[int] = None,
                 stream: Optional[bool] = None,
                 stop: Optional[Union[str, List]] = None,
                 max_tokens: Optional[int] = None,
                 presence_penalty: Optional[float] = None,
                 frequency_penalty: Optional[float] = None,
                 logit_bias: Optional[Dict] = None,
                 user: str = None):
        self.model = model
        self.messages: List[Message] = inject_variables(messages, declared_variables, variables_to_inject)
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.logit_bias = logit_bias
        self.user = user

    def get_prompt_text(self) -> str:
        result: List[Dict] = []
        for message in self.messages:
            result.append({
                'content': message.content,
                'role': message.role
            })
        return json.dumps(result)


def inject_variables(messages: List[Dict], declared_variables: List[DeclaredVariable],
                     variables_to_inject: List[Variable]) -> List[Message]:
    results: List[Message] = []
    for msg in messages:
        results.append(Message(content=msg['content'], role=msg['role']))
    return results
