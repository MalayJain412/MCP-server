from abc import ABC, abstractmethod
from typing import Dict, Any

class CRMProvider(ABC):

    @abstractmethod
    def create_lead(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
