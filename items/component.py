
from typing import Any


class Component:
    def __init__(self, item, amount) -> None:
        self.item = item
        self.amount = amount

    def __getattr__(self, attr):
        return getattr(self.item, attr)