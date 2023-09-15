import asyncio
from typing import List

import httpx

from src.neptune_benchmark.generate_run_data import generate_run_data_subset
from src.neptune_benchmark.utils import BenchmarkConfig


# def fetch_chart_data(run_data: List[Dict[str, str]], config: BenchmarkConfig):
#     return grequests.post(
#         'https://testing.stage.neptune.ai/api/leaderboard/v1/channels/view',
#         json=run_data,
#         headers=config.headers,
#         params=config.params,
#     )


def fetch(url: str, run_data: List[str], num_requests: int, config: BenchmarkConfig, subset_length: int = 200,
          chart_id: int = 0):
    async def fetch_data():
        async with httpx.AsyncClient(params=config.params, headers=config.headers) as client:
            reqs = [
                client.post(
                    url=url,
                    json=generate_run_data_subset(run_data, chart_id, subset_length),
                    timeout=100000,
                ) for _ in range(num_requests)
            ]
            results = await asyncio.gather(*reqs)

        return results

    return asyncio.run(fetch_data())
