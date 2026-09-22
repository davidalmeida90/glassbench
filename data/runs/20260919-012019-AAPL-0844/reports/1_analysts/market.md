# AAPL — Technical Analysis Report
**Analysis date: 2026-05-15 | Ticker: AAPL (Apple Inc., NMS) | Business: Technology / Consumer Electronics**

*Source of truth: `get_verified_market_snapshot` for 2026-05-15. All exact price/indicator values below are drawn from that verified snapshot or from direct `get_indicators` output. No conflicting values were found between the two tools (verified snapshot MACD 9.51, boll 281.11, macds 7.73, macdh 1.77, boll_lb 257.72 are all internally consistent with the individually retrieved series).*

---

## 1. Verified Market State (2026-05-15)

| Field | Value |
|---|---:|
| Open | 297.64 |
| High | 302.94 |
| Low | 296.26 |
| **Close** | **299.97** |
| Volume | 54,862,800 |

AAPL closed at **$299.97**, its highest close in the entire Oct-2025 → May-2026 window retrieved. The session printed a new high of 302.94, closing near the top of the daily range — a constructive, momentum-preserving finish.

---

## 2. Indicator Selection & Rationale (8 chosen, complementary, non-redundant)

| # | Indicator | Value (2026-05-15) | Why it was chosen for THIS market |
|---|---|---|---|
| 1 | **close_10_ema** | 291.35 | Fast momentum/entry timing. Captures whether short-term thrust is still intact after a steep run. |
| 2 | **close_50_sma** | 265.74 | Medium-term trend + dynamic support reference for pullback entries. |
| 3 | **close_200_sma** | 258.43 | Long-term regime filter / golden-cross confirmation. |
| 4 | **macd** | 9.51 | Trend-momentum confirmation via EMA spread; validates the rally's underlying force. |
| 5 | **rsi** | 76.03 | Overbought/extension gauge — critical after a ~22% run in 6 weeks. |
| 6 | **boll_ub** | 304.51 | Breakout/extension zone; defines where price may stretch to in a strong trend. |
| 7 | **atr** | 6.23 | Volatility-based stop sizing and position sizing (risk management). |
| 8 | **vwma** | 284.95 | Volume-weighted confirmation that the advance is being supported by real participation. |

*Deliberately excluded as redundant: `macds`/`macdh` (derive from MACD), `boll`/`boll_lb` (band context captured via upper band + ATR), and `close_50`-duplicative momentum tools. RSI was used instead of a stochastics variant to avoid overlap.*

---

## 3. Trend Analysis — Moving Averages (Textbook Bullish Stack)

The moving-average structure is **fully bullish and accelerating**:

- **Price ($299.97) > 10 EMA (291.35) > 50 SMA (265.74) > 200 SMA (258.43)** — a clean, correctly ordered bullish alignment with no crossover conflicts.
- **Price sits +2.96% above the 10 EMA** — the 10 EMA has risen every day from 270.70 (2026-05-01) to 291.35 (2026-05-15), i.e. it is *not* flattening. Short-term momentum remains upward.
- **Price is +12.9% above the 50 SMA** and **+16.1% above the 200 SMA** — a wide, healthy but stretched spread typical of a mature thrust leg.
- **Golden-cross configuration:** the 50 SMA (265.74) is **2.83% above** the 200 SMA (258.43). Both are rising (50 SMA moved from 259.68 on 2026-04-01 → 265.74 on 2026-05-15; 200 SMA from 247.77 → 258.43 over the same span), confirming the long-term uptrend is intact and still building, not rolling over.

**Interpretation:** The stack is the strongest possible bullish arrangement. The main caveat is distance from the averages — mean-reversion risk increases the further price stretches, but there is no trend-break signal in any average.

---

## 4. Momentum — MACD & RSI

**MACD (9.51) vs Signal (7.73), Histogram (1.77):**
- MACD is **strongly positive** and above its signal line — an unambiguous bullish momentum regime.
- The MACD histogram (**+1.77, expanding**) indicates momentum is *increasing*, not merely positive. The MACD line has climbed monotonically from 4.35 (2026-05-01) to 9.51 (2026-05-15).
- Crucially, the MACD **crossed above zero** in mid-April: it was deeply negative in March (trough −4.18 on 2026-03-20) and turned positive on 2026-04-13 (0.08) → 2026-04-14 (0.24), marking the momentum regime change that launched this leg. Today's reading is the strongest of the entire advance.

**RSI (76.03):**
- Above the 70 overbought threshold. RSI has been climbing steadily: 61.77 (2026-05-04) → 69.41 (2026-05-06) → 72.94 (2026-05-08) → 76.03 (2026-05-15).
- **No bearish divergence observed** — price is making new highs *with* RSI making new highs, which is characteristic of a *strong* trend rather than an exhausted one. However, RSI in the mid-70s is a warning that the margin of safety for new longs is thin and that pullbacks can be sharp.
- For context, RSI was as low as **34.90 on 2026-03-20** — the swing low from which this rally began — showing how far the pendulum has swung.

---

## 5. Volatility — Bollinger Upper Band & ATR

**Bollinger Upper Band (304.51):**
- Price (299.97) is trading in the upper portion of the band envelope, roughly **1.5% below the upper band** (304.51), with the middle band at 281.11 and lower at 257.72.
- The bands are **expanding**: the upper band has risen sharply from 279.56 (2026-05-01) to 304.51 (2026-05-15), signaling a volatility expansion/breakout regime. In strong trends price can "ride the band," so the upper band acts less as a hard ceiling and more as the *upper edge of the new range*.
- Practical read: a close above ~304.51 would signal a fresh breakout extension; failure to hold and a move back toward the middle band (281.11) would begin to cool the trend.

**ATR (6.23):**
- Volatility has risen from the ~5.4–5.6 area in late March (e.g., 5.40 on 2026-03-25) to **6.23** now — consistent with the band expansion. ATR is 2.08% of price.
- **Risk-management use:** a 1×ATR stop is ~$6.23; a common 2–3×ATR swing stop for this setup implies ~$12–$19 of downside tolerance. Position size should be scaled down relative to a low-volatility regime to keep dollar risk constant.

---

## 6. Volume Confirmation — VWMA

- **VWMA = 284.95**, sitting **below** the current price ($299.97) and below the 10 EMA (291.35). Price above VWMA = volume-weighted participation confirms the uptrend.
- VWMA has risen every session from 269.69 (2026-05-01) to 284.95 (2026-05-15), meaning the *average traded price* is climbing — buyers are in control, not distribution.
- Volume on the recent breakout was firm: **79.9M on 2026-05-01** (a notable spike vs. the ~30–50M typical range) and 54.9M on the 2026-05-15 new-high session. This supports the move as participation-backed rather than a low-volume drift.
- Caveat: VWMA lags and can be skewed by single volume spikes (e.g., the 144.6M quad-witching session on 2025-12-19), so it is used here as confirmation, not a standalone trigger.

---

## 7. Actionable Insights & Scenario Framework

**Base case — trend continuation (bullish):**
- Structure favors the trend. Confirmation signals to watch: a daily close **above the Bollinger upper band (304.51)** with volume > recent average would mark a fresh breakout; sustained MACD histogram expansion (>1.77) supports continuation.
- Trend-following entries on shallow pullbacks toward the **10 EMA (291.35)** or the **region between 284.95 (VWMA) and 291.35** are the "buy-the-dip-in-an-uptrend" zones, where price has recently found support by proximity (price closed 292.43 on 2026-05-11 and 292.80 on 2026-05-08).

**Caution case — extension risk:**
- RSI at **76.03** and price **+12.9% above the 50 SMA** flag a stretched condition. Rallies can digest sideways or pull back sharply from such readings.
- A breakdown cue would be a close **below the 10 EMA (291.35)** followed by loss of the VWMA (284.95); a deeper support reference is the middle Bollinger band at 281.11. A move below the 50 SMA (265.74) would be required to question the medium-term trend — currently ~11.4% below price, so not an imminent concern.

**Risk management:**
- With ATR = 6.23, size positions so that stops (e.g., 2×ATR ≈ $12.5, or ~$287.5 from the current close) risk a fixed fraction of capital. Given the extended RSI, tighter trailing stops or scaled entries are prudent.

**What would invalidate the bull thesis:**
- MACD rolling back below its signal and toward zero, RSI breaking below ~50 on a pullback, or price closing decisively below the 50 SMA — none of which are present today.

---

## 8. Key Points Summary

| Dimension | Indicator | Verified Value (2026-05-15) | Signal |
|---|---|---:|---|
| Price | Close | 299.97 (High 302.94 / Low 296.26) | New multi-month closing high |
| Short-term trend | close_10_ema | 291.35 | Price above; rising daily → bullish |
| Medium-term trend | close_50_sma | 265.74 | Price +12.9% above; rising → bullish |
| Long-term trend | close_200_sma | 258.43 | Price +16.1% above; golden-cross intact |
| Trend structure | 50 vs 200 SMA | 265.74 vs 258.43 (+2.83%) | Bullish stack confirmed |
| Momentum | macd / macds / macdh | 9.51 / 7.73 / 1.77 | Positive, above signal, histogram expanding |
| Momentum regime shift | macd zero-cross | Turned positive 2026-04-13/14 | Launched current leg |
| Overbought gauge | rsi | 76.03 | Overbought; no divergence yet |
| Volatility band | boll_ub | 304.51 | Price ~1.5% below; breakout edge |
| Volatility (risk) | atr | 6.23 (2.08% of price) | Rising; size stops/size accordingly |
| Volume confirmation | vwma | 284.95 | Price above → participation-supported |
| Swing anchor | March low close | 246.19 (2026-03-30) | +21.8% to 299.97 (May 15) |

**Bottom line:** AAPL is in a robust, multi-timeframe uptrend with a fully aligned bullish moving-average stack, expanding MACD momentum, and volume confirmation. The one clear yellow flag is an overbought RSI (76.03) and stretched distance above the 50/200 SMAs, which argues for disciplined, staged entries on pullbacks rather than chasing strength, with ATR-based stops. No tool output currently signals a trend reversal.