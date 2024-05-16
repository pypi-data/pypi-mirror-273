from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Union

from qwak.llmops.prompt.chat.message import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from qwak.llmops.prompt.chat.value import ChatPromptValue
from qwak.llmops.prompt.template import BasePromptTemplate, StringPromptTemplate


@dataclass
class BaseMessagePromptTemplate(BasePromptTemplate):
    @abstractmethod
    def render(self, variables: Dict[str, any]) -> BaseMessage:
        pass


@dataclass
class BaseStringMessagePromptTemplate(BaseMessagePromptTemplate, ABC):
    template: StringPromptTemplate = field(init=False)

    def __init__(self, template: str):
        self.template = StringPromptTemplate(template=template)


class AIMessagePromptTemplate(BaseStringMessagePromptTemplate):
    def render(self, variables: Dict[str, any]) -> BaseMessage:
        return AIMessage(content=self.template.render(variables=variables).to_string())


class HumanMessagePromptTemplate(BaseStringMessagePromptTemplate):
    def render(self, variables: Dict[str, any]) -> BaseMessage:
        return HumanMessage(
            content=self.template.render(variables=variables).to_string()
        )


class SystemMessagePromptTemplate(BaseStringMessagePromptTemplate):
    def render(self, variables: Dict[str, any]) -> BaseMessage:
        return SystemMessage(
            content=self.template.render(variables=variables).to_string()
        )


@dataclass
class ChatPromptTemplate(BasePromptTemplate):
    messages: List[Union[BaseMessage, BaseStringMessagePromptTemplate]]

    def render(self, variables: Dict[str, any]) -> ChatPromptValue:
        resulting_messages: List[BaseMessage] = list()

        for message in self.messages:
            if isinstance(message, BaseMessage):
                resulting_messages.append(message)
            elif isinstance(message, BaseStringMessagePromptTemplate):
                resulting_messages.append(message.render(variables=variables))
            else:
                raise ValueError(
                    f"Got unsupported message type: {repr(message)}. \n"
                    "Supported messages are: "
                    "AIMessagePromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, \n"
                    "AIMessage, HumanMessage, SystemMessage."
                )

        return ChatPromptValue(messages=resulting_messages)
