from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class Profile:
    """
    Profile structure, containing the name, domain ID, API key, and default
    read and write contexts.
    """
    name: str
    domain_id: str
    api_key: str
    default_read_context: Optional[str]
    default_write_context: Optional[str]

    @staticmethod
    def from_dict(json: Dict[str, Any]) -> "Profile":
        return Profile(**json)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
