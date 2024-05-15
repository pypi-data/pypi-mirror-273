import os
import time
import mlflow
import shutil
import plotly.graph_objects as go
from typing import Union, Dict, List, Tuple
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from determined import TrialInfo


def check_not_empty(data):
    assert data is not None
    assert data != ""


class MlflowHelper:
    def __init__(self, cfg, train=False, trailinfo: TrialInfo = None):
        super().__init__()
        tags = {"phase": "train" if train else "test"}
        if trailinfo is not None:
            tags["det_exp_id"] = str(trailinfo.experiment_id)
            tags["det_trail_id"] = str(trailinfo.trial_id)
            tags["platform"] = "determined"
        else:
            tags["platform"] = "local"

        self.exp_name, self.run_name = self.parse_exp_info(cfg.det_cfg)
        self.exp_id, self.run_id = self.create_run(self.exp_name, self.run_name, tags)
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.artifacts_path = f"./output/mlflow/{timestamp}_{self.run_name}"
        os.makedirs(self.artifacts_path)
        self.log_cfg(cfg)

    @staticmethod
    def create_run(exp_name, run_name, tags):
        exp = mlflow.get_experiment_by_name(exp_name)
        if exp is None:
            exp_id = mlflow.create_experiment(name=exp_name)
        else:
            exp_id = exp.experiment_id
        with mlflow.start_run(
            experiment_id=exp_id, run_name=run_name, tags=tags
        ) as run:
            run_id = run.info.run_id
        return exp_id, run_id

    @staticmethod
    def parse_exp_info(det_cfg: DictConfig):
        """
        det_cfg: config info from determined
        """
        check_not_empty(det_cfg.workspace)
        check_not_empty(det_cfg.project)
        check_not_empty(det_cfg.name)
        exp_name = f"{det_cfg.workspace}_{det_cfg.project}"
        run_name = det_cfg.name
        return exp_name, run_name

    def log_cfg(self, cfg: Union[Dict, DictConfig]):
        if isinstance(cfg, DictConfig):
            cfg = OmegaConf.to_object(cfg)
        artifact_file = "config.yaml"
        with mlflow.start_run(self.run_id):
            mlflow.log_dict(cfg, artifact_file=artifact_file)

    def log_metrics(self, metrics: dict, step=None):
        with mlflow.start_run(self.run_id):
            mlflow.log_metrics(metrics, step=step)

    def log_files(self, file_pathes: List):
        with mlflow.start_run(self.run_id):
            for fp in file_pathes:
                mlflow.log_artifact(fp)

    def store_artifact(self, file_path):
        shutil.copy(file_path, self.artifacts_path)

    def log_artifacts(self, local_dir=None):
        upload_path = local_dir if local_dir is not None else self.artifacts_path
        with mlflow.start_run(self.run_id):
            mlflow.log_artifacts(upload_path)

    def log_table(self, *args, **kwargs):
        with mlflow.start_run(self.run_id):
            mlflow.log_table(*args, **kwargs)

    def log_figure(self, *args, **kwargs):
        with mlflow.start_run(self.run_id):
            mlflow.log_figure(*args, **kwargs)

    def log_simple_fiegure(
        self,
        data: List[Tuple[List, List, str]],
        file_name: str,
        xlable: str,
        ylabel: str,
        legend_title: str,
    ):
        fig = go.Figure()
        for subdata in data:
            fig = fig.add_trace(go.Scatter(x=subdata[0], y=subdata[1], name=subdata[2]))
        fig.update_layout(
            xaxis_title=xlable, yaxis_title=ylabel, legend_title=legend_title
        )
        self.log_figure(fig, file_name)
