import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletion
from .base import BaseModel

MODEL_PRICES = {
    "gpt-3.5-turbo-0125": {"input_tokens": 0.0005 / 1000, "output_tokens": 0.0015 / 1000},
    "gpt-4-0125-preview": {"input_tokens": 0.01 / 1000, "output_tokens": 0.03 / 1000},
}


class OpenAIModel(BaseModel):
    def __init__(self, model_name: str, temperature=0):
        assert os.environ.get("OPENAI_API_KEY") is not None
        assert model_name in MODEL_PRICES.keys()
        self.model_name = model_name
        self.temperature = temperature
        self.client = OpenAI()

    @staticmethod
    def request_price(response: ChatCompletion):
        nr_tokens_input = response.usage.prompt_tokens
        nr_tokens_output = response.usage.completion_tokens
        price_dict = MODEL_PRICES[response.model]
        return nr_tokens_input * price_dict['input_tokens'] + nr_tokens_output * price_dict['output_tokens']

    def __call__(self, messages, response_type) -> (dict, float):
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            response_format={"type": response_type},
            messages=messages
        )

        price = OpenAIModel.request_price(response)

        if response_type == "text":
            return response.choices[0].message.content, price

        json_content = response.choices[0].message.content
        response_dict = json.loads(json_content)

        return response_dict, price
