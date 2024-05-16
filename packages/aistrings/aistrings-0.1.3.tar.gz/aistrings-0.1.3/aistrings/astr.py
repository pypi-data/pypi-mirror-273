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

    def find(self, query: str, targets: list[str]) -> tuple[str, int]:
        """
        Find the best matched target based on criterion.
        """
        messages = [
            {
                "role": "user",
                "content": f"You will receive a query and list of possible targets."
                           f"Find the target that is semantically the closest to the query."
                           f"Return the index of the matching target starting from 0. Return the index (not the matching target) and the index only!."
                           f"Query: {query}, Targets: {targets}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        try:
            index = int(response)
        except ValueError:
            # sometimes llm messes up and returns the target instead of the index
            try:
                index = targets.index(response)
            except ValueError:
                raise ValueError(f"Response {response} is not a valid index or target.")
        self.log(action_type='find', input_str=query, output_str=targets[index], cost=cost)
        return targets[index], index

    def split(self, text: str, criterion: str) -> list[str]:
        """
        Split text into a list of parts based on the criterion. Semantic version of text.split("str").
        """
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
        """
        Join a list of texts based on the criterion. Semantic version of "str".join(text_list).
        """
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

    def replace(self, text: str, criterion: str) -> str:
        """
        Replace parts of the text based on the criterion. Semantic version of text.replace("str1", "str2").
        """
        messages = [
            {
                "role": "user",
                "content": f"You will receive a text and a prompt explaining what needs to be replaced in the text."
                           f"Return the edited text only."
                           f"Text: {text}, Criterion: {criterion}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        self.log(action_type='replace', input_str=text, output_str=response, cost=cost)
        return response

    def substr(self, text: str, criterion: str) -> str:
        """
        Return a part of the text based on the criterion. Semantic version of text[n:m].
        """
        messages = [
            {
                "role": "user",
                "content": f"You will receive a text and a criterion for what needs to be found in the text."
                           f"Return the most relevant part based on the criterion. Bes short, you are allowed to use ellipsis to shorten the result."
                           f"Text: {text}, Criterion: {criterion}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="text")
        self.log(action_type='substr', input_str=text, output_str=response, cost=cost)
        return response

    def match(self, text: str, test_text: str) -> bool:
        """
        Return True if the topic in contained_text is also present in text, False otherwise.
        """
        messages = [
            {
                "role": "user",
                "content": f"You will receive a text and another test_text for what needs to be found in the text."
                           f"Return True if the topic in test_text is somehow also present in the text. "
                           f"False otherwise. Return json with the key is_match."
                           f"Text: {text}, Test text: {test_text}"
            },
        ]
        response, cost = self.model(messages=messages, response_type="json_object")
        self.log(action_type='match', input_str=text, output_str=response['is_match'], cost=cost)
        return response['is_match']


class HistoryItem(TypedDict):
    action_type: str
    input_str: str
    output_str: str
    cost: float
    timestamp: datetime.datetime
