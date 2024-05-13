import os
import subprocess
import tempfile
import time
import traceback

from komo.api_client import APIClient


class Logger:
    _TIME_BETWEEN_LOGS = 1

    def __init__(
        self,
        api_client: APIClient,
        task_id: str,
        task_type: str,
    ):
        self.api_client = api_client
        self.task_id = task_id
        self.task_type = task_type
        self.buffer = []
        self.last_log_time = None

    def flush(self):
        if len(self.buffer) == 0:
            return

        try:
            self.api_client.post_logs(
                self.task_id,
                self.task_type,
                self.buffer,
            )
        except Exception as e:
            print(e)
            traceback.print_exc()

        self.buffer = []
        self.last_log_time = time.time()

    def flush_if_necessary(self):
        curr_time = time.time()

        if (
            not self.last_log_time
            or (curr_time - self.last_log_time) > self._TIME_BETWEEN_LOGS
        ):
            self.flush()

    def log(self, message: str):
        self.flush_if_necessary()

        self.buffer.append(
            {
                "timestamp": int(time.time() * 1000),
                "message": message,
            }
        )

    def __del__(self):
        self.flush()


def _get_node_index():
    node_index = os.environ.get("SKYPILOT_NODE_RANK", 0)
    return node_index


def _execute(
    api_client: APIClient,
    task_id: str,
    task_type: str,
    script: str,
):
    logger = Logger(api_client, task_id, task_type)

    with tempfile.TemporaryDirectory() as td:
        script_file = os.path.join(td, "script.sh")

        with open(script_file, "w") as f:
            f.write(script)

        proc = subprocess.Popen(
            ["bash", "-l", script_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in proc.stdout:
            logger.log(line.decode("utf-8"))


def setup(job_id: str, setup_script: str):
    api_client = APIClient()
    api_client.mark_job_as_running(job_id)
    node_index = _get_node_index()
    task_id = f"{job_id}/{node_index}"
    _execute(api_client, task_id, "jobs", setup_script)


def run(job_id: str, run_script: str):
    api_client = APIClient()
    try:
        api_client.mark_job_as_running(job_id)
        node_index = _get_node_index()
        task_id = f"{job_id}/{node_index}"
        _execute(api_client, task_id, "jobs", run_script)
    finally:
        api_client.finish_job(job_id)


def setup_machine(machine_id: str, setup_script: str):
    api_client = APIClient()
    api_client.mark_machine_as_initializing(machine_id)
    _execute(api_client, machine_id, "machines", setup_script)
    api_client.mark_machine_as_running(machine_id)


def setup_service_replica(service_id: str, replica_id: int, setup_script: str):
    api_client = APIClient()
    task_id = f"{service_id}/{replica_id}"
    _execute(api_client, task_id, "services", setup_script)


def run_service_replica(service_id: str, replica_id: int, run_script: str):
    api_client = APIClient()
    task_id = f"{service_id}/{replica_id}"
    _execute(api_client, task_id, "services", run_script)
