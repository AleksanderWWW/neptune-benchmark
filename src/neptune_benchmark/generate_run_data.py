__all__ = [
    "generate_run_data",
    "generate_run_data_subset",
]

import pickle
from random import sample
from typing import (
    Dict,
    List,
)

import neptune

from src.neptune_benchmark.constants import RUN_DATA_PATH


def generate_run_data(project: str, api_token: str) -> List[str]:
    if RUN_DATA_PATH.exists():
        with open(RUN_DATA_PATH, "rb") as data_file:
            ids = pickle.load(data_file)
    else:
        RUN_DATA_PATH.parent.mkdir(exist_ok=True)
        with neptune.init_project(project, api_token=api_token) as neptune_project:
            ids = list(map(lambda x: x._id, neptune_project.fetch_runs_table().to_rows()))
        with open(RUN_DATA_PATH, "wb") as data_file:
            pickle.dump(ids, data_file)
    return ids


def generate_run_data_subset(run_data: List[str], chart_id: int, length: int = 10) -> List[Dict[str, str]]:
    ids = sample(run_data, length)
    return [
        {
            "attributePath": f"charts/chart-{chart_id}",
            "holderIdentifier": run_id,
            "holderType": "experiment",
        }
        for run_id in ids
    ]
