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
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
)

import numpy as np
from loguru import logger

from neptune_benchmark.settings import SUBSET_LENGTH


@dataclass
class StatsCollector:
    _resp_times: List[float] = field(default_factory=list)
    _errors: Set[str] = field(default_factory=set)
    _error_count: int = 0
    _percentiles: Dict[int, float] = field(default_factory=dict)
    _processed: bool = False

    subset_len: int = SUBSET_LENGTH

    def reset(self) -> None:
        self._resp_times: List[float] = []
        self._error_count: int = 0
        self._processed = False

    def record_error(self, error: Exception) -> None:
        self._error_count += 1
        self._errors.add(f"{error.__class__.__name__}: {str(error)}")

    def record_response_time(self, resp_time: float):
        if not isinstance(resp_time, float):
            raise ValueError(f"Value '{resp_time}' of type {type(resp_time)} is not a proper response time (float).")

        self._resp_times.append(resp_time)

    def record_response_time_series(self, series: List[float]) -> None:
        self._resp_times.extend(series)

    def summarize(self) -> Dict[str, Any]:
        if not self._processed:
            resp_times_array = np.array(self._resp_times)
            non_zero_resp_times = resp_times_array[resp_times_array > 0]

            if len(non_zero_resp_times) == 0:  # all requests failed
                pass  # do not calculate statistics
            else:

                for i in range(100):
                    self._percentiles[i] = np.percentile(non_zero_resp_times, i)

        self._processed = True

        errors = list(self._errors)

        return {
            "requestsSentCount": len(self._resp_times),
            "chartsPerRequestCount": self.subset_len,
            "responseTimeSeries": self._resp_times,
            "percentiles": self._percentiles,
            "errorCount": self._error_count,
            "errorCauses": errors,
            "successCount": len(self._resp_times) - self._error_count,
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

        logger.debug(f"Writing stats to {str(file_path)}")
        file_path.write_text(json_str)
