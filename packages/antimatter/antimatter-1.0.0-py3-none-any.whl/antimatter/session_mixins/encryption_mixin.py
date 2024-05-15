from typing import Callable

import antimatter.client as openapi_client
from antimatter.session_mixins.token import exec_with_token


class EncryptionMixin:
    """
    Session mixin defining CRUD functionality for encryption functionality.

    :param domain: The domain to use for the session.
    :param client: The client to use for the session.
    """

    def __init__(self, domain: str, client_func: Callable[[], openapi_client.ApiClient], **kwargs):
        try:
            super().__init__(domain=domain, client_func=client_func, **kwargs)
        except TypeError:
            super().__init__()  # If this is last mixin, super() will be object()
        self._domain = domain
        self._client_func = client_func

    @exec_with_token
    def flush_encryption_keys(self):
        """
        Flush all keys in memory. The keys will be immediately reloaded from persistent
        storage, forcing a check that the domain's root key is still available
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        encryption_api.domain_flush_encryption_keys(domain_id=self._domain)
