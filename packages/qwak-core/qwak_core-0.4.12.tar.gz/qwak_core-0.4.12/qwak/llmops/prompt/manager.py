from typing import Optional

from qwak.llmops.prompt.base import BasePrompt, RegisteredPrompt


class PromptManager:
    def register(
        self,
        name: str,
        description: Optional[str],
        prompt: RegisteredPrompt,
    ) -> RegisteredPrompt:
        pass

    def update(
        self,
        name: str,
        description: str,
        prompt: BasePrompt,
        set_as_default: bool,
    ) -> RegisteredPrompt:
        pass

    def set_default(self, name: str, version: int):
        pass

    # Delete all versions of the prompt
    def delete_prompt(self, name: str):
        pass

    # Delete a specific version of the prompt, if it not the default one
    def delete_prompt_version(self, name: str, version: int):
        pass

    def get_prompt(self, name: str, version: Optional[int] = None) -> RegisteredPrompt:
        pass
