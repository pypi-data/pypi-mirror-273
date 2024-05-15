import datetime
from typing import TypedDict

from .models.base import BaseModel
from .models.openai import OpenAIModel

MODEL_PROVIDERS = {
    'openai': OpenAIModel
}


class AiStrings:
    def __init__(self, provider_name: str, model_name: str, temperature=0):
        assert provider_name in MODEL_PROVIDERS.keys()
        self.model: BaseModel = MODEL_PROVIDERS[provider_name](model_name=model_name, temperature=temperature)
        self.cumulative_cost = 0
        self.history: list[HistoryItem] = []

    def reset_cost(self):
        self.cumulative_cost = 0

    def log(self, action_type: str, input_str: str, output_str: str, cost: float):
        self.history.append(
            {
                "action_type": action_type,
                "input_str": input_str,
                "output_str": output_str,
                "cost": cost,
                "timestamp": datetime.datetime.now()
            }
        )
        self.cumulative_cost += cost

    def log_history(self):
        print("History")
        print(f"----------------------")
        for h in self.history:
            print(
                f"  Action: {h['action_type']}\n"
                f"  Input: {h['input_str']}\n"
                f"  Output: {h['output_str']}\n"
                f"  Cost: {h['cost']}\n"
                f"  Time: {h['timestamp']}\n"
            )
        print(f"Total Cost: {self.cumulative_cost}")
        print(f"----------------------\n")

    # Operations
    def summarize(self, text: str) -> str:
        messages = [
            {
                "role": "user",
                "content": f"Summarize the the text, be brief, don't repeat yourself and return the summary only. Text: {text} "
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        self.log(action_type='summarize', input_str=text, output_str=response, cost=cost)
        return response

    def match(self, query: str, targets: list[str]) -> tuple[str, int]:
        messages = [
            {
                "role": "user",
                "content": f"You will receive a query and list of possible targets."
                           f"Find the target that is semantically the closest to the query."
                           f"Return the index of the matching target starting from 0. Return only the index."
                           f"Query: {query}, Targets: {targets}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        index = int(response)
        self.log(action_type='match', input_str=query, output_str=targets[index], cost=cost)
        return targets[index], index

    def split(self, text: str, criterion: str) -> list[str]:
        messages = [
            {
                "role": "user",
                "content": f"You will receive a text and criterion for how to split the text into a list."
                           f"Return the text split into a list based on the criterion as a json list with the key \"parts\"."
                           f"Text: {text}, Criterion: {criterion}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="json_object")
        self.log(action_type='split', input_str=text, output_str=response["parts"], cost=cost)
        return response["parts"]

    def join(self, text_list: list[str], criterion: str):
        messages = [
            {
                "role": "user",
                "content": f"You will receive a list of texts and a criterion for how to join the texts."
                           f"Return the texts joined together based on the criterion."
                           f"Texts: {text_list}, Criterion: {criterion}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        self.log(action_type='join', input_str=str(text_list), output_str=response, cost=cost)
        return response


class HistoryItem(TypedDict):
    action_type: str
    input_str: str
    output_str: str
    cost: float
    timestamp: datetime.datetime
