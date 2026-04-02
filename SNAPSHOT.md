# Credit Snapshot — 2026-04-03

## Katana OFT Adapter Balances

Outbound credit for Katana → Ethereum/Spoke routes. When empty, `_debit()` reverts with `Panic(0x11)`.

| Adapter | Address | Balance | Status |
|---------|---------|---------|--------|
| vbUSDT | `0x4690f346` | $34.30 | LOW — needs replenish |
| vbUSDC | `0x80727572` | $67,616,847 | OK |
| vbWETH | `0x694d1697` | 0.057 ETH | LOW — needs replenish |
| vbWBTC | `0x8169e532` | 0.00006 BTC | LOW — needs replenish |

Adapter owner: `0x619D553686958A873A62B336b2DD97C3b25134EA`

## Stargate v2 Path Credits (Ethereum → Spoke)

Directional flow control on Ethereum Stargate v2 pools. When insufficient, `send()` reverts with `Path_InsufficientCredit`.

### USDT — pool `0x933597a3`

| Spoke | Credit | Status |
|-------|--------|--------|
| Base (30184) | 0 | EMPTY |
| Arbitrum (30110) | $7,641 | OK |
| Polygon (30109) | $5,440 | OK |
| Optimism (30111) | $2,115 | OK |
| BSC (30102) | $109,172 | OK |
| Mantle (30181) | $49,638 | OK |
| Avalanche (30106) | $16,071 | OK |
| Sei (30279) | 0 | EMPTY |

### USDC — pool `0xc0263958`

| Spoke | Credit | Status |
|-------|--------|--------|
| Base (30184) | $286,362 | OK |
| Arbitrum (30110) | $1,841,574 | OK |
| Polygon (30109) | $88,389 | OK |
| Optimism (30111) | $155,578 | OK |
| BSC (30102) | $1,701,616 | OK |
| Mantle (30181) | $179,009 | OK |
| Avalanche (30106) | $54,252 | OK |
| Sei (30279) | 0 | EMPTY |
| Gnosis (30167) | 0 | EMPTY |

### ETH — pool `0x77b20437`

| Spoke | Credit | Status |
|-------|--------|--------|
| Base (30184) | 312 ETH | OK |
| Arbitrum (30110) | 571 ETH | OK |
| Optimism (30111) | 272 ETH | OK |
| Mantle (30181) | 41 ETH | LOW |
| Gnosis (30167) | 0 | EMPTY |

## Action Items

1. Replenish `secondaryChainBalance` on vbUSDT, vbWETH, vbWBTC adapters (adapter owner)
2. Stargate path credits rebalance organically — no action needed unless a specific route is critical
3. Sei and Gnosis routes are effectively dead for all tokens
