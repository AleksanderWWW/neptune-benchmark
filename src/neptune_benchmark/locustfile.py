import sys
from typing import List

from dotenv import load_dotenv
from locust import (
    FastHttpUser,
    between,
    task,
)
from loguru import logger

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.generate import (
    generate_run_data_subset,
    generate_run_ids,
)
from neptune_benchmark.settings import (
    CHART_ENDPOINT,
    HOST,
    LOGGING_LEVEL,
    SUBSET_LENGTH,
)


class NeptuneUser(FastHttpUser):
    wait_time = between(1, 1)
    host = HOST
    config: BenchmarkConfig
    all_run_ids: List[str]

    @task
    def test_chart_endpoint(self):
        self.client.post(
            CHART_ENDPOINT,
            params=self.config.params,
            headers=self.config.headers,
            json=generate_run_data_subset(self.all_run_ids, 0, SUBSET_LENGTH),
        )

    def on_start(self):
        logger.remove()
        logger.add(sys.stdout, level=LOGGING_LEVEL)

        load_dotenv()
        self.config = BenchmarkConfig.from_env()
        self.all_run_ids = generate_run_ids(self.config.project, self.config.token)
