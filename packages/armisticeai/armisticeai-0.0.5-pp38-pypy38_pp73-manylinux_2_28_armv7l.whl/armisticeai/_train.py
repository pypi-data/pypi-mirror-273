from enum import Enum
from transformers import (
    AutoImageProcessor,
    TrainingArguments,
    Trainer,
    DefaultDataCollator,
)
from peft import (
    LoraConfig,
    LoftQConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    get_peft_model_state_dict,
)
from transformers import AutoModelForImageClassification, BitsAndBytesConfig
from ._dataset import ArmisticeDataset
from typing import Dict
from ._utils import NDArrays, log
from collections import OrderedDict
import torch
import numpy as np
import evaluate
from logging import DEBUG


class TrainingType(Enum):
    FULL = 1
    LORA_FP16 = 2
    LORA_INT8 = 3
    QLORA_INT4 = 4


class TrainingConfig:
    def __init__(
        self,
        *,
        checkpoint: str,
        training_type: str,
        rank=None,
        dataset: ArmisticeDataset,
    ):
        self.checkpoint = checkpoint
        self.training_type = TrainingType[training_type.upper()]
        self.image_processor = AutoImageProcessor.from_pretrained(
            checkpoint, device_map="auto"
        )
        self.load_in_8bit = False
        self.load_in_4bit = False
        if self.training_type == TrainingType.LORA_INT8:
            self.load_in_8bit = True
        self.rank = rank
        self.dataset = dataset
        self._load_model()
        self.data_collator = DefaultDataCollator()
        self.accuracy = evaluate.load("accuracy")

    def _load_model(self):
        if self.load_in_8bit or self.load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_8bit=self.load_in_8bit, load_in_4bit=self.load_in_4bit
            )
        else:
            bnb_config = None

        self.model = AutoModelForImageClassification.from_pretrained(
            self.checkpoint,
            num_labels=len(self.dataset.labels),
            id2label=self.dataset.id2label,
            label2id=self.dataset.label2id,
            quantization_config=bnb_config,
            device_map="auto",
        )

        if (
            self.training_type == TrainingType.LORA_FP16
            or self.training_type == TrainingType.LORA_INT8
        ):
            lora_config = LoraConfig(
                r=self.rank,
                lora_alpha=2 * self.rank,
                target_modules=["query", "value"],
                lora_dropout=0.1,
                bias="none",
                modules_to_save=["classifier"],
            )
            if self.training_type == TrainingType.LORA_INT8:
                self.model = prepare_model_for_kbit_training(self.model)
            self.model = get_peft_model(self.model, lora_config)
        elif self.training_type == TrainingType.QLORA_INT4:
            loftq_config = LoftQConfig(loftq_bits=4)
            lora_config = LoraConfig(
                init_lora_weights="loftq",
                loftq_config=loftq_config,
                r=self.rank,
                lora_alpha=2 * self.rank,
                target_modules=["query", "value"],
                lora_dropout=0.1,
                bias="none",
                modules_to_save=["classifier"],
            )
            self.model = get_peft_model(self.model, lora_config)

    def get_parameters(self) -> NDArrays:
        if self.training_type == TrainingType.FULL:
            state_dict = self.model.state_dict()
        else:
            state_dict = get_peft_model_state_dict(self.model)
        return [val.cpu().numpy() for _, val in state_dict.items()]

    def set_parameters(self, parameters: NDArrays):
        state_dict = self.model.state_dict()
        if self.training_type != TrainingType.FULL:
            lora_keys = get_peft_model_state_dict(self.model).keys()
            lora_dict = OrderedDict(
                {k: torch.Tensor(v) for k, v in zip(lora_keys, parameters)}
            )
            full_dict = {}
            for k in state_dict:
                if k in lora_dict:
                    full_dict[k] = lora_dict[k]
                else:
                    full_dict[k] = state_dict[k]

            self.model.load_state_dict(full_dict)
        else:
            params_dict = zip(state_dict.keys(), parameters)
            ordered_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
            self.model.load_state_dict(ordered_dict)

    def set_batch_size(self):
        self.batch_size = 64

    def create_trainer(
        self, local_epochs: int, output_dir: str, eval=False, save_model=False
    ):
        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            return self.accuracy.compute(predictions=predictions, references=labels)

        lr = 5e-5
        fp16 = False

        if self.training_type != TrainingType.FULL:
            lr = 5e-4
            fp16 = True

        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            remove_unused_columns=False,
            num_train_epochs=local_epochs,
            evaluation_strategy="epoch",
            warmup_ratio=0.1,
            logging_steps=100,
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            learning_rate=lr,
            fp16=fp16,
            label_names=["labels"],
            report_to="none",
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=self.data_collator,
            train_dataset=self.trainset,
            eval_dataset=self.testset,
            tokenizer=self.image_processor,
            compute_metrics=compute_metrics,
        )

        if save_model:
            trainer.save_model(output_dir)

        return trainer

    def log_model_slice(self, msg: str):
        if self.training_type != TrainingType.FULL:
            log(DEBUG, f"{msg}: {self.get_parameters()[2][0][:10]}")
        else:
            log(DEBUG, f"{msg}: {self.get_parameters()[1][0][0][:10]}")
