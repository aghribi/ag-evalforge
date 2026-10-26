"""Hosted scorer — delegates scoring to the hosted EvalForge API (no OpenAI key needed)."""
from __future__ import annotations
from typing import Optional
import httpx
from ..models import EvalCase, EvalResult
from .base import Scorer


class QuotaExceededError(Exception):
    """Raised when the hosted API returns HTTP 429 (monthly quota exceeded)."""

class HostedScorer(Scorer):
    """
    Score eval cases via the hosted API.

    Supports all hosted scorers: ``exact_match``, ``rouge_l``, ``regex``, ``llm_judge``.
    No OpenAI API key required — uses your hosted API key.

    Example::

        from ag_evalforge import run_eval, EvalCase, HostedScorer

        scorer = HostedScorer(api_key="ag_live_...", base_url="https://your-ag-platform",
                              scorer="llm_judge",
                              criteria="Is the answer accurate and professional?")
        report = run_eval(cases=[...], scorer=scorer)
    """

    name = "hosted"

    def __init__(
        self,
        api_key:   str,
        base_url:  str,
        scorer:    str = "llm_judge",
        threshold: float = 0.7,
        criteria:  Optional[str] = None,
        pattern:   Optional[str] = None,
        timeout:   float = 30.0,
    ):
        self.api_key   = api_key
        self.scorer    = scorer
        self.threshold = threshold
        self.criteria  = criteria
        self.pattern   = pattern
        self._base     = base_url.rstrip("/")
        self._timeout  = timeout

    def score_batch(self, cases: list[EvalCase], outputs: list[str]) -> list[EvalResult]:
        payload: dict = {
            "scorer": self.scorer,
            "threshold": self.threshold,
            "cases": [
                {"input": c.input, "output": o, "expected": c.expected}
                for c, o in zip(cases, outputs)
            ],
        }
        if self.criteria:
            payload["criteria"] = self.criteria
        if self.pattern:
            payload["pattern"] = self.pattern

        with httpx.Client(
            base_url=self._base,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self._timeout,
        ) as client:
            resp = client.post("/v1/eval/score", json=payload)
            if resp.status_code == 429:
                try:
                    detail = resp.json().get("detail", "Monthly quota exceeded.")
                except Exception:
                    detail = "Monthly quota exceeded."
                raise QuotaExceededError(detail)
            resp.raise_for_status()
            data = resp.json()

        results = []
        for item in data.get("results", []):
            results.append(EvalResult(
                case=EvalCase(input=item["input"], expected=item.get("expected")),
                output=item["output"],
                score=float(item["score"]),
                passed=bool(item["passed"]),
                reason=item.get("rationale"),
            ))
        return results

    def score(self, case: EvalCase, output: str) -> EvalResult:
        return self.score_batch([case], [output])[0]
