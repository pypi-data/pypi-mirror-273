from transformers import (
    TrainingArguments,
    Seq2SeqTrainingArguments,
    GenerationConfig,
)

from ..basic.registry import Registry

TANSFORMERS_REGISTRY = Registry("TRANSFORMERS")

TANSFORMERS_REGISTRY.register(TrainingArguments)
TANSFORMERS_REGISTRY.register(Seq2SeqTrainingArguments)
TANSFORMERS_REGISTRY.register(GenerationConfig)
