__all__ = [
    "StatsCollector",
]

import json
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from pathlib import Path
from statistics import (
    mean,
    median,
)
from typing import (
    Any,
    Dict,
    Optional,
)

from loguru import logger

from neptune_benchmark.constants import (
    NUM_REQUESTS,
    SUBSET_LENGTH,
)


@dataclass
class StatsCollector:
    _resp_times: list[float] = field(default_factory=list)
    _error_count: int = 0
    _mean_resp_time: float = 0
    _median_resp_time: float = 0
    _processed: bool = False

    req_num: int = NUM_REQUESTS
    subset_len: int = SUBSET_LENGTH

    def reset(self) -> None:
        self._resp_times: list[float] = []
        self._error_count: int = 0
        self._mean_resp_time: float = 0
        self._median_resp_time = 0
        self._processed = False

    def record_error(self) -> None:
        self._error_count += 1

    def record_response_time(self, resp_time: float):
        if not isinstance(resp_time, float):
            raise ValueError(f"Value '{resp_time}' of type {type(resp_time)} is not a proper response time (float).")

        self._resp_times.append(resp_time)

    def record_response_time_series(self, series: list[float]) -> None:
        self._resp_times.extend(series)

    def summarize(self) -> Dict[str, Any]:
        if not self._processed:
            self._mean_resp_time = mean(self._resp_times)
            self._median_resp_time = median(self._resp_times)

        self._processed = True

        return {
            "requestsSentCount": self.req_num,
            "chartsPerRequestCount": self.subset_len,
            "responseTimeSeries": self._resp_times,
            "meanResponseTime": self._mean_resp_time,
            "medianResponseTime": self._median_resp_time,
            "errorCount": self._error_count,
            "successCount": self.req_num - self._error_count,
        }

    def to_json(self) -> str:
        return json.dumps(self.summarize(), indent=4)

    def to_json_file(self, file_path: Optional[str] = None) -> None:
        file_path = file_path or f"stats/stats-{datetime.now().strftime('%Y-%m-%d::%H:%M:%S')}.json"
        json_str = self.to_json()

        file_path = Path(file_path)

        if not file_path.parent.exists():
            logger.info(f"Creating '{str(file_path.parent)}' as it does not exist")
            file_path.parent.mkdir()

        logger.info(f"Writing stats to {str(file_path)}")
        file_path.write_text(json_str)
