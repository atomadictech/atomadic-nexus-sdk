"""Surface-import smoke tests for atomadic-nexus-sdk."""
from __future__ import annotations


def test_package_imports():
    import atomadic_nexus
    assert atomadic_nexus.__version__ == "0.1.0"


def test_client_class_exists():
    from atomadic_nexus import NexusClient
    assert NexusClient is not None
    for verb in ("trust_gate", "verirand", "hallucination_oracle",
                 "x402_verify", "attest_lineage", "agent_reputation",
                 "ratchet_gate", "nexus_shield"):
        assert hasattr(NexusClient, verb), f"NexusClient missing .{verb}"


def test_codex_anchors_present():
    from atomadic_nexus.client import CODEX_ANCHORS
    assert set(CODEX_ANCHORS) >= {"TAU_TRUST", "sigma_0", "epsilon_KL",
                                  "RG_LOOP", "D_MAX"}
    # Codex constants: TAU_TRUST ~ 0.9984
    assert 0.998 < CODEX_ANCHORS["TAU_TRUST"] < 1.0
    assert 0.002 < CODEX_ANCHORS["sigma_0"] < 0.003
    assert CODEX_ANCHORS["RG_LOOP"] == 47
    assert CODEX_ANCHORS["D_MAX"] == 23


def test_exceptions_are_typed():
    from atomadic_nexus import NexusError, PaymentRequired, RejectVerdict
    assert issubclass(PaymentRequired, NexusError)
    assert issubclass(RejectVerdict, NexusError)


def test_cli_list_does_not_crash():
    import subprocess, sys
    r = subprocess.run([sys.executable, "-m", "atomadic_nexus.cli", "list"],
                       capture_output=True, text=True, timeout=10)
    assert r.returncode == 0
    assert "TRUST" in r.stdout
    assert "trust-gate" in r.stdout


def test_sign_x402_helper():
    from atomadic_nexus.client import sign_x402
    h = sign_x402("0.008", chain="base")
    assert "X-Payment-Proof" in h
    assert "X-Payment-Chain" in h
    assert h["X-Payment-Chain"] == "base"
