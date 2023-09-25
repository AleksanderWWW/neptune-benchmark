__all__ = [
    "BenchmarkConfig",
]

import os
from dataclasses import dataclass
from typing import Dict

from neptune_benchmark.auth import get_auth_tokens


@dataclass
class BenchmarkConfig:
    token: str
    access_token: str
    refresh_token: str
    project: str

    @classmethod
    def from_env(cls) -> "BenchmarkConfig":
        token = os.getenv("NEPTUNE_BENCHMARK_API_TOKEN")
        project = os.getenv("NEPTUNE_BENCHMARK_PROJECT")

        auth_tokens = get_auth_tokens(token)
        access_token = auth_tokens.accessToken
        refresh_token = auth_tokens.refreshToken

        return cls(token, access_token, refresh_token, project)

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
            "Origin": "https://testing.stage.neptune.ai",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    @property
    def params(self) -> Dict[str, str]:
        return {
            "projectIdentifier": self.project,
        }
