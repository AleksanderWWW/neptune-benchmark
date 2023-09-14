from typing import List, Dict

import httpx


def fetch_chart_data(run_data: List[Dict[str, str]], client: httpx.AsyncClient):
    return client.post(
        'https://testing.stage.neptune.ai/api/leaderboard/v1/channels/view',
        json=run_data,
    )
