from typing import Dict, Tuple, Callable, Any, List

from lightrag.optim.parameter import Parameter

from lightrag.optim.trainer.adal import AdalComponent
from lightrag.datasets.big_bench_hard import ObjectCountData
from lightrag.optim.text_grad.textual_grad_desc import TextualGradientDescent
from lightrag.core.generator import BackwardEngine
from lightrag.eval.answer_match_acc import AnswerMatchAcc
from lightrag.eval.base import EvaluationResult
from lightrag.optim.text_grad.text_loss_with_eval_fn import EvalFnToTextLoss


from use_cases.question_answering.bhh_object_count.task import ObjectCountTaskOriginal


class TGDWithEvalFnLoss(AdalComponent):
    def __init__(
        self,
        task_model_config: Dict,  # for task pipeline
        backward_engine_model_config: Dict,  # for computing gradients
        optimizer_model_config: Dict,  # for proposal
    ):
        super().__init__()

        self.task_model_config = task_model_config
        self.backward_engine_model_config = backward_engine_model_config
        self.optimizer_model_config = optimizer_model_config

        self.backward_engine = BackwardEngine(
            **backward_engine_model_config, use_cache=True
        )
        self.task = ObjectCountTaskOriginal(**task_model_config)
        self.evaluator = AnswerMatchAcc(type="exact_match")
        self.configure_backward_engine()

    def handle_one_train_sample(self, sample: ObjectCountData) -> Tuple[Callable, Dict]:
        return self.task.call, {"question": sample.x, "id": sample.id}

    def handle_one_loss_sample(
        self, sample: ObjectCountData, y_pred: Any
    ) -> Tuple[Callable, Dict]:
        return self.loss_fn, {
            "kwargs": {
                "y": y_pred,
                "y_gt": Parameter(
                    data=sample.y,
                    role_desc="The ground truth(reference correct answer)",
                    alias="y_gt",
                    requires_opt=False,
                ),
            }
        }

    def evaluate_one_sample(self, sample: ObjectCountData, y_pred: Any) -> Any:
        return self.evaluator.compute_single_item(y_pred, sample.y)

    # TODO: remove this, one should be enough
    def evaluate_samples(
        self, samples: List[ObjectCountData], y_preds: List
    ) -> EvaluationResult:
        r"""Support both batch and list of samples"""
        y_gts = [sample.y for sample in samples]
        return self.evaluator.compute(y_preds, y_gts)

    def train_step(self, batch, batch_idx, num_workers: int = 2) -> List:
        self.task.train()
        y_preds = super().pred_step(batch, batch_idx, num_workers)
        for i, y_pred in enumerate(y_preds):
            y_pred.alias += f"y_pred_{i}"
        return y_preds

    def configure_optimizers(self):
        return TextualGradientDescent(
            params=list(
                self.task.parameters()
            ),  # NOTE: for now it has to be a list not a generator
            **self.optimizer_model_config,
            num_gradient_memory=0,
        )

    def configure_backward_engine(self):
        self.backward_engine = BackwardEngine(**self.backward_engine_model_config)
        # add backward engine to the generator of the task
        self.task.llm_counter.set_backward_engine(self.backward_engine)

    def configure_loss_fn(self):
        # share the backward engine with the generator
        if self.backward_engine is None:
            self.configure_backwar_engine()
        self.loss_fn = EvalFnToTextLoss(
            eval_fn=self.evaluator.compute_single_item,
            eval_fn_desc="ObjectCountingEvalFn, Output accuracy score: 1 for correct, 0 for incorrect",
            backward_engine=self.backward_engine,
        )
