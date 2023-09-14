import os

import httpx
from dotenv import load_dotenv

from src.neptune_benchmark.generate_runs import generate_runs
from src.neptune_benchmark.generate_run_data import generate_run_data, generate_run_data_subset
from src.neptune_benchmark.auth import get_auth_tokens
from src.neptune_benchmark.request import fetch_chart_data


def main():
    load_dotenv()
    token = os.getenv("NEPTUNE_BENCHMARK_API_TOKEN")
    project = os.getenv("NEPTUNE_BENCHMARK_PROJECT")

    # generate_runs(10, project, token)

    auth_tokens = get_auth_tokens(token)
    access_token = auth_tokens.accessToken
    # refresh_token = auth_tokens.refreshToken

    all_run_data = generate_run_data(project, token)
    subset = generate_run_data_subset(all_run_data, length=5)

    response = fetch_chart_data(subset, project, access_token)

    print(len(response.json()["elements"]))


if __name__ == "__main__":
    main()
