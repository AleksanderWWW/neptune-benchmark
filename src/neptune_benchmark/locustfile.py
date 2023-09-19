from dotenv import load_dotenv
from locust import (
    FastHttpUser,
    between,
    events,
    task,
)

from neptune_benchmark.config import BenchmarkConfig
from neptune_benchmark.generate import (
    generate_run_data_subset,
    generate_run_ids,
)
from neptune_benchmark.settings import (
    CHART_ENDPOINT,
    HOST,
    SUBSET_LENGTH,
)

stat_file = open("stats.csv", "w")


@events.request_success.add_listener
def hook_request_success(request_type, name, response_time, response_length, **kw):
    stat_file.write(request_type + ";" + name + ";" + str(response_time) + ";" + str(response_length) + "\n")


@events.quitting.add_listener
def hook_quitting(environment, **kw):
    stat_file.close()


class NeptuneUser(FastHttpUser):
    wait_time = between(1, 1)
    host = HOST

    @task
    def hello_world(self):
        self.client.post(
            CHART_ENDPOINT,
            params=self.config.params,
            headers=self.config.headers,
            json=generate_run_data_subset(self.all_run_ids, 0, SUBSET_LENGTH),
        )

    def on_start(self):
        load_dotenv()
        self.config = BenchmarkConfig.from_env()
        self.all_run_ids = generate_run_ids(self.config.project, self.config.token)
