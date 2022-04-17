import json

from typing import Dict

from abc import (
    ABC,
    abstractmethod
)

from pywrparser.utils import PywrTypeValidator

class PywrType(ABC):

    data = PywrTypeValidator()

    def as_dict(self) -> Dict[str, Dict]:
        return self.data

    def as_json(self) -> str:
        return json.dumps(self.data)
