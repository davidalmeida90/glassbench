# AAPL Technical Analysis Report — Analysis Date: 2026-05-15

**Resolved identity:** Apple Inc. (AAPL), Technology / Consumer Electronics, exchange NMS.

**Verified source-of-truth (snapshot, 2026-05-15):** Open 297.64 / High 302.94 / Low 296.26 / **Close 299.97** / Volume 54,862,800. Snapshot indicator values: close_10_ema 291.35, close_50_sma 265.74, close_200_sma 258.43, RSI 76.02, Bollinger middle 281.11, upper 304.51, lower 257.72, MACD 9.51, Signal 7.73, Histogram 1.77, ATR 6.23. *No discrepancy was found between the raw OHLCV series and the verification snapshot on the 2026-05-15 row.*

---

## 1. Market Context & Selected Indicators

AAPL is in a **well-established, accelerating uptrend** with a strongly stacked moving-average structure and elevated but not yet reversing momentum. To characterize this environment without redundancy, I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume:

| # | Indicator | Category | Why selected for THIS context |
|---|-----------|----------|-------------------------------|
| 1 | close_10_ema | Short-term MA | Captures the fast momentum leg and nearest dynamic support in an accelerating trend |
| 2 | close_50_sma | Medium-term MA | Confirms intermediate trend + serves as deeper dynamic support |
| 3 | close_200_sma | Long-term MA | Confirms strategic trend / golden-cross regime |
| 4 | rsi | Momentum | Flags overbought risk after a 2-week surge |
| 5 | macd | Momentum | Confirms the trend's momentum via EMA differential |
| 6 | macds | Momentum (signal) | Defines the crossover framework vs MACD |
| 7 | boll_ub | Volatility/extension | Measures how stretched price is (band-riding vs exhaustion) |
| 8 | atr | Volatility/risk | Sizes stops and positions given elevated price |
| — | vwma | Volume-weighted MA | Confirms the trend is volume-backed, not a thin drift |

*(Bollinger middle and lower band values are cited from the verified snapshot for context; RSI is used instead of a stochastics variant to avoid momentum redundancy.)*

---

## 2. Trend Structure — Strongly Bullish

- **Price vs. averages (all supportive):** Close 299.97 vs 10 EMA 291.35 (**+2.96%**), vs 50 SMA 265.74 (**+12.9%**), vs 200 SMA 258.43 (**+16.1%**). The perfect ordering — **price > 10 EMA > 50 SMA > 200 SMA** — is the textbook signature of a healthy uptrend.
- **Golden-cross regime intact:** The 50 SMA (265.74) sits well above the 200 SMA (258.43), and **both are rising** (50 SMA climbed from 259.49 on 2026-03-31 to 265.74; 200 SMA from 247.77 to 258.43). This is strategic confirmation, not a fresh crossover signal.
- **Short-term momentum is steepening:** The 10 EMA has risen every session from 270.70 (2026-05-01) to 291.35 (2026-05-15). The close is riding ~9 points above it — a sign of strong conviction, but also of short-term extension.

## 3. Momentum — Positive but Overbought

- **MACD firmly bullish:** MACD (9.51) > Signal (7.73), histogram +1.77 and expanding. The MACD line crossed above zero around **2026-04-13/14** (0.08 → 0.24) and has climbed monotonically since, with the MACD line sitting above the signal line continuously — **no bearish crossover warning** as of the analysis date.
- **RSI at 76.02 — overbought:** RSI has been above 70 since 2026-05-08 and closed the period at its highest reading of the sample (76.02). In strong trends RSI can remain extended, so this is a **caution flag, not an automatic sell signal** — but it does mean new long entries here carry elevated mean-reversion risk, and adds should ideally be on pullbacks rather than at the highs.

## 4. Volatility & Extension

- **Bollinger position:** Price 299.97 is in the **upper region of the bands** (middle 281.11, upper 304.51, lower 257.72). It is ~4.5 points below the upper band — stretched but **not yet closing above it**, so no clear exhaustion/breakout confirmation either way. Band width (~46.8 points) is wide, reflecting the recent strong move. In a trend this strong, price can "ride the band," so treat the upper band as a **potential resistance/overhead zone (≈304.5)**, and a close above it as a continuation signal rather than a reversal.
- **ATR = 6.23** (~2.1% of price). Volatility has eased modestly from the early-May peak (~6.69 on 2026-05-08) but remains meaningful. This is the right tool for stop placement and position sizing.

## 5. Volume Confirmation

- **VWMA = 284.95** vs close 299.97 — price trades ~15 points above the volume-weighted average, confirming the advance is **volume-backed** rather than a thin drift. The VWMA has risen in lock-step with price, so it acts as a secondary, volume-aware dynamic support level.
- Supporting volume reads: 2026-04-30 (91.8M) and 2026-05-01 (79.9M) mark the breakout acceleration; 2026-05-15 volume (54.9M) is healthy but not climactic — consistent with trend continuation rather than blow-off.

---

## 6. Actionable Trade Levels (derived from verified tool output)

**Support / pullback zones (long side reference):**
- **≈291.4** — 10 EMA (nearest dynamic support; first pullback dip-buy zone)
- **≈290.0** — psychological round number
- **≈285.0** — VWMA (volume-weighted support)
- **≈265.7 / 258.4** — 50 SMA / 200 SMA (deeper, higher-conviction trend support)

**Resistance / upside reference:**
- **≈300.0** — psychological round number (price closed just under at 299.97)
- **≈302.94** — 2026-05-15 intraday high
- **≈304.5** — Bollinger upper band (extension/continuation trigger)

**Risk management (ATR-based):**
- With ATR at 6.23, a 2×ATR stop from a swing entry is roughly **12.5 points**. A swing long entered near 300 with a 2×ATR stop would risk to ~287.5, just under the VWMA — a structurally coherent placement.

---

## 7. Nuanced Judgment

The **trend and momentum evidence is bullishly aligned across every timeframe**: MA stacking, rising 50/200 SMA, positive and expanding MACD, price above VWMA, and a fresh 302.94 intraday high. The **one genuine caveat is overbought extension** — RSI 76, price ~3% above the 10 EMA and near the upper band. This favors a **"hold / buy-on-dip" posture rather than chasing at the highs.** A healthy continuation would show price holding above the 10 EMA (~291) and VWMA (~285); a decisive close above the 304.5 upper band would signal trend acceleration, whereas an RSI divergence or a MACD histogram contraction while price stalls near 300–305 would be the first warning of a pullback toward the 285–291 support shelf. No bearish crossover or reversal confirmation is present as of 2026-05-15.

---

## Summary Table

| Dimension | Indicator(s) | Verified Value (2026-05-15) | Read / Signal |
|---|---|---|---|
| Price | Close | 299.97 | Near round-number 300; new intraday high 302.94 |
| Short-term trend | close_10_ema | 291.35 | Bullish; price +2.96% above, extension risk |
| Medium-term trend | close_50_sma | 265.74 (rising) | Bullish; support ~12.9% below price |
| Long-term trend | close_200_sma | 258.43 (rising) | Strategic uptrend; golden-cross regime intact |
| Momentum | rsi | 76.02 | Overbought — caution, not yet reversal |
| Momentum | macd / macds | 9.51 / 7.73 | Bullish; MACD > signal, no bearish cross |
| Momentum | macdh | 1.77 | Positive, expanding (momentum intact) |
| Volatility/extension | boll_ub / boll | 304.51 / 281.11 | Price in upper band zone; extended |
| Volatility/risk | atr | 6.23 (~2.1% of price) | Use ~12.5-pt 2×ATR stops |
| Volume | vwma | 284.95 | Trend volume-backed; secondary support |
| **Overall bias** | — | — | **Bullish trend; favor hold / buy-on-dip, avoid chasing at 300+** |

FINAL TRANSACTION PROPOSAL: **HOLD**