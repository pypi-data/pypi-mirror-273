import os
from typing import Dict, List, Literal, Optional, Union

import requests
from qwak.llmops.generation.streaming import ChatCompletionStream
from qwak.llmops.prompt.base import ChatCompletionGeneration
from qwak.utils.dict_utils import remove_none_value_keys
from requests import Session


class OpenAIClient:
    http_session: Session
    base_url: str = os.environ.get("_QWAK_OPEN_AI_BASE_URL", None)
    timeout_seconds: float = os.environ.get("_QWAK_OPEN_TIMEOUT", 5.0)

    def __init__(self):
        self.http_session = requests.session()

    def invoke_chat_completion(
        self,
        api_key: str,
        model: str,
        messages: str,
        frequency_penalty: Optional[float],
        logit_bias: Optional[Dict[str, int]],
        logprobs: Optional[bool],
        max_tokens: Optional[int],
        n: Optional[int],
        presence_penalty: Optional[float],
        response_format: Literal["text", "json_object"],
        seed: Optional[int],
        stop: Union[Optional[str], List[str]],
        stream: Optional[bool],
        temperature: Optional[float],
        # tool_choice: ChatCompletionToolChoiceOptionParam,
        # tools: Iterable[ChatCompletionToolParam],
        top_logprobs: Optional[int],
        top_p: Optional[float],
        user: Optional[str],
        extra_headers: Optional[Dict[str, str]] = None,
        extra_body: Optional[Dict[str, str]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Union[ChatCompletionGeneration, ChatCompletionStream]:
        # url: str = urljoin(self.base_url, "v1/chat/completions")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body = {
            "messages": messages,
            "model": model,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "max_tokens": max_tokens,
            "n": n,
            "presence_penalty": presence_penalty,
            "response_format": response_format,
            "seed": seed,
            "stop": stop,
            "stream": stream,
            "temperature": temperature,
            # "tool_choice": json.dumps(tool_choice),
            # "tools": json.dumps(tools),
            "top_logprobs": top_logprobs,
            "top_p": top_p,
            "user": user,
        }
        body = remove_none_value_keys(body)

        if extra_headers:
            headers.update(extra_headers)

        if extra_body:
            body.update(extra_body)

        return ChatCompletionGeneration()
