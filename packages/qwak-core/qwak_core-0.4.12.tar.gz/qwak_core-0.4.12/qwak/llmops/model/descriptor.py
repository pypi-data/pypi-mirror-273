from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Union


class ModelDescriptor(ABC):
    pass


class ChatModelDescriptor(ModelDescriptor):
    pass


@dataclass
class OpenAIChat(ChatModelDescriptor):
    model_id: str
    stream: bool = field(default=False)
    frequency_penalty: Optional[float] = field(default=None)
    logit_bias: Optional[Dict[str, int]] = field(default=None)
    logprobs: Optional[int] = field(default=None)
    max_tokens: Optional[int] = field(default=None)
    n: Optional[int] = field(default=None)
    presence_penalty: Optional[float] = field(default=None)
    response_format: Literal["text", "json_object"] = "text"
    seed: Optional[int] = field(default=None)
    stop: Union[Optional[str], List[str], None] = field(default=None)
    suffix: Optional[str] = field(default=None)
    temperature: Optional[float] = field(default=None)
    top_p: Optional[float] = field(default=None)
    top_logprobs: Optional[int] = field(default=None)
    user: Optional[str] = field(default=None)
