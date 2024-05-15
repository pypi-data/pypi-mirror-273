import requests
from typing import List
from ._train import TrainingType
from ._exceptions import ArmisticeAIError


class Administrator:
    def __init__(
        self,
        access_code: str,
        server_url="https://test.armistice.ai",
    ):
        self.access_code = access_code
        self.server_url = server_url

    def create_project(self, task: str, project_name: str) -> str:
        url = f"{self.server_url}/projects"
        payload = {
            "task": task,
            "project_name": project_name,
            "access_code": self.access_code,
        }
        response = requests.post(url, json=payload)
        return response.json()["project_id"]

    def view_labels(self, project_id: str):
        url = f"{self.server_url}/projects/{project_id}/labels"
        response = requests.get(url)
        return response.json()

    def set_training_config(
        self,
        project_id: str,
        model: str,
        training_type: str,
        labels: List[str],
        rounds: int,
        num_clients: int,
        wandb: bool,
        rank=None,
    ):
        if rank is None and training_type != TrainingType.FULL:
            raise ArmisticeAIError(
                f"Rank must be specified when training_type is not FULL"
            )
        try:
            TrainingType[training_type.upper()]
        except KeyError:
            raise ArmisticeAIError("Invalid training type")
        url = f"{self.server_url}/projects/{project_id}/config"
        payload = {
            "model": model,
            "training_type": training_type,
            "labels": labels,
            "rounds": rounds,
            "num_clients": num_clients,
            "wandb": wandb,
        }
        if rank is not None:
            payload["rank"] = rank
        response = requests.post(url, json=payload)
        return response.json()

    def start_training(self, project_id: str):
        url = f"{self.server_url}/start_training"
        payload = {"project_id": project_id}
        response = requests.post(url, json=payload)
        return response.json()
