from dataclasses import dataclass
from typing import Any, Dict, Type

from antimatter.auth.config.tokens import OidcToken, OidcTokenType
from antimatter.auth.google.models import GoogleOidcToken

_NAME_KEY = "name"
_TOKEN_KEY = "token"
_TYPE_KEY = "type"


class OidcTokenFactory:
    """
    The token factory for converting config file keywords or CLI keywords into
    specific token formats.
    """

    @staticmethod
    def from_dict_type(token_type: str) -> Type["OidcToken"]:
        t = OidcTokenType(token_type)  # We'll raise an error here if the token type is invalid
        if t is OidcTokenType.Google:
            return GoogleOidcToken
        assert False  # Should be unreachable

    @staticmethod
    def from_cli_type(cli_type: str) -> Type["OidcToken"]:
        if cli_type == "google":
            return GoogleOidcToken
        raise ValueError(f"'{cli_type}' is not a supported token type")


@dataclass
class GlobalIdentity:
    """
    Global identity structure, containing name and token.
    """
    name: str
    token: OidcToken

    @staticmethod
    def from_dict(identity_dict: Dict[str, Any]) -> "GlobalIdentity":
        """
        Parse a GlobalIdentity from the json. The json must contain a 'token'
        property, which itself must contain a 'type' property that has a value
        that can be parsed into a specific token type.

        :param identity_dict: The json to parse
        :return: The parsed GlobalIdentity
        """
        name = identity_dict.get(_NAME_KEY)
        token = identity_dict.get(_TOKEN_KEY, {})
        token_cls = OidcTokenFactory.from_dict_type(token.get(_TYPE_KEY))
        token = {k: v for k, v in token.items() if k != _TYPE_KEY}
        return GlobalIdentity(name=name, token=token_cls(**token))

    def to_dict(self) -> Dict[str, Any]:
        return {
            _NAME_KEY: self.name,
            _TOKEN_KEY: self.token.to_dict(),
        }
