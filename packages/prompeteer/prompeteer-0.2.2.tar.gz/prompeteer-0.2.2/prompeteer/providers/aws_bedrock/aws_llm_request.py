import json
from typing import List, Optional, Dict

from prompeteer.prompt.prompt import Message, Variable, DeclaredVariable
from prompeteer.providers.llm_request import ILLMRequest


class AWSLLMRequest(ILLMRequest):

    def __init__(self,
                 variables_to_inject: List[Variable],
                 declared_variables: List[DeclaredVariable],
                 max_tokens: int,
                 model: str,
                 messages: List[Dict],
                 system: Optional[str] = None,
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 top_k: Optional[float] = None,
                 stop_sequence: Optional[List[str]] = None):
        self.max_tokens = max_tokens
        self.model = model
        self.messages: List[Message] = inject_variables(messages, declared_variables, variables_to_inject)
        self.system = system
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stop_sequence = stop_sequence

    def get_prompt_text(self) -> str:
        messages: List[Dict] = []
        for message in self.messages:
            messages.append({
                'content': message.content,
                'role': message.role
            })
        result = dict()
        result['messages'] = messages
        if self.system is not None:
            result['system'] = self.system
        return json.dumps(result)


def inject_variables(messages: List[Dict], declared_variables: List[DeclaredVariable],
                     variables_to_inject: List[Variable]) -> List[Message]:
    results: List[Message] = []
    for msg in messages:
        results.append(Message(content=msg['content'], role=msg['role']))
    return results
