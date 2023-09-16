__all__ = ["fetch"]

import asyncio
from datetime import timedelta
from typing import List

import httpx
import requests
from loguru import logger
from tqdm import tqdm

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.constants import DEFAULT_TIMEOUT
from neptune_benchmark.generate import generate_run_data_subset
from neptune_benchmark.stats import StatsCollector


def fetch(
    url: str,
    run_ids: List[str],
    num_requests: int,
    config: BenchmarkConfig,
    collector: StatsCollector,
    subset_length: int = 200,
    chart_id: int = 0,
):
    async def fetch_data():
        with tqdm(total=num_requests) as pbar:

            async def error_happened(error):
                logger.error(f"Error: {error}")
                collector.record_error()
                empty_resp = requests.Response
                empty_resp.elapsed = timedelta(microseconds=0)
                pbar.update(1)
                return empty_resp

            async def single_fetch():
                try:
                    await asyncio.sleep(1)
                    resp = await client.post(
                        url=url,
                        json=generate_run_data_subset(run_ids, chart_id, subset_length),
                    )
                    pbar.update(1)
                    logger.info(f"Success :: status code: {resp.status_code}")
                    return resp
                except (httpx.RemoteProtocolError, httpx.ReadError) as exc:
                    return await error_happened(exc)

            async with httpx.AsyncClient(
                params=config.params,
                headers=config.headers,
                timeout=DEFAULT_TIMEOUT,
            ) as client:
                reqs = [single_fetch() for _ in range(num_requests)]
                results = await asyncio.gather(*reqs)

            return results

    return asyncio.run(fetch_data())
