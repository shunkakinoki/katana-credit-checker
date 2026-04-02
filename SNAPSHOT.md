# Credit Snapshot — 2026-04-03

Thresholds: **VERY LOW** < $10k USD, **LOW** < $100k USD, **OK** >= $100k USD

Prices: ETH $2,058 | BTC $67,009

## Katana OFT Adapter Balances

Outbound credit for Katana → Ethereum/Spoke routes. When empty, `_debit()` reverts with `Panic(0x11)`.

| Adapter | Address | Balance | USD Value | Status |
|---------|---------|---------|-----------|--------|
| vbUSDT | `0x4690f346` | $34.30 | $34 | VERY LOW |
| vbUSDC | `0x80727572` | $67,616,703 | $67,616,703 | OK |
| vbWETH | `0x694d1697` | 0.057 ETH | $118 | VERY LOW |
| vbWBTC | `0x8169e532` | 0.00006 BTC | $3.89 | VERY LOW |

Adapter owner: `0x619D553686958A873A62B336b2DD97C3b25134EA`

## Stargate v2 Path Credits (Ethereum → Spoke)

Directional flow control on Ethereum Stargate v2 pools. When insufficient, `send()` reverts with `Path_InsufficientCredit`.

### USDT — pool `0x933597a3`

| Spoke | Credit | USD Value | Status |
|-------|--------|-----------|--------|
| Base (30184) | 0 | $0 | EMPTY |
| Arbitrum (30110) | $7,641 | $7,641 | VERY LOW |
| Polygon (30109) | $5,440 | $5,440 | VERY LOW |
| Optimism (30111) | $2,115 | $2,115 | VERY LOW |
| BSC (30102) | $109,172 | $109,172 | OK |
| Mantle (30181) | $49,638 | $49,638 | LOW |
| Avalanche (30106) | $16,071 | $16,071 | LOW |
| Sei (30279) | 0 | $0 | EMPTY |

### USDC — pool `0xc0263958`

| Spoke | Credit | USD Value | Status |
|-------|--------|-----------|--------|
| Base (30184) | $286,362 | $286,362 | OK |
| Arbitrum (30110) | $1,841,574 | $1,841,574 | OK |
| Polygon (30109) | $88,389 | $88,389 | LOW |
| Optimism (30111) | $155,578 | $155,578 | OK |
| BSC (30102) | $1,701,616 | $1,701,616 | OK |
| Mantle (30181) | $179,009 | $179,009 | OK |
| Avalanche (30106) | $54,252 | $54,252 | LOW |
| Sei (30279) | 0 | $0 | EMPTY |
| Gnosis (30167) | 0 | $0 | EMPTY |

### ETH — pool `0x77b20437`

| Spoke | Credit | USD Value | Status |
|-------|--------|-----------|--------|
| Base (30184) | 312 ETH | $642,098 | OK |
| Arbitrum (30110) | 571 ETH | $1,174,204 | OK |
| Optimism (30111) | 272 ETH | $560,324 | OK |
| Mantle (30181) | 41 ETH | $83,811 | LOW |
| Gnosis (30167) | 0 | $0 | EMPTY |

## Action Items

1. **Critical**: Replenish `secondaryChainBalance` on vbUSDT, vbWETH, vbWBTC Katana adapters — all are VERY LOW, blocking outbound routes
2. **USDT paths**: Arbitrum/Polygon/Optimism are VERY LOW (<$10k), Mantle/Avalanche are LOW (<$100k), Base/Sei are EMPTY
3. **USDC paths**: Polygon and Avalanche are LOW; Sei and Gnosis are EMPTY
4. **ETH paths**: Mantle is LOW; Gnosis is EMPTY
5. Stargate path credits rebalance organically — no action needed unless a specific route is critical
