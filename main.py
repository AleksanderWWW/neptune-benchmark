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


async def main():
    execution_times = []
    load_dotenv()
    token = os.getenv("NEPTUNE_BENCHMARK_API_TOKEN")
    project = os.getenv("NEPTUNE_BENCHMARK_PROJECT")

    # generate_runs(10, project, token)

    auth_tokens = get_auth_tokens(token)
    access_token = auth_tokens.accessToken
    # refresh_token = auth_tokens.refreshToken

    all_run_data = generate_run_data(project, token)

    client = httpx.AsyncClient(
        params={
            'projectIdentifier': project,
        },
        headers={
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
        })

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
