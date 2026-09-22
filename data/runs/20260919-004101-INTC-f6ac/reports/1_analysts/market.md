# INTC (Intel Corporation) — Technical Analysis Report
**Analysis date:** 2025-11-14 | **Exchange:** NMS | **Sector:** Technology / Semiconductors
**Verified close:** $35.52 (O 35.03 / H 36.10 / L 34.62) | **Volume:** 71,716,200

---

## 1. Market Context — What Happened to INTC

INTC is in the aftermath of one of the most violent repricings in the semiconductor space this year. Key data-supported milestones from the price series:

- **Short squeeze / repricing event:** On 2025-09-17 INTC closed $24.90; the very next session (2025-09-18) it **opened at $31.78** — a gap of roughly +27.6% — on **523.9 million shares** (the highest single-session volume in the entire dataset). This is a textbook volume-confirmed structural repricing, not drift.
- **Trend peak:** The rally extended to a **closing peak of $41.53 on 2025-10-28** (intraday high $42.48).
- **Current pullback:** From that $41.53 close to the verified $35.52 close on 2025-11-14, the stock has shed about **-14.5%**. The decline accelerated sharply this week: close $37.89 (11/12) → **$35.91 (11/13, ≈ -5.2%)** → $35.52 (11/14), on a downside gap (11/14 opened $35.03 versus the prior $35.91 close).

**Bottom line:** A parabolic, volume-driven uptrend has rolled over into a sharp but, so far, *contained* pullback. The question is whether this is a healthy retracement inside a still-intact uptrend or the start of a larger reversal. The indicator set below is chosen to answer that asymmetrically.

---

## 2. Indicator Selection & Rationale (8 indicators)

| # | Indicator | Category | Why selected (non-redundant role) |
|---|-----------|----------|-----------------------------------|
| 1 | close_10_ema | Trend – short | Captures the fast momentum turn; price has lost it. |
| 2 | close_50_sma | Trend – medium | The pivotal line separating "pullback" from "breakdown." |
| 3 | close_200_sma | Trend – long | Strategic bias / confirms structural uptrend. |
| 4 | macd | Momentum | Trend-change detection, confirmed crossover. |
| 5 | macds | Momentum | Crossover trigger / filters MACD noise. |
| 6 | rsi | Momentum | Overbought/oversold + divergence detection. |
| 7 | atr | Volatility | Size stops / position risk around wide swings. |
| 8 | vwma | Volume | Only volume-integrated view; confirms conviction/participation. |

Deliberately excluded to avoid redundancy: Bollinger bands (band values already verified in the snapshot and complement vwma/atr), stochrsi (duplicates rsi), macdh (derived from macd/macds already chosen).

---

## 3. Trend Structure (Multi-Timeframe)

**Long-term — strongly bullish.** The 200 SMA sits at **$25.05** and is rising every session (e.g., $24.21 on 10/31 → $25.05 on 11/14). Price at $35.52 is roughly **+41.8% above the 200 SMA**, a wide but not unprecedented extension for a momentum name. The 50 SMA ($34.63) is far above the 200 SMA ($25.05) — a clean bullish (golden-cross-aligned) structural stack. *Strategic bias remains up.*

**Medium-term — at a decision point.** The 50 SMA is at **$34.63** and rising. Price at **$35.52** remains *above* it by about $0.89 (~2.6%). This is the crux: as long as price holds the rising 50 SMA, the medium-term uptrend is technically intact and the move reads as a pullback. Notably, the **11/14 session low of $34.62 essentially touched the 50 SMA ($34.63)** — a coincident cluster that defines the near-term line in the sand.

**Short-term — bearish / momentum breakdown.** The 10 EMA is **$37.42** and has been declining for two weeks (from $39.35 on 11/3 to $37.42 on 11/14). Price is trading **~$1.90 below the 10 EMA**, confirming that short-term momentum has flipped decisively negative. The configuration — price below the 10 EMA but above the 50 SMA — is the classic signature of a pullback within a larger uptrend, not yet a trend reversal.

---

## 4. Momentum

**MACD — confirmed bearish crossover.** The MACD line (**0.43**) crossed *below* its signal line (**1.12**). Tracing the crossover: on 2025-10-29 MACD (2.42) was still above signal (2.39); by 2025-10-30 MACD (2.36) fell below signal (2.39) — the bearish cross landed around **2025-10-30**. Both lines have since rolled over hard (MACD from 3.19 on 10/10 to 0.43; signal from 3.05 to 1.12). Critically, the **histogram is negative and widening** (≈ -0.68 on 11/14 vs ≈ -0.51 on 11/12), meaning bearish momentum is still *accelerating*, not yet decelerating. This is a caution against premature bottom-fishing.

**RSI — fell to neutral-low, with a prior bearish divergence.** RSI is **43.49**, its lowest reading since mid-September, and it has dropped fast (52.9 on 11/12 → 44.9 on 11/13 → 43.5 on 11/14). It is no longer overbought but is **not oversold** — there is still room to fall before the 30 threshold. Importantly, there is a **bearish momentum divergence**: RSI peaked at **80.57 on 2025-09-26** while price made a *higher* closing peak of $41.53 on 2025-10-28, when RSI was only 73.37. Price up, RSI down = classic weakening-of-thrust signal that presaged this pullback.

**Takeaway:** Momentum is unambiguously deteriorating short term. No bullish momentum confirmation exists yet (no positive histogram, no RSI turn, no MACD re-cross).

---

## 5. Volatility & Risk

**ATR = $1.77** (verified snapshot), after peaking near **$2.00 on 2025-10-28**. Volatility more than doubled versus mid-September (ATR ≈ $0.87 on 9/17), reflecting the post-repricing regime. For risk management:
- A one-ATR daily move is ~$1.77, i.e. ~5% of price — position sizes should be scaled down accordingly.
- A 2×ATR stop (~$3.50) from $35.52 would sit near $32, deep below the 50 SMA — arguably too loose; tighter stops referenced to the $34.62 low / 50 SMA are more logical for active traders.

**Bollinger context (verified snapshot):** Middle **$38.40**, upper **$41.56**, lower **$35.25**. Price ($35.52) is now pressed against the **lower band ($35.25)** and is $2.88 below the middle band. Band width is wide (≈$6.31), consistent with the elevated-ATR regime. A decisive close below the lower band ($35.25) would confirm a volatility-expansion breakdown; a hold and reversal off it would be the first sign of stabilization.

---

## 6. Volume Analysis (VWMA)

**VWMA = $38.85**, sitting **above** spot ($35.52). This is a meaningful bearish tell: the volume-weighted average price of recent activity is ~$3.33 above the current price, meaning the *average recent buyer is underwater* and up-moves face overhead supply from trapped longs. The VWMA also sits above the 50 SMA and 10 EMA, reinforcing that recent volume has transacted at higher levels — a distribution-like footprint.

That said, downside volume is moderating versus the panic prints: 11/13 saw 95.6M shares but 11/14 cooled to 71.7M. Watching whether declines continue on *rising* or *falling* volume is the key tell — a low-volume drift down is more consistent with a shakeout; high-volume down days signal real distribution.

---

## 7. Actionable Read — Scenarios & Levels

**Bearish-leaning but trend-defining at the 50 SMA. Bias: neutral-to-cautious, wait for confirmation.**

- **Support cluster (critical): $34.62–$35.25.** This combines the 11/14 intraday low ($34.62), the rising 50 SMA ($34.63), and the Bollinger lower band ($35.25). A **close below $34.62–$34.63** flips the medium-term structure bearish. Below that, the next *structural* reference is distant (200 SMA at $25.05), with the post-gap consolidation zone roughly in the low-$30s acting as a waypoint — expect an air pocket if the 50 SMA fails.
- **Resistance ladder: $37.42 (10 EMA) → $38.40 (Boll middle) → $38.85 (VWMA).** Reclaiming the 10 EMA would be the first evidence the pullback is ending; reclaiming VWMA would restore the bull case.
- **What to watch:** (1) A MACD histogram that stops widening (flattens) = decelerating downside; (2) RSI holding above ~40–42 and turning up; (3) price defending the $34.62–35.25 cluster on *declining* volume.
- **Risk framing:** With ATR at $1.77, avoid tight stops that wide daily ranges will whipsaw; size positions for the elevated-volatility regime.

**Summary verdict:** INTC remains in a powerful long-term uptrend, but short-term momentum has broken (MACD bearish cross, negative widening histogram, RSI at 43 with a prior bearish divergence, price under the 10 EMA and under VWMA). The bull/bear line is the **$34.62–$35.25** cluster anchored by the rising 50 SMA. Hold = healthy pullback; decisive break = trend damage. No confirmed bullish reversal signal exists yet.

---

## 8. Key Points Summary Table

| Dimension | Indicator | Value (2025-11-14) | Signal | Interpretation |
|---|---|---|---|---|
| Price | Close / OHLC | 35.52 (O 35.03, H 36.10, L 34.62) | — | Gapped down, near session lows |
| Trend – short | close_10_ema | 37.42 (falling) | Bearish | Price ~$1.90 below; momentum flipped down |
| Trend – medium | close_50_sma | 34.63 (rising) | Bullish (at risk) | Price still above; 11/14 low $34.62 touched it |
| Trend – long | close_200_sma | 25.05 (rising) | Bullish | Price ~+41.8% above; structural uptrend intact |
| Momentum | macd | 0.43 | Bearish | Below signal; cross ~2025-10-30 |
| Momentum | macds | 1.12 | Bearish | Above MACD; downtrend |
| Momentum | macdh (derived) | ≈ -0.68 | Bearish, widening | Downside momentum still accelerating |
| Momentum | rsi | 43.49 | Weak/neutral | Not oversold; bearish divergence vs 10/28 peak |
| Volatility | atr | 1.77 | Elevated | Wide $1.77 daily range; size down |
| Volatility | boll / ub / lb | 38.40 / 41.56 / 35.25 | Pressed to lower band | Close < 35.25 = breakdown |
| Volume | vwma | 38.85 | Bearish | Spot below VWMA; average buyer underwater |
| Level – support | Cluster | 34.62–35.25 | Pivotal | 50 SMA + recent low + lower band |
| Level – resistance | Ladder | 37.42 / 38.40 / 38.85 | Overhead | 10 EMA, Boll middle, VWMA |
| Event | 2025-09-18 | Open 31.78, Vol 523.9M | Catalyst | ~+27.6% gap = structural repricing |
| Peak | 2025-10-28 | Close 41.53 (H 42.48) | — | -14.5% to current 35.52 |

*All exact price, OHLCV, and indicator figures are taken from the verified market snapshot and tool outputs for 2025-11-14; no discrepancies were found between the snapshot and the get_indicators results.*