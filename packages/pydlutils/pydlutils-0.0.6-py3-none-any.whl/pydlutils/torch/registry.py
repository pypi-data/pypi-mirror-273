from torch import nn
from ..basic.registry import Registry

PYTORCH_REGISTRY = Registry("PYTORCH")

PYTORCH_REGISTRY.register(nn.LeakyReLU)
PYTORCH_REGISTRY.register(nn.ReLU6)
PYTORCH_REGISTRY.register(nn.SELU)
PYTORCH_REGISTRY.register(nn.ELU)
PYTORCH_REGISTRY.register(nn.GELU)
PYTORCH_REGISTRY.register(nn.SiLU)
PYTORCH_REGISTRY.register(nn.Hardswish)
