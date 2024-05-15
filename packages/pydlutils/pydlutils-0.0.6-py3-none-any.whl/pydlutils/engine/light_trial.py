import os
import time
import torch
import determined as det
import torch.nn as nn
from typing import Dict
from uranus_light.utils.mlflow_utils import MlflowHelper


class LightTrial:
    r"""
    Light trail implement the convenient interface:
        - parse config file
        - report metrics to determined
        - upload checkpoint to determined
    User need to inherit this class and implement the run interface.
    """

    def __init__(self, context: det.core.Context, **kwargs) -> None:
        self.kwargs = kwargs
        self.config = kwargs["full_cfg"]
        self.info = det.get_cluster_info()
        if self.info is not None:
            self.env = self.create_env_context(self.info)
            self.prof = det.profiler.ProfilerAgent.from_env(
                self.env,
                global_rank=context.distributed.rank,
                local_rank=context.distributed.local_rank,
            )
            self.exp_id = self.info.trial.experiment_id
            trailinfo = self.info.trial
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            self.exp_id = f"{timestamp}_{self.config.det_cfg.name}"
            trailinfo = None
        self.context = context
        self.mlflow_helper = MlflowHelper(self.config, train=True, trailinfo=trailinfo)
        self.model_cfg = self.init_config(self.config, "model_cfg")
        self.loss_cfg = self.init_config(self.config, "loss")
        self.trainloader_cfg = self.init_config(self.config, "trainloader")
        self.testloader_cfg = self.init_config(self.config, "testloader")
        self.optimizer_cfg = self.init_config(self.config, "optimizer")
        self.scheduler_cfg = self.init_config(self.config, "scheduler")
        self.exp_cfg = self.init_config(self.config, "exp_cfg")
        if "output_dir" in self.exp_cfg:
            self.output_dir = f"{self.exp_cfg.output_dir}_{self.exp_id}"
            os.makedirs(self.output_dir, exist_ok=True)
        self.initialize()

    @staticmethod
    def create_env_context(info):
        return det.EnvContext(
            master_url=info.master_url,
            master_cert_file=info.master_cert_file,
            master_cert_name=info.master_cert_name,
            experiment_config=info.trial._config,
            hparams=info.trial.hparams,
            latest_checkpoint=info.latest_checkpoint,
            steps_completed=info.trial._steps_completed,
            use_gpu=bool(info.gpu_uuids),
            container_gpus=info.gpu_uuids,
            slot_ids=info.slot_ids,
            debug=info.trial._debug,
            det_trial_id=str(info.trial.trial_id),
            det_experiment_id=str(info.trial.experiment_id),
            det_agent_id=info.agent_id,
            det_cluster_id=info.cluster_id,
            trial_seed=info.trial.trial_seed,
            trial_run_id=info.trial._trial_run_id,
            allocation_id=info.allocation_id,
            managed_training=True,
            test_mode=False,
            on_cluster=True,
        )

    def _sync_device(self) -> None:
        torch.cuda.synchronize(self.context.device)

    def initialize(self):
        if torch.cuda.is_available() and self.info:
            self.prof._set_sync_device(self._sync_device)
            self.prof.set_training(True)

    def report_train_metrics(self, *args, **kwargs):
        if kwargs["steps_completed"] % self.exp_cfg.visual_steps != 0:
            return

        if self.context is None:
            return

        self.mlflow_helper.log_metrics(
            kwargs["metrics"], step=kwargs["steps_completed"]
        )
        self.context.train.report_training_metrics(*args, **kwargs)
        self.prof.update_batch_idx(kwargs["steps_completed"])

    def report_valid_metrics(self, *args, **kwargs):
        metrics = kwargs["metrics"]
        new_metrics = {}
        for key in metrics.keys():
            new_metrics[f"eval_{key}"] = metrics[key]
        self.mlflow_helper.log_metrics(new_metrics, step=kwargs["steps_completed"])
        if self.context is None:
            return
        self.context.train.report_validation_metrics(*args, **kwargs)

    def update_profiler(self, batch_idx: int):
        if self.context is None:
            return
        self.prof.update_batch_idx(batch_idx)

    def save_checkpoint(
        self, steps_completed: int, epochs_completed: int, model: nn.Module
    ):
        if self.context is None:
            return
        checkpoint_metadata_dict = {"steps_completed": steps_completed}

        # NEW: Here we are saving multiple files to our checkpoint
        # directory. 1) a model state file and 2) a file includes
        # information about the training loop state.
        with self.context.checkpoint.store_path(checkpoint_metadata_dict) as (
            path,
            storage_id,
        ):
            torch.save(model.state_dict(), path / "checkpoint.pt")
            with path.joinpath("state").open("w") as f:
                f.write(f"{epochs_completed},{self.info.trial.trial_id}")

    @staticmethod
    def init_config(config: Dict, key: str):
        if key in config:
            return config[key]
        else:
            return None

    def start(self):
        if self.config.remote:
            with self.prof:
                self.run()
        else:
            self.run()

    def run(self):
        raise NotImplementedError
