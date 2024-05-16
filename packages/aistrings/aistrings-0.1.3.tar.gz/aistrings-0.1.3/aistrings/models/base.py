from typing import Literal


class BaseModel:
    @staticmethod
    def request_price(response):
        raise NotImplemented

    def __call__(self, messages: list[dict], response_type: Literal["text", "json_object"]):
        raise NotImplemented
