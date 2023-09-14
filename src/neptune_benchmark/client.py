import os
from typing import Optional

from bravado.requests_client import RequestsClient
from neptune.common.oauth import NeptuneAuthenticator
from neptune.internal.backends.hosted_client import _get_token_client, get_client_config, BACKEND_SWAGGER_PATH, \
    create_http_client
from neptune.internal.backends.utils import build_operation_url
from neptune.internal.credentials import Credentials


def create_authenticator(api_token: Optional[str] = None) -> NeptuneAuthenticator:
    api_token = api_token if api_token else os.getenv("NEPTUNE_API_TOKEN")
    credentials = Credentials.from_token(api_token)
    client_config = get_client_config(credentials=credentials, ssl_verify=True, proxies={})

    config_api_url = credentials.api_url_opt or credentials.token_origin_address

    endpoint_url = None
    if config_api_url != client_config.api_url:
        endpoint_url = build_operation_url(client_config.api_url, BACKEND_SWAGGER_PATH)

    return NeptuneAuthenticator(
        credentials.api_token,
        _get_token_client(
            credentials=credentials,
            ssl_verify=True,
            proxies={},
            endpoint_url=endpoint_url,
        ),
    )


def create_client(authenticator: NeptuneAuthenticator) -> RequestsClient:
    http_client = create_http_client(ssl_verify=True, proxies={})
    http_client.authenticator = authenticator

    return http_client
