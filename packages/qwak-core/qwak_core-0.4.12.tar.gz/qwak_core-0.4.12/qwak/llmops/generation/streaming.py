from abc import ABC
from typing import Generic, TypeVar

from qwak.llmops.generation.chat.chat_completion import ChatCompletionChunk

_T = TypeVar("_T")


class Stream(Generic[_T], ABC):
    pass


class ChatCompletionStream(Stream[ChatCompletionChunk]):
    pass
