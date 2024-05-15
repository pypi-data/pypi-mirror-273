import determined as det
from omegaconf import dictconfig
from ..registry import build_trial


class LightDet:
    r"""
    Wrap the task in determined context
    """

    def __init__(self, config: dictconfig.DictConfig) -> None:
        self.config = config

    def run(self):
        with det.core.init() as core_context:
            trial = build_trial(core_context, self.config)
            trial.start()
