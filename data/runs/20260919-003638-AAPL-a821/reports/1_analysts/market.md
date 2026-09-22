# AAPL — Technical Analysis Report
**Analysis date:** 2025-11-14 | **Last verified close:** $271.67 | **Ticker:** AAPL (Apple Inc., NMS)

---

## 1. Data Integrity & Indicator Set

All figures below are anchored to the **verified market snapshot** (latest row 2025-11-14). The individual indicator feeds returned values that **agree** with the snapshot to the reported rounding (e.g., close_10_ema 270.1905 vs 270.19; rsi 65.085 vs 65.08; macd 5.2302 vs 5.23; atr 5.2348 vs 5.23; boll_ub 276.785 vs 276.79). **No discrepancies** were found between tool outputs.

**Indicators selected (8 total) and why they are complementary:**

| # | Indicator | Category | Rationale for selection |
|---|-----------|----------|--------------------------|
| 1 | close_10_ema | Moving Average (short) | Captures the immediate swing/pullback dynamic; price is only ~0.55% above it, so it's the tightest trend filter. |
| 2 | close_50_sma | Moving Average (medium) | Defines the medium-term trend and dynamic support for the current leg. |
| 3 | close_200_sma | Moving Average (long) | Strategic benchmark to confirm the primary bull structure (golden-cross regime). |
| 4 | macd | MACD / Momentum | Trend-following momentum and crossover regime; reveals deceleration. |
| 5 | rsi | Momentum | Independent momentum oscillator to flag overbought/exhaustion and divergence. |
| 6 | boll_ub | Volatility / Bands | Measures how extended price is relative to its 20-day envelope (breakout vs. mean-reversion zones). |
| 7 | atr | Volatility | Volatility-scaled stop placement and position sizing — essential given price at highs. |
| 8 | vwma | Volume | Volume-weighted confirmation of the trend (are buyers actually behind the move?). |

I deliberately avoided redundancy: only one short/medium/long average each, one momentum oscillator (RSI), one trend-momentum pair (MACD), one band edge (upper), one volatility (ATR), and one volume-weighted measure.

---

## 2. Verified Snapshot (2025-11-14)

| Field | Value |
|---|---:|
| Open | 270.31 |
| High | 275.21 |
| Low | 268.87 |
| **Close** | **271.67** |
| Volume | 47,431,300 |
| close_10_ema | 270.19 |
| close_50_sma | 255.01 |
| close_200_sma | 224.29 |
| RSI | 65.08 |
| Bollinger middle (boll) | 267.38 |
| Bollinger upper (boll_ub) | 276.79 |
| Bollinger lower (boll_lb) | 257.98 |
| MACD | 5.23 |
| MACD signal | 5.49 |
| MACD histogram | -0.26 |
| ATR | 5.23 |

### Price vs. key levels (derived from verified values)
- Close vs 10 EMA: **+1.48 (+0.55%)** — price hugging short-term trend
- Close vs 50 SMA: **+16.66 (+6.53%)** — moderately extended
- Close vs 200 SMA: **+47.38 (+21.13%)** — strongly extended
- Close vs VWMA (270.16): **+1.51 (+0.56%)** — price only marginally above volume-weighted average
- Close vs Bollinger middle: **+4.29**; vs upper band: **−5.12** below (inside band, upper half)
- Bollinger width: (276.79 − 257.98)/267.38 ≈ **7.0%** — moderate, not a squeeze
- ATR as % of price: 5.23/271.67 ≈ **1.93%** — normal single-day range

---

## 3. Trend Analysis — Primary Uptrend Fully Intact

The moving-average stack is textbook bullish:

**Close 271.67 > 10 EMA 270.19 > 50 SMA 255.01 > 200 SMA 224.29**

- **Long-term (200 SMA):** Risen steadily from 220.29 (2025-09-15) to 224.29 (2025-11-14) — a slow, persistent climb confirming a durable primary uptrend.
- **Medium-term (50 SMA):** Rose from 220.65 (2025-09-15) to 255.01 (2025-11-14) — roughly a **+34-point advance in two months**, showing the medium-term trend re-accelerated.
- **Golden-cross regime:** 50 SMA sits **~30.7 points above** the 200 SMA, and the spread has been widening — the classic signature of a healthy, established bull trend rather than a nascent crossover.
- **Short-term (10 EMA):** At 270.19, it has been rising every session into 2025-11-14. Price holding just above it (+0.55%) suggests the immediate uptrend remains intact but is no longer pressing away from it — the kind of pause seen during consolidation at highs.

**Interpretation:** The trend structure gives no bearish signal. However, the +6.5% premium over the 50 SMA and +21% premium over the 200 SMA indicate the move is *extended*, which raises mean-reversion/profit-taking risk on any momentum break.

---

## 4. Momentum Analysis — Fading Internals

This is where nuance appears: **price is near highs, but momentum is not confirming.**

- **MACD = 5.23 vs signal = 5.49 → histogram = −0.26.** The MACD line has slipped *below* its signal line, a mild bearish crossover. The histogram turned negative on the most recent reading.
- **MACD trajectory:** Peaked at **7.52 (2025-09-29)** and **7.41 (2025-10-02)**, collapsed to **2.64 (2025-10-17)** during the October dip, recovered to **6.19 (2025-11-03)**, then rolled over again to **5.23 (2025-11-14)**.
- **RSI = 65.08**, down from **71.68 on 2025-11-11**. It is *not* overbought now, but was on Nov 11. Earlier overbought peaks: **75.00 (2025-09-22)**, **72.32 (2025-09-23)**, **71.98 (2025-09-25)**, **71.09 (2025-10-30)**.

**Key nuance — bearish momentum divergence:** Price has printed successively higher closes into early November (Sept 22 close 255.14; Oct 30 close 270.40; Nov 11 close 274.50), yet:
- RSI's recent peak (71.68 on Nov 11) is **below** its September peak (75.00), and
- MACD's recent peak (6.19 on Nov 3) is **well below** its late-September peak (7.52).

This is a mild **negative divergence** — the rally is advancing with less momentum force. It's a *caution* flag, not a reversal signal, and it must be weighed against the still-bullish trend structure.

---

## 5. Volatility Analysis

- **Bollinger:** Upper 276.79, middle 267.38, lower 257.98. Price (271.67) sits in the **upper half but comfortably below the upper band (−5.12)**. Because price is not riding or tagging the upper band, this is *not* a burst/breakout extension — consistent with a consolidation-at-highs reading. The ~7% bandwidth indicates normal, non-compressed volatility (no imminent squeeze breakout).
- **ATR = 5.23 (~1.93% of price):** Stable and only modestly above the October lows (4.29 on 2025-10-08, 4.53 on 2025-09-18). Volatility is neither spiking nor collapsing. For risk framing, a 1× ATR stop under the recent consolidation would sit near **~266.4**, and a 2× ATR band near **~261.2**.

---

## 6. Volume Confirmation

- **VWMA = 270.16** vs close 271.67 — price is **+0.56% above** the volume-weighted average. This is only a marginal bullish tilt: it confirms that recent heavy-volume trade occurred near current prices, meaning the rally is *not* being rejected by volume-weighted sellers, but it also shows price isn't being dragged decisively above value.
- **Notable volume events in the dataset:** 163.7M shares on 2025-09-19 (close 244.60) and 105.5M on 2025-09-22 (close 255.14) — the big October/September breakout legs came on heavy volume. More recently, volume has been moderate (47.4M on 2025-11-14 vs the 100M+ breakout days), consistent with a lower-conviction consolidation phase rather than a fresh distribution or breakout.

---

## 7. Price Action Narrative (supported by tool data)

- **May–July:** Base-building and gradual recovery from the ~195 area (close 195.05 on 2025-05-07) up to the 210s.
- **August acceleration:** A sharp advance from close 201.94 (2025-08-05) to close 228.25 (2025-08-08) on elevated volume (names include 108.5M on Aug 6, 113.9M on Aug 8), then continuation into the 230s.
- **September breakout:** Closes stepped up to 244.60 (2025-09-19) and 255.14 (2025-09-22) on outsized volume, establishing the 250s as a new shelf.
- **October dip & recovery:** Pulled back to close 244.37 (2025-10-10), then recovered through 261.27 (2025-10-20) and into the high 260s/270s by month-end (close 270.40 on 2025-10-30; intraday high 276.30 on 2025-10-31).
- **November consolidation:** Range-bound between roughly 267.5 and 274.5 (closes: 268.70, 274.50, 272.73, 272.21, 271.67 from Nov 10 to Nov 14) — a tight, orderly pause near record levels.

---

## 8. Synthesis & Actionable Insights

**Overall stance: Bullish trend, but extended and losing momentum — a "hold with discipline" rather than an aggressive fresh-buy setup.**

1. **Trend (primary): Constructive.** The clean MA stack and widening 50/200 gap argue against fighting the trend. Trend-followers should remain long-biased while price holds above the 10 EMA (~270.19) and especially the 50 SMA (~255.01).
2. **Momentum (caution):** The MACD bearish crossover (5.23 < 5.49) and the mild RSI/MACD divergence versus September peaks warn that upside thrust is diminishing. Longs may consider **trailing stops** rather than adding at current levels.
3. **Extension risk:** +6.5% above the 50 SMA and +21% above the 200 SMA leave little cushion; a routine mean-reversion could target the Bollinger middle (267.38) or the 50 SMA (255.01) without breaking the trend.
4. **Key levels to watch:**
   - **Immediate support:** 10 EMA ~270.19; Nov consolidation lows ~267.5; Bollinger middle 267.38.
   - **Deeper support:** Bollinger lower 257.98; 50 SMA 255.01.
   - **Resistance/extension:** Bollinger upper 276.79; recent intraday high 276.30 (2025-10-31) and 2025-11-14 high 275.21. A decisive close above ~277 would likely coincide with a fresh MACD re-acceleration.
5. **Risk management:** With ATR ≈ 5.23, position sizing should assume ~$5 daily swings. A stop below the ~266–267 consolidation floor (roughly 1× ATR beneath price) limits damage while allowing normal noise.
6. **Trigger logic:**
   - *Bullish re-entry:* MACD histogram turning positive again **and** a close reclaiming/breaking above ~275–277 with above-average volume.
   - *Bearish caution:* A close below the 10 EMA (270.19) followed by loss of the Bollinger middle (267.38), with MACD histogram staying negative.

**Bottom line:** AAPL is in a confirmed, mature uptrend trading just beneath record highs, but momentum internals (MACD negative crossover, RSI/MACD lower highs) and a stretched distance above the 50/200 SMAs make this a spot for disciplined trend-following with tight, volatility-based risk controls — not undisciplined chasing.

---

## 9. Key Points Summary

| Dimension | Indicator | Value (2025-11-14) | Signal | Actionable Takeaway |
|---|---|---|---|---|
| Price | Close | 271.67 | — | Near-record territory; low 268.87 / high 275.21 on the day |
| Short trend | close_10_ema | 270.19 | Bullish (price +0.55%) | Tight support; loss = short-term momentum break |
| Medium trend | close_50_sma | 255.01 | Bullish (price +6.53%) | Medium-term support; rising steeply |
| Long trend | close_200_sma | 224.29 | Bullish (price +21.13%) | Primary uptrend confirmed; extended |
| Trend structure | 50 vs 200 SMA | +30.72 spread | Bullish golden-cross regime | Widening gap = healthy but mature trend |
| Momentum | MACD / signal | 5.23 / 5.49 | **Mild bearish crossover** (hist −0.26) | Deceleration; avoid chasing |
| Momentum | RSI | 65.08 | Neutral-to-strong (was 71.68 Nov 11) | Not overbought now; watch for divergence |
| Volatility | Bollinger upper | 276.79 | Price 5.12 below band | Room to run; not over-extended vs band |
| Volatility | ATR | 5.23 (~1.93%) | Normal | Size positions for ~$5 daily swings |
| Volume | VWMA | 270.16 | Mild bullish (price +0.56%) | Volume confirms value near price, no rejection |

*Source of truth for all exact prices and indicator values: verified market snapshot dated 2025-11-14 (AAPL). No conflicts were detected between the snapshot and the individual indicator feeds.*