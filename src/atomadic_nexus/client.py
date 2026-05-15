"""Atomadic Nexus SDK — typed HTTP client for the hosted trust layer.

The hosted endpoint is ``https://nexus.atomadic.tech/v1``. Calls
authenticate via API key (Pro/Team subscription) OR x402 USDC
micropayments (autonomous agent) via the ``X-Payment-Proof`` header.

Trust formulas are anchored to externally-verified lattice constants
(TAU_TRUST = 1820/1823, σ₀ = 1/√196560, ε_KL = 1/196884, RG_LOOP=47,
D_MAX=23). The derivation lives in the private MHED-TOE codex; this
SDK only carries the scalar values for caller-side reasoning.
"""
from __future__ import annotations

import os
from typing import Any

import httpx

from .exceptions import NexusError, PaymentRequired, RejectVerdict


_DEFAULT_ENDPOINT = "https://nexus.atomadic.tech/v1"
_DEFAULT_TIMEOUT_S = 30.0  # sub-200ms gates ideal; 30s ceiling for safety

CODEX_ANCHORS: dict[str, float | int] = {
    "TAU_TRUST":  1820 / 1823,
    "sigma_0":    1.0 / (196560 ** 0.5),
    "epsilon_KL": 1.0 / 196884,
    "RG_LOOP":    47,
    "D_MAX":      23,
}


class NexusClient:
    """Synchronous client for the hosted Atomadic Nexus trust layer."""

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT_S,
    ):
        self.api_key = (
            api_key
            or os.environ.get("ATOMADIC_NEXUS_API_KEY")
            or os.environ.get("ATOMADIC_API_KEY")
        )
        self.endpoint = endpoint or _DEFAULT_ENDPOINT
        self.timeout = timeout

    # ── TRUST family ─────────────────────────────────────────────────

    def trust_gate(self, body_text: str, name: str = "") -> dict[str, Any]:
        """Classify and score a request before forwarding. Returns
        ``{verdict, confidence, evidence}`` where verdict is one of
        PASS / REFINE / QUARANTINE / REJECT."""
        out = self._post("trust-gate", {"body_text": body_text, "name": name})
        if out.get("verdict") == "REJECT":
            raise RejectVerdict(
                message=out.get("reason", "trust gate REJECT"),
                evidence=out.get("evidence", {}),
            )
        return out

    def trust_score(self, agent_id: str) -> dict[str, Any]:
        return self._post("trust-score", {"agent_id": agent_id})

    def drift_check(self, sample: dict[str, Any]) -> dict[str, Any]:
        return self._post("drift-check", {"sample": sample})

    def hallucination_oracle(self, generation: str, grounding: str | None = None) -> dict[str, Any]:
        return self._post("hallucination-oracle", {
            "generation": generation, "grounding": grounding,
        })

    def prompt_inject_scan(self, prompt: str) -> dict[str, Any]:
        return self._post("prompt-inject-scan", {"prompt": prompt})

    # ── PAYMENT family ──────────────────────────────────────────────

    def x402_verify(self, header: str) -> dict[str, Any]:
        return self._post("x402-verify", {"x_payment_proof": header})

    def stripe_link(self, tier: str = "starter") -> dict[str, Any]:
        return self._post("stripe-link", {"tier": tier})

    def pricing_lookup(self, product: str = "atomadic-nexus") -> dict[str, Any]:
        return self._post("pricing-lookup", {"product": product})

    # ── LINEAGE family ──────────────────────────────────────────────

    def attest_lineage(self, artifact_sha: str, parents: list[str] | None = None) -> dict[str, Any]:
        return self._post("attest-lineage", {
            "artifact_sha": artifact_sha,
            "parents":      parents or [],
        })

    def recall_lineage(self, artifact_sha: str) -> dict[str, Any]:
        return self._post("recall-lineage", {"artifact_sha": artifact_sha})

    def semantic_diff(self, a: str, b: str) -> dict[str, Any]:
        return self._post("semantic-diff", {"a": a, "b": b})

    def contradiction_detect(self, a: str, b: str) -> dict[str, Any]:
        return self._post("contradiction-detect", {"a": a, "b": b})

    # ── COORDINATION family ────────────────────────────────────────

    def agent_plan(self, goal: str) -> dict[str, Any]:
        return self._post("agent-plan", {"goal": goal})

    def agent_topology(self) -> dict[str, Any]:
        return self._post("agent-topology", {})

    def routing_recommend(self, request: dict[str, Any]) -> dict[str, Any]:
        return self._post("routing-recommend", {"request": request})

    def consensus_create(self, peers: list[str], threshold: float = 0.66) -> dict[str, Any]:
        return self._post("consensus-create", {"peers": peers, "threshold": threshold})

    def delegation_depth(self) -> dict[str, Any]:
        return self._post("delegation-depth", {})

    # ── EVOLUTION family ────────────────────────────────────────────

    def agent_reputation(self, agent_id: str) -> dict[str, Any]:
        return self._post("agent-reputation", {"agent_id": agent_id})

    def lora_capture_fix(self, before: str, after: str, label: str) -> dict[str, Any]:
        return self._post("lora-capture-fix", {
            "before": before, "after": after, "label": label,
        })

    # ── MARQUEE family ──────────────────────────────────────────────

    def ratchet_gate(self, session_id: str) -> dict[str, Any]:
        return self._post("ratchet-gate", {"session_id": session_id})

    def verirand(self, n_bytes: int = 32) -> dict[str, Any]:
        return self._post("verirand", {"n_bytes": int(n_bytes)})

    def trust_phase_oracle(self, agent_id: str) -> dict[str, Any]:
        return self._post("trust-phase-oracle", {"agent_id": agent_id})

    def topological_identity(self, fingerprint: str) -> dict[str, Any]:
        return self._post("topological-identity", {"fingerprint": fingerprint})

    def nexus_shield(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post("nexus-shield", {"payload": payload})

    def veridelegate(self, ucan_chain: str) -> dict[str, Any]:
        return self._post("veridelegate", {"ucan_chain": ucan_chain})

    def sla_engine(self, contract: dict[str, Any]) -> dict[str, Any]:
        return self._post("sla-engine", {"contract": contract})

    def escrow_open(self, buyer: str, seller: str, amount_usdc: str) -> dict[str, Any]:
        return self._post("escrow-open", {
            "buyer": buyer, "seller": seller, "amount_usdc": amount_usdc,
        })

    def reputation_ledger(self, agent_id: str) -> dict[str, Any]:
        return self._post("reputation-ledger", {"agent_id": agent_id})

    # ── OWASP-2026 family ──────────────────────────────────────────

    def goal_alignment_check(self, intent: str, planned: list[str]) -> dict[str, Any]:
        return self._post("goal-alignment-check", {"intent": intent, "planned": planned})

    def tool_misuse_detect(self, tool: str, args: dict[str, Any]) -> dict[str, Any]:
        return self._post("tool-misuse-detect", {"tool": tool, "args": args})

    def emergent_behavior_probe(self, loop_trace: list[str]) -> dict[str, Any]:
        return self._post("emergent-behavior-probe", {"loop_trace": loop_trace})

    # ── HTTP plumbing ────────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json",
             "User-Agent":   "atomadic-nexus-sdk/0.1.0"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _post(self, verb: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.endpoint}/{verb}"
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(url, headers=self._headers(), json=payload)
        return self._handle(r)

    def _handle(self, r: httpx.Response) -> dict[str, Any]:
        if r.status_code == 200:
            return r.json()
        if r.status_code == 402:
            data = r.json() if r.content else {}
            raise PaymentRequired(
                message=data.get("error", "Payment required"),
                payment_url=data.get("payment_url"),
                amount_usdc=data.get("amount_usdc"),
            )
        raise NexusError(f"HTTP {r.status_code}: {r.text[:200]}")


def sign_x402(amount_usdc: str, chain: str = "base") -> dict[str, str]:
    """Stub helper that returns the canonical x402 header pair. The
    real EIP-712 signing happens against your wallet — supply your own
    signer in production. This stub is for protocol shape only."""
    return {
        "X-Payment-Proof":  f"<base64-eip712-stub: {amount_usdc} USDC on {chain}>",
        "X-Payment-Chain":  chain,
        "X-Payment-Amount": amount_usdc,
    }
