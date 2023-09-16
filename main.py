import sys

from dotenv import load_dotenv
from loguru import logger

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.generate import generate_run_ids
from neptune_benchmark.request import fetch
from neptune_benchmark.settings import (
    CHART_URL,
    LOAD_CONFIG_FROM_ENV,
    LOGGING_LEVEL,
    NUM_REQUESTS,
    SUBSET_LENGTH,
)
from neptune_benchmark.stats import StatsCollector


def main():
    logger.remove()
    logger.add(sys.stdout, level=LOGGING_LEVEL)
    # ==================================================================================================================
    # Configuration
    # ==================================================================================================================
    logger.info("Initializing configuration")
    if LOAD_CONFIG_FROM_ENV:
        logger.info("Loading configuration info from environment")
        load_dotenv()
        config = BenchmarkConfig.from_env()
    else:
        logger.info("Loading configuration info from CLI")
        config = BenchmarkConfig.from_cli()

    # ==================================================================================================================
    # Statistic Collector
    # ==================================================================================================================
    logger.info("Initializing statistics collector")
    collector = StatsCollector()

    # ==================================================================================================================
    # Generate a list of existing run ids
    # ==================================================================================================================
    logger.info("Generating run data")
    all_run_ids = generate_run_ids(config.project, config.token)

    # ==================================================================================================================
    # Fetch chart data
    # ==================================================================================================================
    logger.info("Fetching chart data")
    responses = fetch(CHART_URL, all_run_ids, NUM_REQUESTS, config, collector, SUBSET_LENGTH)

    # ==================================================================================================================
    # Collect results
    # ==================================================================================================================
    execution_times = [r.elapsed.total_seconds() for r in responses]
    logger.info("Recording response times")
    collector.record_response_time_series(execution_times)

    # ==================================================================================================================
    # Save results
    # ==================================================================================================================
    logger.info("Saving results")
    collector.to_json_file()


if __name__ == "__main__":
    main()
