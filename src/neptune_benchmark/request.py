__all__ = ["fetch"]

import asyncio
from typing import List

import httpx

from src.neptune_benchmark.config import BenchmarkConfig
from src.neptune_benchmark.generate_run_data import generate_run_data_subset


def fetch(
    url: str,
    run_data: List[str],
    num_requests: int,
    config: BenchmarkConfig,
    subset_length: int = 200,
    chart_id: int = 0,
):
    async def fetch_data():
        async with httpx.AsyncClient(params=config.params, headers=config.headers) as client:
            reqs = [
                client.post(
                    url=url,
                    json=generate_run_data_subset(run_data, chart_id, subset_length),
                    timeout=100000,
                )
                for _ in range(num_requests)
            ]
            results = await asyncio.gather(*reqs)

        return results

    return asyncio.run(fetch_data())
