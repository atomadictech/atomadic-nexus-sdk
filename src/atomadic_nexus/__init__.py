"""Atomadic Nexus SDK — Trust Layer for the Agent Economy.

Public SDK v0.1.0. Wraps the hosted Nexus engine at nexus.atomadic.tech
behind a typed Python client + CLI + MCP server. 51 verbs across 7
families (TRUST, PAYMENT, LINEAGE, COORDINATION, EVOLUTION, MARQUEE,
OWASP, MARKETPLACE).

See README.md for quick start. Live stats:
    https://sot.atomadic.tech/SoT.json
"""
from __future__ import annotations

from .client import NexusClient
from .exceptions import NexusError, PaymentRequired, RejectVerdict

__all__ = ["NexusClient", "NexusError", "PaymentRequired", "RejectVerdict"]
__version__ = "0.1.0"
