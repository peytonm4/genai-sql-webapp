import requests
import time
from typing import List, Optional, Dict, Any, Mapping
from get_resources_analysis import token_analysis


class GenAICenterLLM:
    # Set the url to access the GenAI Center LLM, with the endpoint being a specific function we want the LLM to achieve
    base_url = "change this url"
    endpoint = "change this endpoint"

    # Initialize the class by defining it with the api_key and model strings passed in when it is being invoked
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    # This function defines the attributes, formats the payload sent to the GenAi Center LLM so that it can be understood by the API

    def _call(
            self,
            messages: List[Dict[str, str]],
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            n: Optional[int] = None,
            stream: Optional[bool] = None,
            stop: Optional[List[str]] = None,
            max_tokens: Optional[int] = None,
            presence_penalty: Optional[float] = None,
            frequency_penalty: Optional[float] = None,
            logit_bias: Optional[Dict[int, float]] = None,
            user: Optional[str] = None,
            **kwargs: Any,
    ) -> Dict[str, Any]:
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
        }
        # Has defined how to access the LLM and the content that will be inputted
        # Function now posts a request to the API using json framework, and expects to receive output from the API
        start_time = time.time()
        # Add optional parameters to payload if provided
        payload["temperature"] = 0
        if top_p: payload["top_p"] = top_p
        if n: payload["n"] = n
        if stream: payload["stream"] = stream
        if stop: payload["stop"] = stop
        if max_tokens: payload["max_tokens"] = max_tokens
        if presence_penalty: payload["presence_penalty"] = presence_penalty
        if frequency_penalty: payload["frequency_penalty"] = frequency_penalty
        if logit_bias: payload["logit_bias"] = logit_bias
        if user: payload["user"] = user
        response = requests.post(f"{self.base_url}{self.endpoint}", headers=headers, json=payload)
        response.raise_for_status()
        print(response.elapsed.total_seconds())
        # Create a text file to log the performance of the model
        file1 = open("Model_Performance.txt", "w")
        file1.write('  ')
        file1.writelines(f'Execution Time: {response.elapsed.total_seconds()}')
        file1.write('  ')
        file1.close()
        # Return the expected response from the request that was posted to the API
        return response.json()

    # The prompt from the Custom LLM passes its content into this second call function as user_messages
    # This function calls the first _call function with this content to be passed as messages in the payload
    def __call__(self, user_messages: List[Dict[str, str]], **kwargs: Any) -> str:
        response = self._call(user_messages, **kwargs)

        # Then the function formats the response to output the answer given by the model,
        # Ignoring other feedback or attributes posted by the model
        # If the output is not as expected, it will return an error
        if response and response.get("choices"):
            # Assuming the first choice's content is the answer.
            token_analysis(response["usage"], self.model)
            return response["choices"][0]["message"]["content"]
        return "Error: No response from Gen AI Center."
