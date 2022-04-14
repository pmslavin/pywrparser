import json

from typing import Dict

from abc import (
    ABC,
    abstractmethod
)

class PywrType(ABC):
    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Dict]:
        return self.data

    def as_json(self) -> str:
        return json.dumps(self.data)
