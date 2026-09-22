# PFE (Pfizer Inc.) — Technical Analysis Report
**Analysis date:** 2026-02-13 | **Exchange:** NYQ | **Sector:** Healthcare / Drug Manufacturers – General
**Verified latest close:** $26.67 (Open 26.68 / High 27.01 / Low 26.64 / Volume 36,986,700)

> All exact OHLCV and indicator figures below are taken from the **get_verified_market_snapshot** for 2026-02-13 (source of truth) and the **get_stock_data** CSV (2025-08-01 → 2026-02-13). I cross-checked the indicator series from **get_indicators** against the snapshot; **no material discrepancies were found** (e.g., 10-EMA 26.1996→26.20, 50-SMA 24.704→24.70, 200-SMA 23.261→23.26, RSI 64.46, MACD 0.6096→0.61, Bollinger Upper 27.147→27.15, ATR 0.5925→0.59, VWMA 25.796→25.80).

---

## 1. Selected Indicators and Rationale (8 total, non-redundant)

| Indicator | Category | Why it is relevant *now* for PFE |
|---|---|---|
| **close_200_sma** | Trend (long) | Strategic anchor. Confirms the multi-month uptrend and defines the "golden-cross" regime (50-SMA well above 200-SMA). |
| **close_50_sma** | Trend (medium) | Medium-term trend + dynamic support reference; rising steadily, giving a robust invalidation floor. |
| **close_10_ema** | Trend (short) | Responsive momentum gauge for timing entries/exits in an accelerating move. |
| **macd** | Momentum | Captures the January regime shift (negative → positive) and current positive impulse. |
| **rsi** | Momentum | Flags overbought risk / potential divergence as price nears highs (currently sub-70). |
| **boll_ub** | Volatility | Defines the overbought/breakout envelope; price is trading in the upper half of the bands. |
| **atr** | Volatility | Sets volatility-scaled stops and position sizing; ATR is expanding, a key risk input. |
| **vwma** | Volume | Confirms the trend is volume-supported rather than a thin drift. |

These span trend (3 timeframes), momentum (2), volatility (2) and volume (1) — complementary, with no redundant pairs (e.g., I deliberately avoided using both RSI and StochRSI, or all three MACD lines).

---

## 2. Trend Structure — Clean Bullish Stacking

The moving-average architecture is textbook bullish alignment:

- **Close $26.67 > 10-EMA $26.20 > 50-SMA $24.70 > 200-SMA $23.26.**
- Price sits **~1.8% above the 10-EMA**, **~8.0% above the 50-SMA**, and **~14.7% above the 200-SMA** (derived from the two verified price/MA points).
- The **50-SMA is $1.44 above the 200-SMA** — a confirmed golden-cross regime that has been widening, indicating a durable intermediate uptrend rather than a fleeting bounce.
- All three averages are **sloping upward**: the 10-EMA rose every session from 25.62 (Feb 9) → 26.20 (Feb 13); the 50-SMA rose from 24.31 (Feb 2) → 24.70 (Feb 13); the 200-SMA rose from 23.00 (Feb 2) → 23.26 (Feb 13).

**Trend trajectory:** From the August 2025 base (~$22), PFE gapped sharply higher on **2025-09-30 → 2025-10-01** (close $23.81 then $25.43 on very heavy volume of 164.9M and 150.9M shares — the two largest volume days in the dataset). Price then corrected through October (low close $22.64 on 2025-10-16, filling the early-October gap) and December, building a **higher-low base around $23.7–24.0** (late Dec/early Jan). Since mid-January it has trended steadily higher, culminating in the current push to the **$27.01 intraday high** (Feb 11 and again Feb 13) — the highest print in the visible Aug-2025-to-Feb-2026 window.

---

## 3. Momentum — Positive but Not Yet Extended

**MACD (verified): 0.61 vs. Signal 0.50, Histogram +0.11.**
- The MACD line crossed **from negative to positive around Jan 13–14, 2026** (0.0002 on Jan 13 → 0.0256 on Jan 14), then accelerated: 0.21 (Jan 26) → 0.34 (Jan 30) → 0.39 (Feb 4) → 0.61 (Feb 13).
- MACD remains above its signal line with a **positive histogram**, confirming the uptrend has momentum behind it. Note the histogram has flattened slightly (0.11 vs. ~0.09 the prior weeks) — momentum is strong but no longer accelerating parabolically, a mild early caution flag.

**RSI (verified): 64.46** (up from 62.38 on Feb 9).
- Below the 70 overbought threshold, leaving **headroom** before an extreme reading.
- Recent RSI peaks: **70.80 on Jan 27** (briefly overbought) and **67.13 on Feb 11**; the current 64.46 is a slight cooling from that Feb 11 peak, consistent with a controlled consolidation near highs rather than an exhausted blow-off.
- No bearish RSI divergence is evident from the tool output: price made a higher high into Feb 11 (close 26.81, the highest close in the dataset) while RSI also printed a secondary high (67.13), so momentum confirmed price.

---

## 4. Volatility — Expanding, Price in Upper Band

**Bollinger Bands:** Middle (20-SMA) 25.54 / Upper 27.15 / Lower 23.93.
- The close of **$26.67 sits at roughly the 85th percentile of the band** (%B ≈ 0.85) — in the upper half, pressing toward the upper band but **not yet riding/breaking it**.
- Band width (Upper − Lower) ≈ **$3.22**, and the upper band has climbed from 25.80 (Feb 2) → 27.15 (Feb 13) — the envelope is expanding upward, reflecting the accelerating advance.
- An upper-band tag/break above **$27.15** would signal a breakout initiation; failure near it is the most likely place for a short-term stall.

**ATR (verified): 0.59** (≈2.2% of price).
- ATR has **risen from a January trough near 0.435 (Jan 2)** to 0.59 now, with a recent peak of ~0.614 (Feb 10). Volatility is **expanding** alongside the rally — healthy for trend traders but it means stops must be wider and position sizes smaller.

---

## 5. Volume Confirmation

**VWMA (verified): 25.80** vs. close 26.67 — price is trading **above the volume-weighted average**, confirming that recent gains are backed by real participation rather than thin drift. The VWMA has risen every session from 24.81 (Feb 2) to 25.80 (Feb 13).

Volume context: Recent sessions run ~37–83M shares. The **Feb 3–4 window** was notable — a high-volume down day (91.96M, close 24.92) followed immediately by a high-volume up day (83.03M, close 25.89), suggesting the dip was absorbed. The current Feb 13 volume (36.99M) is on the lighter side, which is normal for a mild consolidation day but is something to monitor for a breakout needing confirmation.

---

## 6. Key Levels (directly from tool output)

| Type | Level | Source |
|---|---|---|
| **Immediate resistance** | **$27.01** | Intraday high on both 2026-02-11 and 2026-02-13 |
| **Breakout trigger** | **$27.15** | Bollinger Upper Band (verified) |
| **First support** | **$26.20** | 10-EMA (verified) |
| **Secondary support** | **$25.54–25.80** | Bollinger Middle ($25.54) / VWMA ($25.80); late-Jan consolidation closes (25.56 on Jan 30, 25.78 on Feb 2) |
| **Trend floor** | **$24.70** | 50-SMA (verified) |
| **Structural floor** | **$23.93 / $23.26** | Bollinger Lower Band / 200-SMA (verified) |

---

## 7. Actionable Insights & Scenarios

**Base case (bullish continuation):** Trend, momentum and volume all align. A decisive close **above $27.01–27.15 on above-average volume** would confirm a breakout and open the door to trend continuation. Momentum traders could look for the 10-EMA ($26.20) to hold on any intraday dip as an add/entry zone.

**Pullback-buy scenario:** RSI at 64.46 and price at the 85th band percentile argue for **buying strength on pullbacks rather than chasing**. The $25.5–26.2 zone (10-EMA + VWMA + prior consolidation) is the highest-probability dip-buy area within the trend; a deeper flush to the 50-SMA ($24.70) would be the trend-following re-entry of last resort.

**Caution / invalidation:** The setup deteriorates if price closes decisively **below the 50-SMA ($24.70)** — that would break the medium-term trend structure and put the $23.93 Bollinger lower band / $23.26 200-SMA back in play. Watch also for an MACD bearish crossover (MACD line falling below the 0.50 signal) and/or RSI pushing above 70 and then reversing — either would be an early momentum-warning.

**Risk management:** With ATR at **$0.59**, a reasonable volatility-scaled stop for a swing position is roughly **1.5–2× ATR (~$0.90–1.20)** below entry. Position sizes should be scaled down relative to the calmer January regime given the ~35% expansion in ATR from the Jan 2 trough (0.435 → 0.59).

**Caveats / data notes:**
- The visible dataset begins 2025-08-01; the $27.01 print is the highest **in this window**, not a confirmed 52-week or all-time high.
- Two quarterly dividends of $0.43 (ex-dates 2025-11-07 and 2026-01-23) are reflected in the CSV; price-return figures above are unadjusted for those payouts.
- No tool discrepancy was identified; all indicator values reconcile with the verified snapshot.

---

## 8. Summary Table

| Dimension | Indicator (value, 2026-02-13) | Reading | Implication |
|---|---|---|---|
| Price | Close **26.67** | Above all key MAs | Bullish |
| Long trend | 200-SMA **23.26** | Price +~14.7% above; rising | Strategic uptrend intact |
| Medium trend | 50-SMA **24.70** | Price +~8.0% above; rising; > 200-SMA | Golden-cross regime |
| Short trend | 10-EMA **26.20** | Price +~1.8% above; rising | Strong near-term momentum |
| Momentum | MACD **0.61** vs Signal **0.50** (Hist +0.11) | Positive & above signal | Bullish; mild deceleration |
| Momentum | RSI **64.46** | Sub-70, cooling from 67.13 | Room to run; not overbought |
| Volatility | Bollinger Upper **27.15** (Mid 25.54, Lower 23.93) | %B ≈ 0.85 | Pressing upper band; breakout watch |
| Volatility | ATR **0.59** | Expanding (up from ~0.435 on Jan 2) | Wider stops / smaller size |
| Volume | VWMA **25.80** | Price above VWMA | Trend volume-confirmed |
| Key resistance | **27.01 / 27.15** | Feb 11 & 13 highs / Boll upper | Breakout trigger |
| Key support | **26.20 → 25.54–25.80 → 24.70** | 10-EMA / Mid+VWMA / 50-SMA | Dip-buy ladder |
| Invalidation | Close **< 24.70** | 50-SMA breach | Trend structure compromised |

**Bottom line:** PFE is in a well-established, volume-confirmed uptrend with a clean bullish moving-average stack, positive MACD, and RSI that is bullish but not yet stretched. The stock is pressing its recent highs and upper Bollinger band, so the reward/risk favors **breakout confirmation above ~$27.15 or disciplined dip-buys toward $26.20 / $25.50**, with a trend invalidation level at the 50-SMA (**$24.70**) and volatility-scaled stops of roughly $0.90–1.20 (1.5–2× ATR).