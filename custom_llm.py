from typing import Any, List, Mapping, Optional
from genai_center_integration import GenAICenterLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
import os

class CustomLLM(LLM):
    #Specify the model and api_key as string objects
    model: str
    api_key: str

    #Allows langchain to identify the wrapper as custom LLM wrapper
    @property
    def _llm_type(self) -> str:
        return "custom"

    # When the Custom LLM Class is invoked, it calls this function, and specifies the necessary attributes
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
    # This format gives a basic instruction to the LLM
    # Provides a tempalate for a prompt formatted as a string to be passed through to the LLM
        message = [{
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        }, {
            "role": "user",
            "content": prompt
        }]
        # We then define the Custom LLM that we are going to access
        # Passing the previously defined message as a user message into the Gen AI Center LLM
        # Returns the output of the GenAI Center class calling the GenAI Center LLM
        llm = GenAICenterLLM(model=self.model, api_key=self.api_key)
        return llm(user_messages=message)
