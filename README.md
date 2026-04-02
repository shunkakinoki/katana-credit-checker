# Katana Credit Checker

Check Stargate v2 path credits and OFT adapter balances across all eligible Katana routing permutations.

## Highlights (2026-04-03)

**Katana OFT adapters — outbound blocked:**
- vbUSDT ($34), vbWETH (0.06 ETH), vbWBTC (0.00006 BTC) are effectively empty — all Katana outbound routes for these tokens will revert
- vbUSDC ($67.6M) is healthy

**Stargate path credits — outbound (Ethereum to spoke):**
- USDT is critically low across most spokes: Arb/Polygon/Optimism < $10k, Base/Sei at zero
- USDC is healthy for major spokes, but Polygon ($88k) and Avalanche ($54k) are below $100k; Sei/Gnosis at zero
- ETH is healthy for Base/Arb/Optimism; Mantle ($84k) is low; Gnosis at zero

**Stargate path credits — inbound (spoke to Ethereum):**
- USDC inbound is fully healthy across all spokes
- USDT inbound is LOW for Arbitrum ($78k), Optimism ($100k), Mantle ($66k), Avalanche ($82k)
- ETH inbound is LOW for Mantle ($70k) and Gnosis ($69k)

**Action needed:** Adapter owner (`0x619D...1EA`) must replenish `secondaryChainBalance` on vbUSDT, vbWETH, vbWBTC. See [full snapshot](SNAPSHOT.md).

## Usage

```bash
uv run check_credits.py
```

## What it checks

1. **Stargate v2 Path Credits — Outbound** (`paths(dstEid)` on Ethereum pools) — directional flow control for Katana -> Spoke routes (second hop)
2. **Stargate v2 Path Credits — Inbound** (`paths(dstEid)` on spoke pools) — directional flow control for Spoke -> Katana routes (first hop)
3. **Katana OFT Adapter `secondaryChainBalance`** — outbound credit on `NonDefaultMintBurnOftAdapter` for Katana -> Ethereum/Spoke routes (vbUSDT/vbUSDC/vbWETH/vbWBTC)

## Rebalancing

- Adapters marked `[LOW]` or `[EMPTY]` need `secondaryChainBalance` replenished by the adapter owner (`0x619D553686958A873A62B336b2DD97C3b25134EA`)
- Stargate path credits rebalance organically as cross-chain transfers flow in both directions
- See [Stargate pool dashboard](https://stargate.finance/pool) for TVL (path credits are a subset of TVL representing allowed directional flow)
