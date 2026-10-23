"""evalforge — eval runner for LLM applications."""

from importlib.metadata import version as _version

from .models  import EvalCase, EvalDataset, EvalResult, EvalReport
from .runner  import run_eval, compare
from .scorers import (
    Scorer, ExactMatchScorer, RegexScorer, RougeScorer,
    SemanticScorer, LLMJudgeScorer, CustomScorer, HostedScorer,
    QuotaExceededError,
)
from .datasets import load as load_dataset

__version__ = _version("ag-evalforge")

__all__ = [
    "EvalCase", "EvalDataset", "EvalResult", "EvalReport",
    "run_eval", "compare", "load_dataset",
    "Scorer", "ExactMatchScorer", "RegexScorer", "RougeScorer",
    "SemanticScorer", "LLMJudgeScorer", "CustomScorer", "HostedScorer",
    "QuotaExceededError",
]
