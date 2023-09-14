import asyncio
import os
import time

import httpx
from dotenv import load_dotenv

from src.neptune_benchmark.generate_runs import generate_runs
from src.neptune_benchmark.generate_run_data import generate_run_data, generate_run_data_subset
from src.neptune_benchmark.auth import get_auth_tokens
from src.neptune_benchmark.request import fetch_chart_data
from src.neptune_benchmark.constants import SUBSET_LENGTH
from src.neptune_benchmark.utils import BenchmarkConfig


async def main():
    execution_times = []
    load_dotenv()
    token = os.getenv("NEPTUNE_BENCHMARK_API_TOKEN")
    project = os.getenv("NEPTUNE_BENCHMARK_PROJECT")

    # generate_runs(10, project, token)

    auth_tokens = get_auth_tokens(token)
    access_token = auth_tokens.accessToken
    # refresh_token = auth_tokens.refreshToken

    config = BenchmarkConfig(access_token, project)

    all_run_data = generate_run_data(project, token)

    client = httpx.AsyncClient(
        params=config.params,
        headers=config.headers
    )

    async def single_task():
        subset = generate_run_data_subset(all_run_data, length=SUBSET_LENGTH)
        now = time.time()
        await fetch_chart_data(subset, client)
        execution_times.append(time.time() - now)

    tasks = [
        single_task() for _ in range(10)
    ]

    await asyncio.gather(*tasks)

    await client.aclose()
    print(execution_times)


if __name__ == "__main__":
    asyncio.run(main())
