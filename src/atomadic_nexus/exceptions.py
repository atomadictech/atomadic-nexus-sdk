"""Atomadic Nexus SDK exceptions."""
from __future__ import annotations


class NexusError(Exception):
    """Base for any Nexus-side error from the hosted engine."""


class PaymentRequired(NexusError):
    """HTTP 402 — fund the wallet (x402) or add a credit pack (Stripe)
    and retry. ``error.payment_url`` carries a 1-click top-up link."""

    def __init__(self, message: str, payment_url: str | None = None,
                 amount_usdc: str | None = None):
        super().__init__(message)
        self.payment_url = payment_url
        self.amount_usdc = amount_usdc


class RejectVerdict(NexusError):
    """Trust gate returned a REJECT verdict. Inspect ``error.evidence``
    for the failing probe(s); fix the request and retry."""

    def __init__(self, message: str, evidence: dict | None = None,
                 verdict: str = "REJECT"):
        super().__init__(message)
        self.evidence = evidence or {}
        self.verdict = verdict
