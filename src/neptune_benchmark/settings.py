__all__ = [
    "CHART_ENDPOINT",
    "HOST",
    "DEFAULT_TIMEOUT",
    "LOGGING_LEVEL",
    "NUM_CHARTS_PER_RUN",
    "RUN_DATA_PATH",
    "SUBSET_LENGTH",
]

from pathlib import Path

# How many series to include in one request
SUBSET_LENGTH = 200

# How many charts are present in each run
NUM_CHARTS_PER_RUN = 4

# URL to fetch chart series data from
HOST = "https://testing.stage.neptune.ai"
CHART_ENDPOINT = "/api/leaderboard/v1/channels/view"

# Where to save generated run ids
RUN_DATA_PATH = Path("data/run_data.pkl")

# Default timeout of the request
DEFAULT_TIMEOUT = 1000

# Logging level for `loguru`
LOGGING_LEVEL = "INFO"
