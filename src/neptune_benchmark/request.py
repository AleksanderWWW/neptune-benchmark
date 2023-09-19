__all__ = ["fetch_all"]

import asyncio
import time
from datetime import timedelta
from typing import List

import httpx
import requests
from loguru import logger
from tqdm import tqdm

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.generate import generate_run_data_subset
from neptune_benchmark.settings import DEFAULT_TIMEOUT
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

            async def handle_error(error: Exception):
                logger.error(f"Error: {error}")
                collector.record_error(error)
                empty_resp = requests.Response
                empty_resp.elapsed = timedelta(microseconds=0)
                pbar.update(1)
                return empty_resp

            async def single_fetch():
                data = generate_run_data_subset(run_ids, chart_id, subset_length)
                try:
                    start = time.perf_counter()
                    resp = await client.post(
                        url=url,
                        json=data,
                    )
                    collector.record_response_time(time.perf_counter() - start)
                    pbar.update(1)
                    logger.debug(f"Success :: status code: {resp.status_code}")
                    return resp
                except (httpx.RemoteProtocolError, httpx.ReadError) as exc:
                    return await handle_error(exc)

            limits = httpx.Limits(max_keepalive_connections=300, max_connections=300)
            async with httpx.AsyncClient(
                params=config.params,
                headers=config.headers,
                timeout=DEFAULT_TIMEOUT,
                limits=limits,
            ) as client:
                reqs = [single_fetch() for _ in range(num_requests)]
                results = await asyncio.gather(*reqs)

            return results

    asyncio.run(fetch_data())


def fetch_all(
    url: str,
    run_ids: List[str],
    num_clients: int,
    num_requests_per_client: int,
    config: BenchmarkConfig,
    collector: StatsCollector,
    subset_length: int = 200,
    chart_id: int = 0,
):
    for i in range(num_requests_per_client):
        logger.info(f"Fetching data for request series no {i+1}/{num_requests_per_client}")
        fetch(url, run_ids, num_clients, config, collector, subset_length, chart_id)
        logger.info(f"Fetched data for request series no {i+1}/{num_requests_per_client}")
