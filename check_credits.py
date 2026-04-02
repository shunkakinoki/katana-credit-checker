# /// script
# requires-python = ">=3.11"
# dependencies = ["web3>=7.0"]
# ///
"""
Check all credit balances for Katana routing permutations.

Usage: uv run check_credits.py
"""

import time
import urllib.request

from web3 import Web3
import json

RATE_LIMIT_DELAY = 0.3  # seconds between RPC calls

# --- RPC endpoints ---
RPCS = {
    "Ethereum": "https://ethereum-rpc.publicnode.com",
    "Arbitrum": "https://arbitrum-one-rpc.publicnode.com",
    "Base": "https://base-rpc.publicnode.com",
    "Polygon": "https://polygon-bor-rpc.publicnode.com",
    "Optimism": "https://optimism-rpc.publicnode.com",
    "BSC": "https://bsc-rpc.publicnode.com",
    "Mantle": "https://mantle-rpc.publicnode.com",
    "Avalanche": "https://avalanche-c-chain-rpc.publicnode.com",
    "Sei": "https://evm-rpc.sei-apis.com",
    "Gnosis": "https://gnosis-rpc.publicnode.com",
    "Katana": "https://rpc.katana.network",
}

# --- ABIs ---
PATHS_ABI = json.loads(
    '[{"inputs":[{"name":"eid","type":"uint32"}],"name":"paths","outputs":[{"name":"credit","type":"uint64"}],"stateMutability":"view","type":"function"}]'
)
SECONDARY_BALANCE_ABI = json.loads(
    '[{"inputs":[],"name":"secondaryChainBalance","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
)

# --- EIDs ---
ETHEREUM_EID = 30101

SPOKE_EIDS = {
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

# --- Stargate v2 Ethereum Pools (outbound: Ethereum -> Spoke) ---
ETH_POOLS = {
    "USDT": {"address": "0x933597a323Eb81cAe705C5bC29985172fd5A3973", "sd": 6},
    "USDC": {"address": "0xc026395860Db2d07ee33e05fE50ed7bD583189C7", "sd": 6},
    "ETH": {"address": "0x77b2043768d28E9C9aB44E1aBfC95944bcE57931", "sd": 6},
}

# Which spokes each token can route to (outbound)
OUTBOUND_SPOKES = {
    "USDT": ["Base", "Arbitrum", "Polygon", "Optimism", "BSC", "Mantle", "Avalanche", "Sei"],
    "USDC": ["Base", "Arbitrum", "Polygon", "Optimism", "BSC", "Mantle", "Avalanche", "Sei", "Gnosis"],
    "ETH": ["Base", "Arbitrum", "Optimism", "Mantle", "Gnosis"],
}

# --- Stargate v2 Spoke Pools (inbound: Spoke -> Ethereum) ---
SPOKE_POOLS = {
    "USDC": {
        "Base":      {"address": "0x27a16dc786820B16E5c9028b75B99F6f604b5d26", "sd": 6},
        "Arbitrum":  {"address": "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3", "sd": 6},
        "Polygon":   {"address": "0x9Aa02D4Fae7F58b8E8f34c66E756cC734DAc7fe4", "sd": 6},
        "Optimism":  {"address": "0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0", "sd": 6},
        "BSC":       {"address": "0x962Bd449E630b0d928f308Ce63f1A21F02576057", "sd": 6},
        "Mantle":    {"address": "0xAc290Ad4e0c891FDc295ca4F0a6214cf6dC6acDC", "sd": 6},
        "Avalanche": {"address": "0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47", "sd": 6},
        "Sei":       {"address": "0x45d417612e177672958dC0537C45a8f8d754Ac2E", "sd": 6},
        "Gnosis":    {"address": "0xB1EeAD6959cb5bB9B20417d6689922523B2B86C3", "sd": 6},
    },
    "USDT": {
        "Arbitrum":  {"address": "0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0", "sd": 6},
        "Polygon":   {"address": "0xd47b03ee6d86Cf251ee7860FB2ACf9f91B9fD4d7", "sd": 6},
        "Optimism":  {"address": "0x19cFCE47eD54a88614648DC3f19A5980097007dD", "sd": 6},
        "BSC":       {"address": "0x138EB30f73BC423c6455C53df6D89CB01d9eBc63", "sd": 6},
        "Mantle":    {"address": "0xB715B85682B731dB9D5063187C450095c91C57FC", "sd": 6},
        "Avalanche": {"address": "0x12dC9256Acc9895B076f6638D628382881e62CeE", "sd": 6},
        "Sei":       {"address": "0x0dB9afb4C33be43a0a0e396Fd1383B4ea97aB10a", "sd": 6},
    },
    "ETH": {
        "Base":      {"address": "0xdc181Bd607330aeeBEF6ea62e03e5e1Fb4B6F7C7", "sd": 6},
        "Arbitrum":  {"address": "0xA45B5130f36CDcA45667738e2a258AB09f4A5f7F", "sd": 6},
        "Optimism":  {"address": "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3", "sd": 6},
        "Mantle":    {"address": "0x4c1d3Fc3fC3c177c3b633427c2F769276c547463", "sd": 6},
        "Gnosis":    {"address": "0xe9aBA835f813ca05E50A6C0ce65D0D74390F7dE7", "sd": 6},
    },
}

# --- Katana OFT Adapters (NonDefaultMintBurnOftAdapter) ---
KATANA_ADAPTERS = {
    "vbUSDT": {"address": "0x4690f346337ed8737bea462ac71ff16ef95b985e", "decimals": 6, "token": "USDT"},
    "vbUSDC": {"address": "0x807275727Dd3E640c5F2b5DE7d1eC72B4Dd293C0", "decimals": 6, "token": "USDC"},
    "vbWETH": {"address": "0x694d1697f6909361775139357d99fb60b5cab683", "decimals": 18, "token": "WETH"},
    "vbWBTC": {"address": "0x8169e532bc781985e155037db1f96c267a520dfc", "decimals": 8, "token": "WBTC"},
}

# --- USD prices ---
TOKEN_USD_PRICE: dict[str, float] = {"USDT": 1.0, "USDC": 1.0}


def fetch_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            TOKEN_USD_PRICE["ETH"] = data["ethereum"]["usd"]
            TOKEN_USD_PRICE["WETH"] = data["ethereum"]["usd"]
            TOKEN_USD_PRICE["BTC"] = data["bitcoin"]["usd"]
            TOKEN_USD_PRICE["WBTC"] = data["bitcoin"]["usd"]
            print(f"ETH price: ${TOKEN_USD_PRICE['ETH']:,.0f}  |  BTC price: ${TOKEN_USD_PRICE['BTC']:,.0f}\n")
    except Exception as e:
        print(f"Warning: Could not fetch prices ({e}), using fallback ETH=$2000 BTC=$60000\n")
        TOKEN_USD_PRICE.update({"ETH": 2000, "WETH": 2000, "BTC": 60000, "WBTC": 60000})


def to_usd(human_amount: float, token: str) -> float:
    return human_amount * TOKEN_USD_PRICE.get(token, 1.0)


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


def status_label(raw: int, decimals: int, token: str) -> str:
    human = raw / (10**decimals)
    usd = to_usd(human, token)
    if raw == 0:
        return "EMPTY"
    elif usd < 10_000:
        return "VERY LOW"
    elif usd < 100_000:
        return "LOW"
    else:
        return "OK"


def print_path_row(spoke: str, eid: int, credit: int, sd: int, token: str):
    human = format_amount(credit, sd)
    status = status_label(credit, sd, token)
    print(f"  -> {spoke:12s} (eid {eid}): {credit:>20d}  ({human:>14s})  [{status}]")


def check_outbound_path_credits():
    print("=" * 70)
    print("STARGATE v2 PATH CREDITS — OUTBOUND (Ethereum -> Spoke)")
    print("Affects: Katana -> Spoke compose routes (second hop)")
    print("=" * 70)

    w3 = Web3(Web3.HTTPProvider(RPCS["Ethereum"]))
    for token, pool_info in ETH_POOLS.items():
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(pool_info["address"]),
            abi=PATHS_ABI,
        )
        print(f"\n--- {token} pool ({pool_info['address']}) ---")
        for spoke in OUTBOUND_SPOKES[token]:
            eid = SPOKE_EIDS[spoke]
            try:
                credit = contract.functions.paths(eid).call()
                print_path_row(spoke, eid, credit, pool_info["sd"], token)
            except Exception as e:
                print(f"  -> {spoke:12s} (eid {eid}): ERROR - {e}")
            time.sleep(RATE_LIMIT_DELAY)


def check_inbound_path_credits():
    print("\n" + "=" * 70)
    print("STARGATE v2 PATH CREDITS — INBOUND (Spoke -> Ethereum)")
    print("Affects: Spoke -> Katana compose routes (first hop)")
    print("=" * 70)

    for token, spokes in SPOKE_POOLS.items():
        print(f"\n--- {token} spoke pools -> Ethereum (eid {ETHEREUM_EID}) ---")
        for spoke, pool_info in spokes.items():
            rpc = RPCS.get(spoke)
            if not rpc:
                print(f"  -> {spoke:12s}: SKIP (no RPC)")
                continue
            try:
                w3 = Web3(Web3.HTTPProvider(rpc))
                contract = w3.eth.contract(
                    address=Web3.to_checksum_address(pool_info["address"]),
                    abi=PATHS_ABI,
                )
                credit = contract.functions.paths(ETHEREUM_EID).call()
                print_path_row(spoke, ETHEREUM_EID, credit, pool_info["sd"], token)
            except Exception as e:
                print(f"  -> {spoke:12s} (eid {ETHEREUM_EID}): ERROR - {e}")
            time.sleep(RATE_LIMIT_DELAY)


def check_katana_adapter_balances():
    print("\n" + "=" * 70)
    print("OFT ADAPTER secondaryChainBalance (Katana)")
    print("Affects: Katana -> Ethereum/Spoke outbound routes")
    print("=" * 70)

    w3 = Web3(Web3.HTTPProvider(RPCS["Katana"]))
    for name, info in KATANA_ADAPTERS.items():
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(info["address"]),
            abi=SECONDARY_BALANCE_ABI,
        )
        try:
            balance = contract.functions.secondaryChainBalance().call()
            human = format_amount(balance, info["decimals"])
            status = status_label(balance, info["decimals"], info["token"])
            print(f"  {name:8s} ({info['address']}): {balance:>30d}  ({human:>14s})  [{status}]")
        except Exception as e:
            print(f"  {name:8s} ({info['address']}): N/A ({e})")


if __name__ == "__main__":
    print("Checking all credit balances for Katana routing...\n")
    fetch_prices()
    check_outbound_path_credits()
    check_inbound_path_credits()
    check_katana_adapter_balances()
    print("\n" + "=" * 70)
    print("Done. Forward empty/low balances to adapter owner for replenishment.")
    print("Adapter owner: 0x619D553686958A873A62B336b2DD97C3b25134EA")
    print("=" * 70)
