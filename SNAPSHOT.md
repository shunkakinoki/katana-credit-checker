# Credit Snapshot — 2026-04-03

Thresholds: **VERY LOW** < $10k USD, **LOW** < $100k USD, **OK** >= $100k USD

Prices: ETH $2,060 | BTC $67,043

## Katana OFT Adapter Balances

Outbound credit for Katana → Ethereum/Spoke routes. When empty, `_debit()` reverts with `Panic(0x11)`.

| Adapter | Address | Balance | USD Value | Status |
|---------|---------|---------|-----------|--------|
| vbUSDT | `0x4690f346` | $34.30 | $34 | VERY LOW |
| vbUSDC | `0x80727572` | $67,616,704 | $67,616,704 | OK |
| vbWETH | `0x694d1697` | 0.057 ETH | $118 | VERY LOW |
| vbWBTC | `0x8169e532` | 0.00006 BTC | $3.89 | VERY LOW |

Adapter owner: `0x619D553686958A873A62B336b2DD97C3b25134EA`

## Stargate v2 Path Credits — Outbound (Ethereum → Spoke)

Affects Katana → Spoke compose routes (second hop). When insufficient, `send()` reverts with `Path_InsufficientCredit`.

### USDT — pool `0x933597a3`

| Spoke | Credit | Status |
|-------|--------|--------|
| Base (30184) | $0 | EMPTY |
| Arbitrum (30110) | $7,641 | VERY LOW |
| Polygon (30109) | $5,440 | VERY LOW |
| Optimism (30111) | $2,115 | VERY LOW |
| BSC (30102) | $79,469 | LOW |
| Mantle (30181) | $49,638 | LOW |
| Avalanche (30106) | $16,071 | LOW |
| Sei (30279) | $0 | EMPTY |

### USDC — pool `0xc0263958`

| Spoke | Credit | Status |
|-------|--------|--------|
| Base (30184) | $286,362 | OK |
| Arbitrum (30110) | $1,841,574 | OK |
| Polygon (30109) | $88,389 | LOW |
| Optimism (30111) | $155,578 | OK |
| BSC (30102) | $1,701,616 | OK |
| Mantle (30181) | $179,009 | OK |
| Avalanche (30106) | $54,252 | LOW |
| Sei (30279) | $0 | EMPTY |
| Gnosis (30167) | $0 | EMPTY |

### ETH — pool `0x77b20437`

| Spoke | Credit | USD Value | Status |
|-------|--------|-----------|--------|
| Base (30184) | 312 ETH | $642,738 | OK |
| Arbitrum (30110) | 571 ETH | $1,175,189 | OK |
| Optimism (30111) | 272 ETH | $560,589 | OK |
| Mantle (30181) | 41 ETH | $83,892 | LOW |
| Gnosis (30167) | 0 | $0 | EMPTY |

## Stargate v2 Path Credits — Inbound (Spoke → Ethereum)

Affects Spoke → Katana compose routes (first hop). Managed by Stargate/LZ, rebalances organically.

### USDC — all spokes healthy

| Spoke | Credit | Status |
|-------|--------|--------|
| Base | $1,464,118 | OK |
| Arbitrum | $860,679 | OK |
| Polygon | $157,638 | OK |
| Optimism | $142,254 | OK |
| BSC | $354,235 | OK |
| Mantle | $288,415 | OK |
| Avalanche | $146,238 | OK |
| Sei | $170,833 | OK |
| Gnosis | $154,318 | OK |

### USDT — some spokes low

| Spoke | Credit | Status |
|-------|--------|--------|
| Arbitrum | $77,969 | LOW |
| Polygon | $116,977 | OK |
| Optimism | $99,574 | LOW |
| BSC | $727,176 | OK |
| Mantle | $65,734 | LOW |
| Avalanche | $82,117 | LOW |
| Sei | $283,092 | OK |

### ETH — Mantle and Gnosis low

| Spoke | Credit | USD Value | Status |
|-------|--------|-----------|--------|
| Base | 186 ETH | $383,160 | OK |
| Arbitrum | 271 ETH | $558,254 | OK |
| Optimism | 241 ETH | $496,798 | OK |
| Mantle | 34 ETH | $70,254 | LOW |
| Gnosis | 33 ETH | $68,867 | LOW |

## Action Items

1. **Critical — Katana team**: Replenish `secondaryChainBalance` on vbUSDT, vbWETH, vbWBTC adapters — all are VERY LOW, blocking all Katana outbound routes for these tokens
2. **Stargate/LZ — outbound**: USDT Ethereum→spoke paths are critically low across most spokes; Base/Sei are EMPTY
3. **Stargate/LZ — inbound**: USDC inbound is fully healthy. USDT inbound is LOW for Arbitrum ($78k), Optimism ($100k), Mantle ($66k), Avalanche ($82k). ETH inbound is LOW for Mantle ($70k) and Gnosis ($69k)
4. Stargate path credits rebalance organically with cross-chain volume — flag to LZ if specific routes are a priority
