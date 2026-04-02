# /// script
# requires-python = ">=3.11"
# dependencies = ["web3>=7.0"]
# ///
"""
Check all credit balances for Katana routing permutations.

Usage: uv run check_credits.py
"""

import time

from web3 import Web3
import json

ETH_RPC = "https://ethereum-rpc.publicnode.com"
KATANA_RPC = "https://rpc.katana.network"

w3_eth = Web3(Web3.HTTPProvider(ETH_RPC))
w3_katana = Web3(Web3.HTTPProvider(KATANA_RPC))

# --- ABIs ---
PATHS_ABI = json.loads(
    '[{"inputs":[{"name":"eid","type":"uint32"}],"name":"paths","outputs":[{"name":"credit","type":"uint64"}],"stateMutability":"view","type":"function"}]'
)
SECONDARY_BALANCE_ABI = json.loads(
    '[{"inputs":[],"name":"secondaryChainBalance","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
)

# --- Stargate v2 Ethereum Pools ---
POOLS = {
    "USDT": {"address": "0x933597a323Eb81cAe705C5bC29985172fd5A3973", "sd": 6},  # pool 2
    "USDC": {"address": "0xc026395860Db2d07ee33e05fE50ed7bD583189C7", "sd": 6},  # pool 1
    "ETH": {"address": "0x77b2043768d28E9C9aB44E1aBfC95944bcE57931", "sd": 6},  # pool 13
}

# --- Spoke EIDs ---
SPOKES = {
    "Base": 30184,
    "Arbitrum": 30110,
    "Polygon": 30109,
    "Optimism": 30111,
    "BSC": 30102,
    "Mantle": 30181,
    "Avalanche": 30106,
    "Sei": 30279,
    "Gnosis": 30167,
}

# Which spokes each token can route to
TOKEN_SPOKES = {
    "USDT": ["Base", "Arbitrum", "Polygon", "Optimism", "BSC", "Mantle", "Avalanche", "Sei"],
    "USDC": [
        "Base",
        "Arbitrum",
        "Polygon",
        "Optimism",
        "BSC",
        "Mantle",
        "Avalanche",
        "Sei",
        "Gnosis",
    ],
    "ETH": ["Base", "Arbitrum", "Optimism", "Mantle", "Gnosis"],
}

# --- Katana OFT Adapters (NonDefaultMintBurnOftAdapter) ---
KATANA_ADAPTERS = {
    "vbUSDT": {
        "address": "0x4690f346337ed8737bea462ac71ff16ef95b985e",
        "decimals": 6,
    },
    "vbUSDC": {
        "address": "0x807275727Dd3E640c5F2b5DE7d1eC72B4Dd293C0",
        "decimals": 6,
    },
    "vbWETH": {
        "address": "0x694d1697f6909361775139357d99fb60b5cab683",
        "decimals": 18,
    },
    "vbWBTC": {
        "address": "0x8169e532bc781985e155037db1f96c267a520dfc",
        "decimals": 8,
    },
}

RATE_LIMIT_DELAY = 0.3  # seconds between Ethereum RPC calls


def format_amount(raw: int, decimals: int) -> str:
    if raw == 0:
        return "0"
    human = raw / (10**decimals)
    if human >= 1_000_000:
        return f"{human:,.0f}"
    elif human >= 1:
        return f"{human:,.2f}"
    else:
        return f"{human:.6f}"


def status_icon(raw: int, decimals: int) -> str:
    human = raw / (10**decimals)
    if raw == 0:
        return "EMPTY"
    elif human < 100:
        return "LOW"
    else:
        return "OK"


def check_path_credits():
    print("=" * 70)
    print("STARGATE v2 PATH CREDITS (Ethereum -> Spoke)")
    print("Querying paths(dstEid) on Ethereum Stargate v2 pools")
    print("Values in shared decimals (SD=6)")
    print("=" * 70)

    for token, pool_info in POOLS.items():
        contract = w3_eth.eth.contract(
            address=Web3.to_checksum_address(pool_info["address"]),
            abi=PATHS_ABI,
        )
        print(f"\n--- {token} pool ({pool_info['address']}) ---")
        for spoke in TOKEN_SPOKES[token]:
            eid = SPOKES[spoke]
            try:
                credit = contract.functions.paths(eid).call()
                human = format_amount(credit, pool_info["sd"])
                status = status_icon(credit, pool_info["sd"])
                print(
                    f"  -> {spoke:12s} (eid {eid}): {credit:>20d}  ({human:>14s})  [{status}]"
                )
            except Exception as e:
                print(f"  -> {spoke:12s} (eid {eid}): ERROR - {e}")
            time.sleep(RATE_LIMIT_DELAY)


def check_katana_adapter_balances():
    print("\n" + "=" * 70)
    print("OFT ADAPTER secondaryChainBalance (Katana)")
    print("Outbound credit for Katana -> Ethereum/Spoke routes")
    print("=" * 70)

    for token, info in KATANA_ADAPTERS.items():
        contract = w3_katana.eth.contract(
            address=Web3.to_checksum_address(info["address"]),
            abi=SECONDARY_BALANCE_ABI,
        )
        try:
            balance = contract.functions.secondaryChainBalance().call()
            human = format_amount(balance, info["decimals"])
            status = status_icon(balance, info["decimals"])
            print(
                f"  {token:8s} ({info['address']}): {balance:>30d}  ({human:>14s})  [{status}]"
            )
        except Exception as e:
            print(f"  {token:8s} ({info['address']}): N/A ({e})")


if __name__ == "__main__":
    print("Checking all credit balances for Katana routing...\n")
    check_path_credits()
    check_katana_adapter_balances()
    print("\n" + "=" * 70)
    print("Done. Forward empty/low balances to adapter owner for replenishment.")
    print("Adapter owner: 0x619D553686958A873A62B336b2DD97C3b25134EA")
    print("=" * 70)
