"""Example: autonomous-agent x402 payment for a Nexus verb call.

Demonstrates the protocol shape — replace the stub signer with a real
EIP-712 typed-data signer against your wallet for production. The
hosted endpoint responds 402 with payment_url + amount_usdc if the
caller hasn't paid yet; the agent retries with X-Payment-Proof.

Run:
    pip install atomadic-nexus-sdk
    python examples/02_x402_payment.py
"""
import httpx

from atomadic_nexus.client import sign_x402


ENDPOINT = "https://nexus.atomadic.tech/v1/verirand"


def main() -> int:
    # Step 1: try the call without payment proof
    r = httpx.post(ENDPOINT, json={"n_bytes": 32}, timeout=10.0)
    print(f"first call: HTTP {r.status_code}")

    if r.status_code == 402:
        data = r.json() or {}
        amount = data.get("amount_usdc", "0.008")
        chain  = data.get("chain", "base")
        print(f"  402 Payment Required: {amount} USDC on {chain}")
        print(f"  payment_url: {data.get('payment_url')}")

        # Step 2: sign and retry (stub signer; real impl signs EIP-712
        # typed data against your wallet)
        headers = sign_x402(amount, chain=chain)
        r2 = httpx.post(ENDPOINT, json={"n_bytes": 32},
                        headers=headers, timeout=10.0)
        print(f"second call (after X-Payment-Proof): HTTP {r2.status_code}")
        if r2.status_code == 200:
            print(f"  random_hex: {r2.json().get('random_hex', '')[:32]}...")
            return 0
        print(f"  retry body: {r2.text[:200]}")
        return 1

    if r.status_code == 200:
        print(f"  200 OK (cached or free-tier): {r.json()}")
        return 0

    print(f"  unexpected: {r.text[:200]}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
