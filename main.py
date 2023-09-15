from src.neptune_benchmark.config import BenchmarkConfig
from src.neptune_benchmark.constants import (
    CHART_URL,
    NUM_REQUESTS,
    SUBSET_LENGTH,
)
from src.neptune_benchmark.generate_run_data import generate_run_data
from src.neptune_benchmark.request import fetch


def main():
    config = BenchmarkConfig.from_env()

    all_run_data = generate_run_data(config.project, config.token)

    assert len(all_run_data) == 5000

    responses = fetch(CHART_URL, all_run_data, NUM_REQUESTS, config, SUBSET_LENGTH)

    execution_times = [r.elapsed.total_seconds() for r in responses]
    print(execution_times)


if __name__ == "__main__":
    main()
