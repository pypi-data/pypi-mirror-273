from enum import Enum
from typing import Any, Dict


class OidcTokenType(str, Enum):
    """
    The enumerated supported OIDC token types.
    """
    Google = "GoogleToken"


class OidcToken:
    """
    The base OIDC token.
    """

    type: OidcTokenType

    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("must serialize specific token type")
