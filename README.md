# Katana Credit Checker

Check Stargate v2 path credits and OFT adapter balances across all eligible Katana routing permutations.

## Usage

```bash
uv run check_credits.py
```

## What it checks

1. **Stargate v2 Path Credits** (`paths(dstEid)`) — Ethereum pool directional flow control for each spoke chain (USDT/USDC/ETH pools)
2. **Katana OFT Adapter `secondaryChainBalance`** — outbound credit on `NonDefaultMintBurnOftAdapter` for Katana -> Ethereum/Spoke routes (vbUSDT/vbUSDC/vbWETH/vbWBTC)

## Rebalancing

- Adapters marked `[LOW]` or `[EMPTY]` need `secondaryChainBalance` replenished by the adapter owner (`0x619D553686958A873A62B336b2DD97C3b25134EA`)
- Stargate path credits rebalance organically as cross-chain transfers flow in both directions
- See [Stargate pool dashboard](https://stargate.finance/pool) for TVL (path credits are a subset of TVL representing allowed directional flow)
