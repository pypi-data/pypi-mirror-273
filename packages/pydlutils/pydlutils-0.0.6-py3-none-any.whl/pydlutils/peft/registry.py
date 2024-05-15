from peft import LoraConfig
from ..basic.registry import Registry

PEFT_REGISTRY = Registry("PEFT")
PEFT_REGISTRY.register(LoraConfig)
