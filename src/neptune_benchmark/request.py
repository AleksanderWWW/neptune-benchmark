from typing import List, Dict

import httpx


def fetch_chart_data(run_data: List[Dict[str, str]], project: str, access_token: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'authorization': f'Bearer {access_token}',
        'content-type': 'application/json',
        'Origin': 'https://testing.stage.neptune.ai',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'projectIdentifier': project,
    }

    return httpx.post(
        'https://testing.stage.neptune.ai/api/leaderboard/v1/channels/view',
        params=params,
        headers=headers,
        json=run_data,
    )
