from abc import ABC


class Context(ABC):
    def get_context(self) -> dict:
        pass
