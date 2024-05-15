import requests
from ._dataset import ArmisticeDataset
from ._train import TrainingConfig
from ._dap import DapConfig
from typing import Dict, Tuple
from flwr.common import Scalar
import flwr as fl
from ._utils import log, NDArrays
from logging import DEBUG, INFO


class Client(fl.client.NumPyClient):
    def __init__(
        self,
        *,
        project_id: str,
        dataset: str,
        output_dir: str,
        server_url="https://test.armistice.ai",
        federator_url="localhost:8081",
        insecure=None,
    ) -> None:
        self.project_id = project_id
        self.dataset = ArmisticeDataset(dataset)
        self.server_url = server_url
        self.id = self._join_project()
        self.output_dir = output_dir
        self.training_config = None
        self.dap_config = None
        self.federator_url = federator_url
        self.insecure = insecure

    def _join_project(self):
        url = f"{self.server_url}/clients"
        payload = {
            "project_id": self.project_id,
            "labels": self.dataset.labels,
        }
        response = requests.post(url, json=payload)
        return response.json()["client_id"]

    def get_training_config(self) -> TrainingConfig:
        if self.training_config is None:
            url = f"{self.server_url}/projects/{self.project_id}/config"
            response = requests.get(url)
            config = response.json()
            self.training_config = TrainingConfig(
                checkpoint=config["model"],
                training_type=config["training_type"],
                rank=config["rank"],
                dataset=self.dataset,
            )
        self.training_config.log_model_slice("Init model slice")
        return self.training_config

    def get_dap_config(self) -> DapConfig:
        if self.dap_config is None:
            url = f"{self.server_url}/projects/{self.project_id}/dap_config"
            response = requests.get(url)
            config = response.json()
            self.dap_config = DapConfig(
                vdaf_length=config["vdaf_length"],
            )
        return self.dap_config

    def get_parameters(self, config: Dict[str, Scalar]) -> NDArrays:
        return self.training_config.get_parameters()

    def set_parameters(self, parameters):
        return self.training_config.set_parameters(parameters)

    def fit(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> tuple[NDArrays, int, dict[str, Scalar]]:
        # Update model parameters
        self.set_parameters(parameters)

        # Create trainers
        output_dir = self.output_dir + "/fed_round_" + str(config["server_round"])
        local_epochs = config["local_epochs"]
        trainer = self.training_config.create_trainer(local_epochs, output_dir)

        # Train and evaluate locally
        train_results = trainer.train()
        eval_results = trainer.evaluate()

        # Local accuracy
        local_accuracy = eval_results["eval_accuracy"]
        metrics = {
            "train_loss": train_results.training_loss,
            "eval_loss": eval_results["eval_loss"],
            "accuracy": local_accuracy,
        }

        self.training_config.log_model_slice(
            "Local model after fit (training on local dataset before aggregating)"
        )
        log(INFO, f"Local model accuracy: {local_accuracy}")
        log(
            DEBUG,
            f"task_id for secure aggregation received inside fit: {config['task_id']}",
        )
        self.dap_config.upload_measurement(config["task_id"], self.get_parameters({}))
        return [], len(self.trainset), metrics

    def evaluate(
        self, parameters: NDArrays, config: Dict[str, Scalar]
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        self.set_parameters(parameters)

        self.training_config.log_model_slice(
            "Remote (aggregated) model received from server for evaluation on local data"
        )

        # Evaluate remote model
        save_model = False
        output_dir = self.output_dir
        if config["server_round"] == config["total_rounds"]:
            output_dir = self.output_dir + "/final"
            save_model = True
        trainer = self.training_config.create_trainer(
            local_epochs=1, output_dir=output_dir, eval=True, save_model=save_model
        )
        results = trainer.evaluate()

        # Metrics for remote model
        eval_loss = results["eval_loss"]
        eval_accuracy = results["eval_accuracy"]
        log(
            INFO,
            f"Remote (aggregated) model eval_loss: {eval_loss}, accuracy: {eval_accuracy}, computed on local validation dataset.",
        )

        return (
            eval_loss,
            len(self.testset),
            {"accuracy": eval_accuracy},
        )

    def train(self) -> None:
        fl.client.start_client(
            server_address=self.federator_url,
            client=self.to_client(),
            insecure=False,
            grpc_max_message_length=2147483647,  # 2GB
        )
