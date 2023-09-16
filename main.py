from loguru import logger

from src.neptune_benchmark.config import BenchmarkConfig
from src.neptune_benchmark.constants import (
    CHART_URL,
    NUM_REQUESTS,
    SUBSET_LENGTH,
)
from src.neptune_benchmark.generate import generate_run_data
from src.neptune_benchmark.request import fetch
from src.neptune_benchmark.stats import StatsCollector


def main():
    logger.info("Initializing configuration")
    config = BenchmarkConfig.from_env()

    logger.info("Initializing statistics collector")
    collector = StatsCollector()

    logger.info("Generating run data")
    all_run_data = generate_run_data(config.project, config.token)

    assert len(all_run_data) == 5000

    logger.info("Fetching chart data")
    responses = fetch(CHART_URL, all_run_data, NUM_REQUESTS, config, collector, SUBSET_LENGTH)

    execution_times = [r.elapsed.total_seconds() for r in responses]
    collector.record_response_time_series(execution_times)

    collector.to_json_file()


if __name__ == "__main__":
    main()
