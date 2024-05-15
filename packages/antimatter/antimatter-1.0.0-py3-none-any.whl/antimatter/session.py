import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union, Dict
from urllib.parse import quote_plus, urlparse

import antimatter_engine as am

from antimatter.auth.config.auth_config import AuthConfig
from antimatter.filetype.extract import extract_from_file
from antimatter.filetype.infer import infer_filetype

import antimatter.client as openapi_client
import antimatter.handlers as handlers
from antimatter.cap_prep.prep import Preparer
from antimatter.tags import ColumnTag, SpanTag
from antimatter.capsule import Capsule, CapsuleBindings
from antimatter.client import ApiClient, Configuration, GeneralApi
from antimatter.datatype.datatypes import Datatype
from antimatter.datatype.infer import infer_datatype
from antimatter.errors import errors
from antimatter.extra_helper import extra_for_session
from antimatter.session_mixins import *

# #version
API_TARGET_VERSION = "v1"


def new_domain(
    email: str,
    display_name: Optional[str] = None,
    config_path: Optional[str] = None,
    add_to_config: bool = True,
    make_active: bool = False,
) -> "Session":
    """
    Create a new domain with the provided email as the admin contact. A
    verification email will be sent to that email. Verification must be completed
    before the Antimatter API can be interacted with.

    :param email: The admin contact email used for email verification
    :param display_name: The display name for the new domain
    :param config_path: The path to the domain profile config file; default is ~/.antimatter/config
    :param add_to_config: Whether to add the new domain to the config file; default is True
    :param make_active: Whether to make the new domain the active profile in the config file; default is False
    :return: A Session holding the newly created domain_id and api_key
    """
    host = os.getenv("ANTIMATTER_API_URL", "https://api.antimatter.io")
    client = GeneralApi(
        api_client=ApiClient(
            configuration=Configuration(
                host=f"{host}/{API_TARGET_VERSION}",
            )
        )
    )
    dm = client.domain_add_new(openapi_client.NewDomain(admin_email=email, display_name=display_name))

    # Try to create the Session before potentially adding to the config file - if creating
    # the Session produces an erroneous result, we don't want to add it to the config
    sess = Session(domain=dm.id, api_key=dm.api_key, email=email)

    if add_to_config or make_active:
        auth_conf = AuthConfig.from_file(config_path)
        try:
            auth_conf.add_profile(
                domain_id=dm.id,
                api_key=dm.api_key,
                name=display_name,
                mark_active=make_active,
                write_to_file=True,
            )
        except Exception as e:
            # Catch any failures as we don't want the caller to lose the domain ID and API key
            # if saving to a config file goes wrong
            print(f"error saving profile to config file: {e}", file=sys.stderr)

    # Finally, return the Session
    return sess


def with_domain(domain_id: str, api_key: str) -> "Session":
    """
    Create a session using an existing domain ID and API key.

    :param domain_id: The domain ID
    :param api_key: The API key for the domain
    :return: A Session holding the existing domain_id and api_key
    """
    return load_domain(domain_id=domain_id, api_key=api_key)


def load_domain(
    domain_id: Optional[str] = None,
    api_key: Optional[str] = None,
    display_name: Optional[str] = None,
    config_path: Optional[str] = None,
    add_to_config: bool = False,
    make_active: bool = False,
) -> "Session":
    """
    Load an existing domain. There are several different ways to specify the domain
    credentials to use, from highest to lowest priority.

    1. Using display name. If this is present, it will attempt to load a profile
    from the config file with this name.
    2. Using domain_id and api_key as the credentials.
    3. Using only domain_id. If this is present, it will attempt to load a profile
    from the config file that matches this domain ID.

    If domain_id is not provided, this will check the ANTIMATTER_DOMAIN_ID env var
    for a domain ID.

    If api_key is not provided, this will check the ANTIMATTER_API_KEY env var for
    an API key.

    The config file is by default expected to exist at ~/.antimatter/config, but an
    override location can be provided with the config_path argument, or the
    ANTIMATTER_CONFIG_PATH env var.

    By default, loading an existing domain will not add the credentials to the profile
    auth config file. Set add_to_config to True to add this domain to the config. To
    make this domain the active profile, set make_active to True. Note that setting
    make_active to True implicitly sets add_to_config to True.

    :param domain_id: The domain ID of the domain to load
    :param api_key: The API key of the domain to load
    :param display_name: The display name in the auth config file of the domain to load
    :param config_path: The path to the domain profile config file; default is ~/.antimatter/config
    :param add_to_config: Whether to add the domain to the config file; default is False
    :param make_active: Whether to make the domain the active profile in the config file; default is False
    :return: A Session holding the existing domain_id and api_key
    """
    if not domain_id:
        domain_id = os.getenv("ANTIMATTER_DOMAIN_ID", None)
    if not api_key:
        api_key = os.getenv("ANTIMATTER_API_KEY", None)
    if not config_path:
        config_path = os.getenv("ANTIMATTER_CONFIG_PATH", None)

    # If a domain and API key are available, and no display name was specified, and no flags
    # have been set to save to the config file, skip loading the auth config profiles
    # because we won't use them
    if not display_name and domain_id and api_key and not add_to_config and not make_active:
        auth_conf = AuthConfig()
    else:
        auth_conf = AuthConfig.from_file(config_path)

    name = None
    from_conf = False

    # If a display name is specified, load that profile
    if display_name:
        pconf = auth_conf.get_profile(name=display_name)
        if pconf is None:
            raise errors.SessionLoadError(f"could not find profile {display_name} in profile config")
        name = pconf.name
        domain_id = pconf.domain_id
        api_key = pconf.api_key
        from_conf = True
    # If a domain ID is specified, but not an API key, load the profile with that domain ID
    elif domain_id and not api_key:
        pconf = auth_conf.get_profile(domain_id=domain_id)
        if pconf is None:
            raise errors.SessionLoadError(f"could not find profile with domain ID {domain_id} in profile config")
        name = pconf.name
        api_key = pconf.api_key
        from_conf = True
    # If no display name or domain ID were specified, load the active profile from the auth config
    # We deliberately aren't confirming the API key is unset here, due in part to the issue where the
    # Session sets the env var
    elif not domain_id:
        pconf = auth_conf.get_profile()
        if pconf is None:
            raise errors.SessionLoadError("no active profile found")
        name = pconf.name
        domain_id = pconf.domain_id
        api_key = pconf.api_key
        from_conf = True

    # If we get to this point without a domain ID and API key, we somehow failed to load the domain
    if not domain_id or not api_key:
        raise errors.SessionLoadError("failed to load domain - no domain ID or API key found")

    # Try to initialize the Session before potentially adding to the config file - if initializing
    # the Session produces an erroneous result, we don't want to add it to the config
    sess = Session(domain=domain_id, api_key=api_key)

    # If the flag is set to add to the auth config, and the profile didn't already come from the
    # auth config, then write it to the config, marking as active if that flag is also set
    if (add_to_config or make_active) and not from_conf:
        auth_conf.add_profile(
            domain_id=domain_id,
            api_key=api_key,
            name=name,
            mark_active=make_active,
            write_to_file=True,
        )

    # Finally, return the session
    return sess


@dataclass
class EncapsulateResponse:
    """
    EncapsulateResponse contains metadata from encapsulating data, including
    the capsule ID or IDs, and the raw bytes if the capsule was not exported.
    """
    capsule_ids: List[str]
    raw: Optional[bytes]
    load_capsule_func: Optional[
        Callable[
            [Optional[str], Optional[Union[bytes, "EncapsulateResponse"]], str],
            Optional[Capsule]
        ]
    ]

    def load(self, read_context: str) -> Optional[Capsule]:
        """
        Load the response into a capsule. Note that this shortcut requires that
        the raw data be returned from the encapsulation.

        :param read_context: The name of the role policy to use for reading data
        :return: The loaded capsule, if the raw data was present on the response.
        """
        return self.load_capsule_func(None, self, read_context)

    def save(self, filename: str):
        """
        Save the capsule to a file
        """
        with open(filename, "wb") as f:
            f.write(self.raw)


class Session(
    CapabilityMixin, CapsuleMixin, DomainMixin, EncryptionMixin,
    FactMixin, GeneralMixin, IdentityProviderMixin, PolicyRuleMixin,
    ReadContextMixin, WriteContextMixin, VerificationMixin, RootEncryptionKeyMixin
):
    """
    The Session establishes auth and the domain you are working with, providing
    both a standard instantiation or a context manager in which a Capsule and
    its underlying data can be interacted with.
    """

    def __init__(self, domain: str, api_key: str, email: Optional[str] = None):
        self._domain = domain
        self._api_key = api_key
        self._email = email
        os.environ['ANTIMATTER_API_KEY'] = api_key
        self._try_init_client(default_values_on_failure=True)
        super().__init__(
            domain=domain,
            api_key=api_key,
            client_func=self._get_client,
            session=self._session,
            email=self._email,
        )

    @property
    def domain_id(self):
        """
        Return the current domain ID
        """
        return self._domain

    @property
    def api_key(self):
        """
        Return the api key in use by this session
        """
        return self._api_key

    def __enter__(self):
        # TODO: handle any resources/auth; call python rust wrapper to create a rust session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: close any resources/auth; call python rust wrapper to close the rust session
        return

    def _get_client(self) -> ApiClient:
        return self._client

    def config(self):
        """
        Returns the configuration of this Session
        """
        return {
            "domain": self._domain,
            "api_key": self._api_key,
            "email": self._email,
        }

    def _try_init_client(self, default_values_on_failure: bool = False) -> bool:
        """
        Try to initialize the client and session with the domain and API key.
        If default_values_on_failure is True, an empty underlying session and
        default client with no authentication will be created if the domain has
        not yet been verified.

        :param default_values_on_failure: Whether to set default client and session values on failure
        :return: True if the client and session were authenticated
        """
        host = os.getenv("ANTIMATTER_API_URL", "https://api.antimatter.io")
        try:
            self._session = am.PySession(self._domain)
            self._client = ApiClient(
                configuration=Configuration(
                    host=f"{host}/{API_TARGET_VERSION}", access_token=self._api_key,
                )
            )
        except Exception as e:
            str_e = str(e).lower()
            # Catch the error where the domain is still awaiting verification
            if "code: 401" not in str_e or "domain contains no verified contacts" not in str_e:
                if "domain auth error" in str_e:
                    if "code: 400" in str_e and "apikey" in str_e and "failed to identify the token" in str_e:
                        raise errors.SessionError(
                            f"domain auth error: failed to identify the API key '{self._api_key}', please check format",
                        ) from None
                    elif "code: 404" in str_e and "antimatter domain" in str_e and "does not exist" in str_e:
                        raise errors.SessionError(f"domain auth error: domain '{self._domain}' does not exist") from None
                    elif "code: 404" in str_e and "page not found" in str_e:
                        raise errors.SessionError(
                            f"domain auth error: failed to identify domain '{self._domain}', please check format",
                        ) from None
                    elif "code: 400" in str_e and "apikey" in str_e and "invalid" in str_e:
                        raise errors.SessionError("domain auth error: invalid domain or API key provided") from None
                    else:
                        raise
                else:
                    raise
            if default_values_on_failure:
                # Set up a default empty session and client without auth
                self._session = None
                self._client = ApiClient(configuration=Configuration(host=f"{host}/{API_TARGET_VERSION}"))
            return False

        return True

    def load_capsule(
        self,
        path: Optional[str] = None,
        data: Optional[Union[bytes, EncapsulateResponse]] = None,
        read_context: str = None,
        read_params: Dict[str, str] = {},
    ) -> Optional[Capsule]:
        """
        load_capsule creates a capsule, extracting data from an Antimatter
        Capsule binary blob, either provided in raw bytes or as a string path
        to a local or remote file.

        If the `as_datatype` parameter is supplied and the data is a binary blob
        Antimatter Capsule, the data will be extracted in that format. If the
        data is data for saving to an Antimatter Capsule, `as_datatype` will
        specify the default format for the data when loaded from the blob.

        :param path: The location of the Capsule as a local or remote path.
        :param data: The data to load into an Antimatter Capsule.
        :param read_context: The name of the role policy to use for reading data
        """
        if self._session is None:
            if not self._try_init_client():
                raise errors.SessionVerificationPendingError(ADMIN_VERIFICATION_PROMPT)

        if not read_context:
            raise ValueError("specify a 'read_context' when loading a capsule")

        if not path and not data:
            raise ValueError("specify a 'path' or the raw 'data' when loading a capsule")

        if data and isinstance(data, EncapsulateResponse):
            data = data.raw

        try:
            capsule_session = self._session.open_capsule(read_context, read_params, path, data)
            cap = CapsuleBindings(capsule_session)
            capsule = Capsule(capsule_binding=cap)
            return capsule
        except Exception as e:
            str_e = str(e).lower()
            if "read_context" in str_e or "readcontext" in str_e:
                raise errors.CapsuleLoadError(
                    f"failed to load capsule: check that read context {read_context} exists for domain",
                ) from None
            raise errors.CapsuleLoadError("loading data from capsule") from e

    def encapsulate(
        self,
        data: Any = None,
        write_context: str = None,
        span_tags: List[SpanTag] = None,
        column_tags: List[ColumnTag] = None,
        as_datatype: Union[Datatype, str] = Datatype.Unknown,
        skip_classify_on_column_names: List[str] = None,
        path: Optional[str] = None,
        subdomains_from: Optional[str] = None,
        create_subdomains: Optional[bool] = False,
        data_file_path: Optional[str] = None,
        data_file_hint: Optional[str] = None,
        **kwargs,
    ) -> EncapsulateResponse:
        """
        Saves the provided Capsule's data, or the provided data using the provided
        write context. If 'as_datatype' is provided, the default datatype for the
        raw data will use the specified type.

        One of 'data' or 'path' must be provided.

        :param data: Raw data in a Capsule-supported format
        :param write_context: The name of the role policy to use for writing data
        :param span_tags: The span tags to manually apply to the data
        :param column_tags: Tags to apply to entire columns by name
        :param as_datatype: The datatype to override the provided data with when the capsule is read
        :param skip_classify_on_column_names: List of columns to skip classifying
        :param path: If provided, the local or remote path to save the capsule to
        :param subdomains_from: column in the raw data that represents the subdomain
        :param create_subdomains: allow missing subdomains to be created
        :param data_file_path: Optional path to a file containing data to be read. If provided, data from
                this file will be used instead of the 'data' parameter.
        :param data_file_hint: Optional hint indicating the format of the data in the file specified by
                'data_file_hint'. Supported formats include 'json', 'csv', 'txt', 'parquet'.
                If not specified, data will be read as plain text.
        :return: The response containing capsule metadata and the raw blob of the
                capsule if no path was provided.
        """
        if self._session is None:
            if not self._try_init_client():
                raise errors.SessionVerificationPendingError(ADMIN_VERIFICATION_PROMPT)

        if data is None and path is None:
            raise ValueError("specify one of 'data' or 'path' when creating a capsule")

        as_datatype = Datatype(as_datatype)
        if column_tags is None:
            column_tags = []
        if span_tags is None:
            span_tags = []
        if skip_classify_on_column_names is None:
            skip_classify_on_column_names = []

        if not write_context:
            raise ValueError("specify a 'write_context' when creating a capsule")

        if data_file_path:
            if not data_file_hint:
                data_file_hint = infer_filetype(data_file_path)
                if not data_file_hint:
                    raise TypeError("unable to infer data file type, provide 'data_file_hint' argument")
            data = extract_from_file(data_file_path, data_file_hint)

        dt = infer_datatype(data)
        if dt is Datatype.Unknown:
            if as_datatype is Datatype.Unknown:
                raise TypeError("unable to infer type of data, provide 'as_datatype' argument")
            dt = as_datatype

        h = handlers.factory(dt)
        col_names, raw, extra = h.to_generic(data)
        extra = extra_for_session(dt, {**extra, **kwargs})
        jextra = json.dumps(extra)

        # if a cell path is not specified, assume it means the first cell
        for idx, st in enumerate(span_tags):
            if not st.cell_path:
                span_tags[idx].cell_path = f"{col_names[0]}[0]"

        try:
            raw, capsule_ids = self._session.encapsulate(
                *Preparer.prepare(col_names, column_tags, skip_classify_on_column_names, raw, span_tags, extra),
                write_context,
                [],
                jextra,
                path,
                subdomains_from,
                create_subdomains)
        except Exception as e:
            str_e = str(e).lower()
            if (
                "write_context" in str_e
                or "writecontext" in str_e
                or ("failed to create capsule" in str_e and "404 not found" in str_e)
                or ("failed to create capsule" in str_e and "400 bad request" in str_e)
            ):
                raise errors.CapsuleSaveError(
                    f"failed to encapsulate data: check that write context {write_context} exists for domain",
                ) from None
            raise errors.CapsuleSaveError("encapsulating data") from e

        if raw is not None:
            raw = bytes(raw)
        return EncapsulateResponse(capsule_ids=capsule_ids, raw=raw, load_capsule_func=self.load_capsule)

    def refresh_token(self):
        return openapi_client.AuthenticationApi(self._get_client()).domain_authenticate(
            self._domain,
            domain_authenticate=openapi_client.DomainAuthenticate(token=self._api_key)).token

    def with_new_peer_domain(
        self,
        import_alias_for_child: str,
        display_name_for_child: str,
        nicknames: Optional[List[str]] = None,
        import_alias_for_parent: Optional[str] = None,
        display_name_for_parent: Optional[str] = None,
        link_all: bool = True,
        link_identity_providers: bool = None,
        link_facts: bool = None,
        link_read_contexts: bool = None,
        link_write_contexts: bool = None,
        link_capabilities: bool = None,
        link_domain_policy: bool = None,
        link_capsule_access_log: bool = None,
        link_control_log: bool = None,
        link_capsule_manifest: bool = None,
    ) -> "Session":
        """
        Creates a new peer domain, returning the authenticated session for that
        new domain.

        :param import_alias_for_child: The import alias for the child domain
        :param display_name_for_child: The display name for the child domain
        :param nicknames: The nicknames for the child domain
        :param import_alias_for_parent: The import alias for the parent domain
        :param display_name_for_parent: The display name for the parent domain
        :param link_all: Link all available resources
        :param link_identity_providers: Link identity providers
        :param link_facts: Link facts
        :param link_read_contexts: Link read contexts
        :param link_write_contexts: Link write contexts
        :param link_capabilities: Link capabilities
        :param link_domain_policy: Link domain policy
        :param link_capsule_access_log: Link capsule access log
        :param link_control_log: Link control log
        :param link_capsule_manifest: Link capsule manifest
        :return: The authenticated session for the new domain
        """
        dm = self.new_peer_domain(
            import_alias_for_child=import_alias_for_child,
            display_name_for_child=display_name_for_child,
            nicknames=nicknames,
            import_alias_for_parent=import_alias_for_parent,
            display_name_for_parent=display_name_for_parent,
            link_all=link_all,
            link_identity_providers=link_identity_providers,
            link_facts=link_facts,
            link_read_contexts=link_read_contexts,
            link_write_contexts=link_write_contexts,
            link_capabilities=link_capabilities,
            link_domain_policy=link_domain_policy,
            link_capsule_access_log=link_capsule_access_log,
            link_control_log=link_control_log,
            link_capsule_manifest=link_capsule_manifest,
        )
        return Session(dm.get("id"), dm.get("api_key"))

    @exec_with_token
    def get_admin_url(
        self,
        company_name: str,
        peer_domain_id: Optional[str] = None,
        nickname: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> Optional[str]:
        """
        Generate the admin URL for the domain. By default, this is the domain
        for this session. If one of the peer_domain_id, nickname, or alias are
        provided, the admin URL will be generated for the subdomain that
        matches.

        :param company_name: The name of the company to display
        :param peer_domain_id: The domain ID of the peer
        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        :return: The admin URL
        """
        if not peer_domain_id and (nickname or alias):
            peer_domain_id = self.get_peer(nickname=nickname, alias=alias)

        api_client = self._get_client()
        auth_api = openapi_client.AuthenticationApi(api_client=api_client)

        _id = self.domain_id
        tkn = api_client.configuration.access_token
        if peer_domain_id:
            _id = peer_domain_id
            tkn = auth_api.domain_authenticate(
                domain_id=peer_domain_id,
                domain_authenticate=openapi_client.DomainAuthenticate(token=tkn),
                token_exchange=True,
            ).token

        url = urlparse(api_client.configuration.host)
        url = f"{url.scheme}://{url.netloc}".replace('api', 'app')
        company_name = quote_plus(company_name)
        tkn = quote_plus(tkn)
        return f"{url}/settings/{_id}/byok?vendor={company_name}&token=${tkn}"
