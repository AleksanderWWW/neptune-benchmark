from typing import Dict
from dataclasses import dataclass


@dataclass
class BenchmarkConfig:
    access_token: str
    project: str

    @property
    def headers(self) -> Dict[str, str]:
        return {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'authorization': f'Bearer {self.access_token}',
                'content-type': 'application/json',
                'Origin': 'https://testing.stage.neptune.ai',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            }

    @property
    def params(self) -> Dict[str, str]:
        return {
            'projectIdentifier': self.project,
        }
