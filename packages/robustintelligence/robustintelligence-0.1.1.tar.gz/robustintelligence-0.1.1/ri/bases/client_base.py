from ri.apiclient import ApiClient, Configuration
from typing import Optional, Any

_DEFAULT_CHANNEL_TIMEOUT = 300.0


class BaseClient:
    """Base client class for creating API clients with comprehensive configuration options.

    Initializes an API client with settings for authentication, server configuration, SSL details,
    and operation-specific configurations.

    :param domain: The base URL of the API server.
    :type domain: str
    :param api_key: The API key used for authentication.
    Each entry in the dict specifies an API key.
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is the API key secret.
    :type api_key: str
    :param api_key_header_name: The header name for the API key.
    :type api_key_header_name: str
    :param channel_timeout: The timeout for network connections in seconds. Default is 300 seconds.
    :type channel_timeout: float
    :param username: Username for HTTP basic authentication.
    :type username: Optional[str]
    :param password: Password for HTTP basic authentication.
    :type password: Optional[str]
    :param access_token: Access token for bearer authentication.
    :type access_token: Optional[str]
    :param ssl_ca_cert: Path to a file of concatenated CA certificates in PEM format.
    :type ssl_ca_cert: Optional[str]
    :param api_key_prefix: Dict to store API prefix (e.g. Bearer).
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is an API key prefix when generating the auth data.
    :type api_key_prefix: Optional[Dict[str, str]]
    :param server_index: Index to servers configuration for selecting the base URL.
    :type server_index: Optional[int]
    :param server_variables: Variables to replace in the templated server URL.
    :type server_variables: Optional[Dict[str, str]]
    :param server_operation_index: Mapping from operation ID to an index to server configuration.
    :type server_operation_index: Optional[Dict[str, int]]
    :param server_operation_variables: Mapping from operation ID to variables for templated server URLs.
    :type server_operation_variables: Optional[Dict[str, Dict[str, str]]]

    Attributes:
        _api_client (ApiClient): The configured API client instance used to interact with the API.
    """
    def __init__(
        self,
        domain: str,
        api_key: str,
        api_key_header_name: str,
        api_key_prefix: Optional[dict[Any, Any]] = None,
        channel_timeout: float=_DEFAULT_CHANNEL_TIMEOUT,
        username=None,
        password=None,
        access_token=None,
        ssl_ca_cert=None,
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
    ):
        host = self._cleanup_domain(domain)
        config = Configuration(
            host=host,
            api_key={api_key_header_name: api_key},
            api_key_prefix=api_key_prefix,
            username=username,
            password=password,
            access_token=access_token,
            server_index=server_index,
            server_variables=server_variables,
            server_operation_index=server_operation_index,
            server_operation_variables=server_operation_variables,
            ssl_ca_cert=ssl_ca_cert,
        )
        self._api_client = ApiClient(configuration=config)
        self._api_client.rest_client.pool_manager.connection_pool_kw["timeout"] = (
            channel_timeout
        )

    @staticmethod
    def _cleanup_domain(domain: str):
        if domain.endswith("/"):
            domain = domain[:-1]
        if not domain.startswith("https://") and not domain.startswith("http://"):
            domain = "https://" + domain
        return domain
