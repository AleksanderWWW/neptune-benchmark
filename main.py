import sys

from dotenv import load_dotenv
from loguru import logger

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.generate import generate_run_ids
from neptune_benchmark.request import fetch_all
from neptune_benchmark.settings import (
    CHART_URL,
    LOAD_CONFIG_FROM_ENV,
    LOGGING_LEVEL,
    NUM_CLIENTS,
    NUM_REQUESTS_PER_CLIENT,
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
    fetch_all(CHART_URL, all_run_ids, NUM_CLIENTS, NUM_REQUESTS_PER_CLIENT, config, collector, SUBSET_LENGTH)
    # ==================================================================================================================
    # Save results
    # ==================================================================================================================
    logger.info("Saving results")
    collector.to_json_file()


if __name__ == "__main__":
    main()
