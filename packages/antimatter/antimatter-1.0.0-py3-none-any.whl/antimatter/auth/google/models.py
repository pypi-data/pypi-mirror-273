from dataclasses import asdict, dataclass
from typing import Any, Dict

from antimatter.auth.config.tokens import OidcToken, OidcTokenType


@dataclass
class GoogleOidcToken(OidcToken):
    """
    The Google OIDC token format.
    """
    access_token: str
    id_token: str
    refresh_token: str
    expires_at: int
    type: OidcTokenType = OidcTokenType.Google

    def to_dict(self) -> Dict[str, Any]:
        json = asdict(self)
        json["type"] = self.type.value
        return json
