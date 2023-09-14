import random

import neptune


def add_charts_small(run, lr):
    namespace = "charts/chart"
    num_steps = 1000
    if lr == 0.0005:
        decay = 0.9995
    elif lr == 0.0004:
        decay = 0.9996
    elif lr == 0.0003:
        decay = 0.9997
    elif lr == 0.0002:
        decay = 0.9998
    elif lr == 0.0001:
        decay = 0.9999
    else:
        decay = 0.99995

    decay_flip = 0.999995
    init_metric = 0.98
    floor = 0.2 + (random.random() - 0.5) * 0.15
    ceiling = floor + random.random() * 0.2
    flip = 100000  # num_steps*0.5 - random.random()*num_steps*0.2
    anomaly_step = int(random.uniform(0.3, 0.6) * num_steps)
    fluctuation = init_metric - floor

    for i in range(num_steps):
        if (i + 1) % anomaly_step == 0:
            run[namespace].append(init_metric + random.random() * 0.5)
        else:
            run[namespace].append(init_metric)

        init_metric = init_metric - (init_metric - floor) * (1 - decay) + (random.random() - 0.5) * 0.005 * (
            fluctuation) * 3

        if init_metric > 1:
            init_metric = 0.99
        elif init_metric < 0.001:
            init_metric = 0.005


def generate_runs(num_runs: int, project: str, api_token: str) -> None:

    lrs = [0.0005, 0.0004, 0.0003, 0.0002, 0.0001, 0.0000]

    for i in range(num_runs):
        lr = random.choice(lrs)
        run = neptune.init_run(project=project, api_token=api_token)
        run["training/hyper_parameters/lr"] = lr
        add_charts_small(run, lr)
        run.stop()
