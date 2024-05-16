from abc import ABC
from dataclasses import dataclass

from qwak.llmops.prompt.value import PromptValue


@dataclass
class BaseMessage(PromptValue, ABC):
    content: str


class AIMessage(BaseMessage):
    pass


class HumanMessage(BaseMessage):
    pass


class SystemMessage(BaseMessage):
    pass
