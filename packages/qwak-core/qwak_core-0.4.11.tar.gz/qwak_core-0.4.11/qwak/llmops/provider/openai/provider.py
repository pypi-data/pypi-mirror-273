from typing import Union

from qwak.llmops.generation.chat.chat_completion import ChatCompletionGeneration
from qwak.llmops.generation.streaming import ChatCompletionStream
from qwak.llmops.model.descriptor import OpenAIChat
from qwak.llmops.prompt.chat.value import ChatPromptValue
from qwak.llmops.provider.openai.client import OpenAIClient


class OpenAIProvider:
    client: OpenAIClient

    def __init__(self):
        self.client = OpenAIClient()

    def create_chat_completion(
        self,
        chat_prompt_value: ChatPromptValue,
        chat_model_descriptor: OpenAIChat,
        stream: bool = False,
    ) -> Union[ChatCompletionGeneration, ChatCompletionStream]:
        # Handle openai api key
        # Handle `ChatPromptValue` role names
        d = chat_model_descriptor
        self.client.invoke_chat_completion(
            stream=stream,
            api_key="",
            model=d.model_id,
            messages=chat_prompt_value.to_string(),
            frequency_penalty=d.frequency_penalty,
            logit_bias=d.logit_bias,
            logprobs=d.logprobs,
            max_tokens=d.max_tokens,
            n=d.n,
            presence_penalty=d.presence_penalty,
            response_format=d.response_format,
            seed=d.seed,
            stop=d.stop,
            temperature=d.temperature,
            top_logprobs=d.top_logprobs,
            top_p=d.top_p,
            user=d.user,
        )
        pass
