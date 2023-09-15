from src.neptune_benchmark.generate_run_data import generate_run_data
from src.neptune_benchmark.request import fetch
from src.neptune_benchmark.constants import SUBSET_LENGTH, NUM_REQUESTS, CHART_URL
from src.neptune_benchmark.utils import BenchmarkConfig


def main():
    config = BenchmarkConfig.from_env()

    all_run_data = generate_run_data(config.project, config.token)

    assert len(all_run_data) == 5000

    responses = fetch(CHART_URL, all_run_data, NUM_REQUESTS, config, SUBSET_LENGTH)

    execution_times = [r.elapsed.microseconds / 1e6 for r in responses]
    print(execution_times)


if __name__ == "__main__":
    main()
