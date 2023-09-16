__all__ = [
    "CHART_URL",
    "DEFAULT_TIMEOUT",
    "NUM_REQUESTS",
    "RUN_DATA_PATH",
    "SUBSET_LENGTH",
]

from pathlib import Path

SUBSET_LENGTH = 200
NUM_REQUESTS = 200
CHART_URL = "https://testing.stage.neptune.ai/api/leaderboard/v1/channels/view"
RUN_DATA_PATH = Path("data/run_data.pkl")
DEFAULT_TIMEOUT = 1000
