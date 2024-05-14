from typing import Optional

from pydantic import BaseModel

from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.claude_3 import Claude3Evaluator
from agenteval.targets import BaseTarget
from agenteval.test import Test

_EVALUATOR_MAP = {
    "claude-3": Claude3Evaluator,
}


class EvaluatorFactory(BaseModel):
    config: dict

    def create(
        self, test: Test, target: BaseTarget, work_dir: Optional[str]
    ) -> BaseEvaluator:
        evaluator_cls = _EVALUATOR_MAP[self.config["model"]]
        return evaluator_cls(
            test=test,
            target=target,
            work_dir=work_dir,
            **{k: v for k, v in self.config.items() if k != "model"}
        )
