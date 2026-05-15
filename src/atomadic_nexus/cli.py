"""Atomadic Nexus CLI entry point."""
from __future__ import annotations

import argparse
import json
import sys

from .client import NexusClient, sign_x402
from .exceptions import NexusError, PaymentRequired, RejectVerdict


VERB_FAMILIES = {
    "TRUST": ["trust-gate", "trust-score", "drift-check", "hallucination-oracle",
              "prompt-inject-scan", "security-prompt-scan"],
    "PAYMENT": ["x402-verify", "stripe-link", "pricing-lookup", "well-known-publish"],
    "LINEAGE": ["attest-lineage", "recall-lineage", "semantic-diff", "contradiction-detect"],
    "COORDINATION": ["agent-plan", "agent-topology", "routing-recommend",
                     "swarm-relay", "swarm-inbox", "consensus-create",
                     "consensus-vote", "consensus-result", "delegation-depth"],
    "EVOLUTION": ["agent-reputation", "lora-capture-fix", "lora-contribute"],
    "MARQUEE": ["ratchet-gate", "verirand", "trust-phase-oracle",
                "topological-identity", "nexus-shield", "veridelegate",
                "agent-discovery", "sla-engine", "escrow-open",
                "escrow-release", "escrow-dispute", "reputation-ledger"],
    "OWASP-2026": ["goal-alignment-check", "tool-misuse-detect",
                   "delegated-trust-validate", "persistent-memory-audit",
                   "emergent-behavior-probe", "tool-poisoning-scan",
                   "scope-validate", "oauth21-gate"],
    "MARKETPLACE": ["marketplace-list", "marketplace-search",
                    "marketplace-purchase", "marketplace-rate",
                    "marketplace-payout"],
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="nexus", description="Atomadic Nexus — Trust Layer for the Agent Economy.")
    p.add_argument("--api-key",  default=None)
    p.add_argument("--endpoint", default=None)
    sub = p.add_subparsers(dest="verb", required=True)

    sp = sub.add_parser("trust-gate", help="classify + score a request")
    sp.add_argument("body_text")
    sp.add_argument("--name", default="")

    sp = sub.add_parser("verirand", help="cryptographic verifiable randomness")
    sp.add_argument("--n-bytes", type=int, default=32)

    sp = sub.add_parser("x402-verify", help="verify a payment-proof header")
    sp.add_argument("header")

    sp = sub.add_parser("attest-lineage", help="attest provenance chain")
    sp.add_argument("artifact_sha")

    sp = sub.add_parser("agent-reputation", help="lookup per-agent reputation")
    sp.add_argument("agent_id")

    sub.add_parser("list", help="list every verb")
    sub.add_parser("families", help="list verb families")

    args = p.parse_args(argv)

    if args.verb == "list":
        for fam, verbs in VERB_FAMILIES.items():
            print(f"== {fam} ==")
            for v in verbs:
                print(f"  {v}")
        return 0
    if args.verb == "families":
        for fam in VERB_FAMILIES:
            print(fam)
        return 0

    client = NexusClient(api_key=args.api_key, endpoint=args.endpoint)
    try:
        if args.verb == "trust-gate":
            out = client.trust_gate(args.body_text, name=args.name)
        elif args.verb == "verirand":
            out = client.verirand(n_bytes=args.n_bytes)
        elif args.verb == "x402-verify":
            out = client.x402_verify(args.header)
        elif args.verb == "attest-lineage":
            out = client.attest_lineage(args.artifact_sha)
        elif args.verb == "agent-reputation":
            out = client.agent_reputation(args.agent_id)
        else:
            print(f"unknown verb: {args.verb}", file=sys.stderr)
            return 2
        print(json.dumps(out, indent=2, default=str))
        return 0
    except PaymentRequired as e:
        print(f"402 Payment Required: {e}", file=sys.stderr)
        if e.payment_url:
            print(f"Top up: {e.payment_url}", file=sys.stderr)
        return 1
    except RejectVerdict as e:
        print(f"REJECT: {e}", file=sys.stderr)
        print(f"Evidence: {json.dumps(e.evidence, indent=2)}", file=sys.stderr)
        return 1
    except NexusError as e:
        print(f"NexusError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
