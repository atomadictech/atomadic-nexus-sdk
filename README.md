# Atomadic Nexus SDK

> **The Trust Layer for the Agent Economy.** Verifiable trust gates, x402 micropayments, agent reputation, hallucination oracles, lineage attestation. Codex-anchored confidence. One SDK across 50+ endpoints.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/PyPI-atomadic--nexus--sdk-blue.svg)](https://pypi.org/project/atomadic-nexus-sdk/)
[![npm](https://img.shields.io/badge/npm-atomadic--nexus--sdk-red.svg)](https://www.npmjs.com/package/atomadic-nexus-sdk)
[![Status](https://img.shields.io/badge/status-public%20beta-orange.svg)](https://atomadic.tech)

## What it does

Atomadic Nexus is the trust + payments layer that agents call when they need to **verify** something: another agent's identity, a payment proof, a hallucination probe, a lineage chain, a sanctions check. Sub-200ms gates. Codex-anchored confidence.

Compared to legacy trust layers:

| | AnChain.AI x402 | **Atomadic Nexus** |
|---|---|---|
| Sanctions screening | ✅ | ✅ |
| Per-agent reputation | ❌ | ✅ (ERC-8004 compatible) |
| Hallucination oracle | ❌ | ✅ |
| Codex anchors (TAU_TRUST, σ₀, ε_KL) | ❌ | ✅ |
| OWASP-2026 Agentic Top 10 coverage | partial | full |
| Verb surface | ~10 endpoints | 50+ verbs across 5 families |

## Install

```bash
pip install atomadic-nexus-sdk
# or
npm install atomadic-nexus-sdk
```

## Quick start (Python)

```python
from atomadic_nexus import NexusClient

n = NexusClient(api_key="ATOMADIC_NEXUS_API_KEY")  # or use bundle key

# Trust gate — classify and score a request before forwarding it
verdict = n.trust_gate(body_text="…", name="…")
# {verdict: "PASS"|"REFINE"|"QUARANTINE"|"REJECT", confidence: 0.9984}

# x402 payment verification
ok = n.x402_verify(header="<base64-EIP712-payload>")

# Per-agent reputation
rep = n.agent_reputation(agent_id="0x…")

# Hallucination oracle
score = n.hallucination_oracle(generation="…", grounding="…")

# Lineage attestation
cert = n.attest_lineage(artifact_sha="…", parents=[…])
```

## Verb families (50+ endpoints)

```
TRUST            trust-gate, trust-score, drift-check, hallucination-oracle,
                 prompt-inject-scan, security-prompt-scan

PAYMENT          x402-verify, stripe-link, pricing-lookup, well-known-publish

LINEAGE          attest-lineage, recall-lineage, semantic-diff,
                 contradiction-detect

COORDINATION     swarm-relay, swarm-inbox, consensus-create/vote/result,
                 agent-plan, routing-recommend, delegation-depth (D_MAX=23)

EVOLUTION        agent-reputation, lora-capture-fix, lora-contribute

MARQUEE          ratchet-gate (CVE-2025-6514), verirand, trust-phase-oracle,
                 topological-identity, nexus-shield, veridelegate,
                 agent-discovery, sla-engine, escrow-open/release/dispute,
                 reputation-ledger

OWASP-2026       goal-alignment-check, tool-misuse-detect,
                 delegated-trust-validate, persistent-memory-audit,
                 emergent-behavior-probe, tool-poisoning-scan,
                 scope-validate, oauth21-gate

MARKETPLACE      marketplace-list/search/purchase/rate/payout
```

## MCP server

Every verb is also an MCP tool. Drop into Claude / Cursor / Windsurf:

```json
{
  "mcpServers": {
    "atomadic-nexus": {
      "command": "atomadic-nexus-mcp"
    }
  }
}
```

## x402 payment example

```python
# Caller agent
import httpx
from atomadic_nexus import sign_x402

headers = sign_x402(amount_usdc="0.008", chain="base")
r = httpx.post("https://nexus.atomadic.tech/v1/trust-gate", headers=headers, json={...})
# 200 OK + signed verdict if payment + sanctions pass
# 402 Payment Required if more funds needed (auto-retry)
```

## Codex anchors

The trust formulas are anchored to externally-verified lattice constants:

| Constant | Value | Source |
|---|---|---|
| `TAU_TRUST` | `1820/1823 ≈ 0.9984` | Niemeier K₂₄ / J₁ |
| `σ₀` | `1/√196560 ≈ 0.00226` | Leech lattice minimal vectors |
| `ε_KL` | `1/196884 ≈ 5e-6` | Monster J-invariant first Fourier coefficient |
| `RG_LOOP` | `47` | Convergence iteration bound |
| `D_MAX` | `23` | Max delegation depth |

## Pricing

- **Free tier**: entropy oracle, agent registration, health checks, 3 trust-gate calls / day
- **Pro**: $8 → 500 calls. No expiry.
- **Team / Enterprise**: usage-based; ask for quote
- **x402 USDC** on Base: $0.008–$0.080 per call by verb

Live pricing at [atomadic.tech/pricing](https://atomadic.tech).

## Live stats

```bash
curl https://sot.atomadic.tech/SoT.json | jq .flagships.nexus
```

## Sibling products

- **[atomadic-fuse](https://github.com/atomadictech/atomadic-fuse)** — the per-repo compiler. Fuse compiles, Nexus gates.
- **atomadic-marketplace** — the third flagship. Sell + buy + rate logic chains.

## Authors

Atomadic Tech. Headed by Thomas Ralph Colvin IV. Axiom 0: `∀t: |∂L/∂t| ≤ 0` — The Love Invariant, authored by Jessica Mary Colvin. Never negotiated.

## License

MIT. See [LICENSE](./LICENSE).
