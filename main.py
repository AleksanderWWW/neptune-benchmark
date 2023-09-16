from dotenv import load_dotenv
from loguru import logger

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.constants import (
    CHART_URL,
    CONFIG_LOAD_STRATEGY,
    NUM_REQUESTS,
    SUBSET_LENGTH,
)
from neptune_benchmark.generate import generate_run_ids
from neptune_benchmark.request import fetch
from neptune_benchmark.stats import StatsCollector


def main():
    logger.info("Initializing configuration")
    if CONFIG_LOAD_STRATEGY == "env":
        logger.info("Loading configuration info from environment")
        load_dotenv()
        config = BenchmarkConfig.from_env()
    else:
        logger.info("Loading configuration info from CLI")
        config = BenchmarkConfig.from_cli()

    logger.info("Initializing statistics collector")
    collector = StatsCollector()

    logger.info("Generating run data")
    all_run_ids = generate_run_ids(config.project, config.token)

    assert len(all_run_ids) == 5000

    logger.info("Fetching chart data")
    responses = fetch(CHART_URL, all_run_ids, NUM_REQUESTS, config, collector, SUBSET_LENGTH)

    execution_times = [r.elapsed.total_seconds() for r in responses]
    logger.info("Recording response times")
    collector.record_response_time_series(execution_times)

    logger.info("Saving results")
    collector.to_json_file()


if __name__ == "__main__":
    main()
