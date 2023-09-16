from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Optional


@dataclass
class CLIArgs:
    project: Optional[str]
    api_token: Optional[str]


def parse_args() -> CLIArgs:
    parser = ArgumentParser()
    parser.add_argument("-p", "--project", type=Optional[str])
    parser.add_argument("-a", "--api-token", type=Optional[str])

    args = parser.parse_args()

    return CLIArgs(project=args.project, api_token=args.api_token)
