from typing import Any, Callable, Dict, List

import antimatter.client as openapi_client
from antimatter.session_mixins.token import exec_with_token


class RootEncryptionKeyMixin:
    """
    Session mixin defining CRUD functionality for root encryption keys

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
    def get_active_root_encryption_key(self) -> Dict[str, Any]:
        """
        Get the active root encryption key

        :return: The active root encryption key
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        return encryption_api.domain_get_active_external_root_encryption_key(domain_id=self._domain).model_dump()

    @exec_with_token
    def list_root_encryption_keys(self) -> List[Dict[str, Any]]:
        """
        List all root encryption keys

        :return: A list of root encryption keys
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        return [key.model_dump() for key in encryption_api.domain_list_external_root_encryption_key(domain_id=self._domain)]

    @exec_with_token
    def test_root_encryption_key(self, root_encryption_key_id: str) -> Dict[str, Any]:
        """
        Attempt to test a root encryption key to encrypt and decrypt

        :param key: The key to test
        :return: The result of the test
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        return encryption_api.domain_external_root_encryption_key_test(
            domain_id=self._domain,root_encryption_key_id=root_encryption_key_id,
            body={}
        ).model_dump()
    
    @exec_with_token
    def add_root_encryption_key(self, key_infos: openapi_client.KeyInfos, description: str = "") -> str:
        """
        Add a new root encryption key.
        Use the builder functions in `antimatter.builders.root_encryption_key` to create the key information.

        For example:
        ```
        key_info = antimatter.builders.antimatter_delegated_aws_key_info(key_arn="key_arn")
        key_id = session.add_root_encryption_key(key_info)

        key_info = antimatter.builders.aws_service_account_key_info(
            access_key_id="access_key_id", secret_access_key
        )
        key_id = session.add_root_encryption_key(key_info)

        key_info = antimatter.builders.gcp_service_account_key_info(
            service_account_credentials="service_account_credentials", project_id="project_id", location="location"
        )
        key_id = session.add_root_encryption_key(key_info)
        ```

        :param key_infos: The key information to add
        :param description: The description of the key
        """
        assert key_infos is not None, "Key information is required"

        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        key_infos.description = description
        return encryption_api.domain_add_external_root_encryption_key(
            domain_id=self._domain,
            key_infos=key_infos
        ).rek_id

    @exec_with_token
    def delete_root_encryption_key(self, root_encryption_key_id: str):
        """
        Delete a root encryption key. Only possible if key is not in use by any data key encryption keys

        :param key: The key to delete
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        encryption_api.domain_delete_external_root_encryption_key(
            domain_id=self._domain,
            root_encryption_key_id=root_encryption_key_id
        )

    @exec_with_token
    def set_active_root_encryption_key(self, root_encryption_key_id: str) -> None:
        """
        Set the active root encryption key for the domain

        :param key: The key to set as active
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        encryption_api.domain_set_active_external_root_encryption_key(
            domain_id=self._domain,
            active_root_encryption_key_id=openapi_client.ActiveRootEncryptionKeyID(key_id=root_encryption_key_id)
        )

    @exec_with_token
    def rotate_encryption_keys(self) -> bool:
        """
        Rotates the root encryption keys. This is a batched operation and if 'True' is
        returned, this indicates whether there are more key encryption keys that can be rotated.
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        return encryption_api.domain_rotate_root_encryption_keys(
            domain_id=self._domain, body={},
        ).has_more

    @exec_with_token
    def list_key_providers(self) -> List[Dict[str, Any]]:
        """
        Retrieve the domain's key providers and a brief overview of their
        configuration.
        """
        encryption_api = openapi_client.EncryptionApi(api_client=self._client_func())
        res = encryption_api.domain_get_external_root_encryption_key_providers(domain_id=self._domain)
        if not res.providers:
            return []
        return [
            provider.actual_instance.model_dump()
            for provider in res.providers
            if provider.actual_instance is not None
        ]
