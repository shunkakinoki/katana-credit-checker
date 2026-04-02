# Katana Credit Checker

Check Stargate v2 path credits and OFT adapter balances across all eligible Katana routing permutations.

## Usage

```bash
uv run check_credits.py
```

## What it checks

1. **Stargate v2 Path Credits** (`paths(dstEid)`) — Ethereum pool directional flow control for each spoke chain
2. **Katana OFT Adapter `secondaryChainBalance`** — outbound credit for Katana → Ethereum/Spoke routes
3. **Ethereum VaultOFT `secondaryChainBalance`** — outbound credit for Spoke→Katana and Eth→Katana routes

## Rebalancing

Adapters marked `[LOW]` or `[EMPTY]` need `secondaryChainBalance` replenished by the adapter owner (`0x619D553686958A873A62B336b2DD97C3b25134EA`). Path credits rebalance organically as cross-chain transfers flow.
