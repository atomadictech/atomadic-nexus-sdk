"""Atomadic Nexus MCP server — wraps the hosted NexusClient as MCP tools.

Usage:
    atomadic-nexus-mcp     # stdio MCP server

Drop into Claude Desktop / Cursor / Windsurf MCP config:
    {
      "mcpServers": {
        "atomadic-nexus": {"command": "atomadic-nexus-mcp"}
      }
    }
"""
from __future__ import annotations

import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("mcp[cli] not installed -- install with: pip install 'atomadic-nexus-sdk[mcp]'",
          file=sys.stderr)
    sys.exit(1)

from .client import NexusClient


mcp = FastMCP("atomadic-nexus")
_client = NexusClient()


@mcp.tool()
def trust_gate(body_text: str, name: str = "") -> Any:
    """Classify + score a request. Returns verdict + Codex-anchored confidence."""
    return _client.trust_gate(body_text, name=name)


@mcp.tool()
def verirand(n_bytes: int = 32) -> Any:
    """Cryptographic verifiable randomness (VRF-grade)."""
    return _client.verirand(n_bytes=n_bytes)


@mcp.tool()
def hallucination_oracle(generation: str, grounding: str = "") -> Any:
    """Hallucination probe with certified confabulation bound."""
    return _client.hallucination_oracle(generation, grounding=grounding or None)


@mcp.tool()
def x402_verify(header: str) -> Any:
    """Verify an x402 payment-proof header (EIP-712 signed)."""
    return _client.x402_verify(header)


@mcp.tool()
def attest_lineage(artifact_sha: str) -> Any:
    """Attest provenance chain for an artifact."""
    return _client.attest_lineage(artifact_sha)


@mcp.tool()
def agent_reputation(agent_id: str) -> Any:
    """Per-agent reputation score (ERC-8004 compatible)."""
    return _client.agent_reputation(agent_id)


@mcp.tool()
def ratchet_gate(session_id: str) -> Any:
    """Session re-key gate (CVE-2025-6514 patched)."""
    return _client.ratchet_gate(session_id)


@mcp.tool()
def nexus_shield(payload: dict) -> Any:
    """Inline guardrail: trust + injection + hallucination in sub-200ms."""
    return _client.nexus_shield(payload)


def launch() -> None:
    mcp.run()


if __name__ == "__main__":
    launch()
