__all__ = [
    "get_auth_tokens",
]

import os
from typing import Optional

from neptune.internal.backends.hosted_client import (
    BACKEND_SWAGGER_PATH,
    _get_token_client,
    get_client_config,
)
from neptune.internal.backends.utils import build_operation_url
from neptune.internal.credentials import Credentials


def get_auth_tokens(api_token: Optional[str] = None):

    api_token = api_token if api_token else os.getenv("NEPTUNE_BENCHMARK_API_TOKEN")
    credentials = Credentials.from_token(api_token)
    client_config = get_client_config(credentials=credentials, ssl_verify=True, proxies={})

    config_api_url = credentials.api_url_opt or credentials.token_origin_address

    endpoint_url = None
    if config_api_url != client_config.api_url:
        endpoint_url = build_operation_url(client_config.api_url, BACKEND_SWAGGER_PATH)

    backend_client = _get_token_client(
        credentials=credentials,
        ssl_verify=True,
        proxies={},
        endpoint_url=endpoint_url,
    )

    auth_tokens = backend_client.api.exchangeApiToken(X_Neptune_Api_Token=api_token).response().result

    return auth_tokens
