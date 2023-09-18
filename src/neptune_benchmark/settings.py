__all__ = [
    "CHART_URL",
    "LOAD_CONFIG_FROM_ENV",
    "DEFAULT_TIMEOUT",
    "LOGGING_LEVEL",
    "NUM_CLIENTS",
    "NUM_REQUESTS_PER_CLIENT",
    "RUN_DATA_PATH",
    "SUBSET_LENGTH",
]

from pathlib import Path

# How many series to include in one request
SUBSET_LENGTH = 50

# How many async requests with series data to send
NUM_CLIENTS = 200

# How many requests will each client send
NUM_REQUESTS_PER_CLIENT = 2

# URL to fetch chart series data from
CHART_URL = "https://testing.stage.neptune.ai/api/leaderboard/v1/channels/view"

# Where to save generated run ids
RUN_DATA_PATH = Path("data/run_data.pkl")

# Default timeout of the request
DEFAULT_TIMEOUT = 1000

# Whether the configuration (project, api_token...) is to be loaded from env
LOAD_CONFIG_FROM_ENV = True

# Logging level for `loguru`
LOGGING_LEVEL = "INFO"
