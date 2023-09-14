from typing import List, Dict

from random import sample

import neptune


def generate_run_data(project: str, api_token: str) -> List[str]:
    with neptune.init_project(project, api_token=api_token) as neptune_project:
        ids = list(map(lambda x: x._id, neptune_project.fetch_runs_table().to_rows()))
    return ids


def generate_run_data_subset(run_data: List[str], length: int = 10) -> List[Dict[str, str]]:
    ids = sample(run_data, length)
    return [
        {"attributePath": "charts/chart", "holderIdentifier": run_id, "holderType": "experiment"} for run_id in ids
    ]
