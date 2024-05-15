from typing import Any, Callable, Dict, List, Optional

import antimatter.client as openapi_client
from antimatter.session_mixins.token import exec_with_token


class CapabilityMixin:
    """
    Session mixin defining CRUD functionality for capabilities.
    """

    def __init__(self, domain: str, client_func: Callable[[], openapi_client.ApiClient], **kwargs):
        try:
            super().__init__(domain=domain, client_func=client_func, **kwargs)
        except TypeError:
            super().__init__()  # If this is last mixin, super() will be object()
        self._domain = domain
        self._client_func = client_func

    @exec_with_token
    def get_capabilities(self) -> List[Dict[str, Any]]:
        """
        Get the capabilities for the session's domain.

        :return: A list of capabilities.
        """
        capabilities = []
        auth_api = openapi_client.AuthenticationApi(api_client=self._client_func())
        for capability in auth_api.domain_get_capabilities(domain_id=self._domain).capabilities:
            capabilities.append(capability.model_dump())
        return capabilities

    @exec_with_token
    def get_capability(self, name: str) -> Dict[str, Any]:
        """
        Get a specific capability for the session's domain.

        :param name: The name for this capability, like "admin"
        :return: The details of the capability.
        """
        auth_api = openapi_client.AuthenticationApi(api_client=self._client_func())
        return auth_api.domain_get_capability(domain_id=self._domain, capability=name).model_dump()

    @exec_with_token
    def put_capability(
            self,
            name: str,
            summary: str,
            description: Optional[str] = None,
            unary: bool = True,
            create_only: bool = False,
    ) -> None:
        """
        Create or update a capability. A capability is attached to authenticated
        domain identities by an identity provider, and confers additional permissions
        upon the identity. This is done by writing domain policy rules that reference
        the capability.

        :param name: The name for this capability, like "admin"
        :param summary: A short, single sentence description of this capability
        :param description: An optional longer form description of this capability
        :param unary: A unary capability does not have a value
        :param create_only:
        If True, an error will be returned if a capability with the name already exists
        """
        if description is None:
            description = ""
        auth_api = openapi_client.AuthenticationApi(api_client=self._client_func())
        auth_api.domain_put_capability(
            domain_id=self._domain,
            capability=name,
            new_capability_definition=openapi_client.NewCapabilityDefinition(
                unary=unary,
                summary=summary,
                description=description,
            ),
            createonly=create_only,
        )

    @exec_with_token
    def delete_capability(self, name: str) -> None:
        """
        Delete a capability.

        :param name: The name of the capability, like "admin"
        """
        auth_api = openapi_client.AuthenticationApi(api_client=self._client_func())
        auth_api.domain_delete_capability(domain_id=self._domain, capability=name)
