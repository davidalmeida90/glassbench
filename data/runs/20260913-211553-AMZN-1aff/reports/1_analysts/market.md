# AMZN (Amazon.com, Inc.) — Technical Analysis Report
**Analysis date:** 2026-09-13 | **Latest verified trading row:** 2026-09-11 (close 256.78) | **Exchange:** NMS | **Sector:** Consumer Cyclical / Internet Retail

---

## 1. Verified Market Snapshot (source of truth)

| Field | Value |
|---|---:|
| Open (9/11) | 254.09 |
| High (9/11) | 257.59 |
| Low (9/11) | 253.14 |
| **Close (9/11)** | **256.78** |
| Volume (9/11) | 26,682,800 |
| close_10_ema | 256.59 |
| close_50_sma | 255.25 |
| close_200_sma | 239.80 |
| rsi | 48.91 |
| boll (middle) | 258.96 |
| boll_ub | 266.66 |
| boll_lb | 251.26 |
| macd | -0.84 |
| macds | 0.27 |
| macdh | -1.11 |
| atr | 6.22 |

*Note: The `get_stock_data` pull and the verified snapshot agree — both terminate at the 2026-09-11 row (256.78). No data discrepancy to flag. 2026-09-12/13 are weekend non-trading days.*

---

## 2. Indicator Selection Rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume so that no single signal dominates:

1. **close_200_sma** — strategic trend anchor (golden/death-cross context).
2. **close_50_sma** — medium-term trend + dynamic support/resistance.
3. **close_10_ema** — fast momentum / entry timing.
4. **macd** — momentum-regime shift (crossover & zero-line).
5. **rsi** — overbought/oversold and divergence.
6. **boll_lb** — oversold/volatility floor (paired with the snapshot's `boll`/`boll_ub` for band context).
7. **atr** — volatility for stop placement and position sizing.
8. **vwma** — volume-weighted confirmation of the trend.

These avoid redundancy (no two oscillators measuring the same thing, no duplicate MACD components) while covering all four analytical dimensions.

---

## 3. Trend Structure

**Long-term (bullish, intact):** Price (256.78) sits **+7.1% above the 200 SMA (239.80)**, and the 200 SMA has been grinding higher every session (238.68 on 8/28 → 239.80 on 9/11). There is no death-cross risk; the strategic uptrend remains firmly in place.

**Medium-term (mixed-to-constructive):** The 50 SMA (255.25) is **rising steadily** (249.73 on 8/21 → 255.25 on 9/11), and price closed just **+0.6% above it**. The 50 SMA has effectively caught up to price — a classic "price rests on a rising medium-term average" configuration.

**Short-term (corrective):** The 10 EMA (256.59) has **declined continuously** from 267.18 on 8/12 to 256.59, and price is only marginally above it (+0.07%). This is the clearest sign the short-term trend is no longer up — it is flat-to-down and has been for roughly a month.

**The dominant narrative:** AMZN staged an explosive late-July/August breakout — from a 226.65 close on 7/29 to a 284.02 close on 8/3 (+25.3% in three sessions), accompanied by huge volume (101.8M on 7/30, 129.1M on 7/31, 90.8M on 8/3). Since that 284.02 peak, the stock has **sold off ~9.6%** and spent the last three weeks **consolidating in a tightening 249.5–259.5 band** while the moving averages converged beneath it.

---

## 4. Momentum

- **MACD has rolled over decisively.** The MACD line peaked at **8.43 on 8/11** and has bled lower ever since: +0.12 on 9/8 → **-0.42 on 9/9 → -0.88 on 9/10 → -0.84 on 9/11**. It crossed **below its signal line** (signal now 0.27, histogram -1.11) and below zero. This is a **fresh short-term bearish crossover** — momentum has shifted against the bulls over the past month.
- **RSI is neutral at 48.91** — no man's land. It is neither overbought nor oversold. Notably it had spiked to **72.23 on 8/3** (overbought at the peak) and has since cooled to the high-40s. It bottomed at 43.62 on 9/10 and ticked up to 48.91 on 9/11, showing a mild positive divergence versus price's 9/10 low — a small hint that selling pressure is easing.
- **Interpretation:** Momentum is *negative but decelerating*. There is no RSI washout (nothing below 40 recently), so this reads as a **controlled pullback/consolidation**, not a capitulation — which keeps the bullish higher-timeframe structure alive but offers no buy confirmation yet.

---

## 5. Volatility & Bands

- **ATR has compressed sharply**, from **9.98 (8/5)** to **6.22 (9/11)** — a ~38% decline in daily range. Volatility is contracting, typical of a coil/consolidation that often precedes a directional resolution.
- **Bollinger squeeze-to-neutral:** The lower band has **risen dramatically** from ~215.6 (8/10) to **251.26 (9/11)** as the wide August ranges got absorbed. The band width (UB 266.66 − LB 251.26 = **15.4**, ≈6% of price) is now moderate.
- **Price position:** At 256.78, price sits in the **lower half of the band** — below the middle (258.96) but ~2.2% above the lower band (251.26). Not oversold by band standards, but also not extended.

---

## 6. Volume Confirmation

- **VWMA (257.95) is slightly above price (256.78)** — a marginal negative. When price trades below its volume-weighted average, recent sellers have been transacting at slightly higher prices than buyers, consistent with the short-term corrective tone.
- VWMA has been **falling** (267.41 on 8/24 → 257.95 on 9/11), mirroring the drift lower.
- **Turnover has dried up:** recent sessions print 24–33M shares versus the 90–129M breakout volumes in late July/early August. Low-volume pullbacks into support are generally constructive, but low volume also means **weak conviction** in either direction — reinforcing the "wait for the breakout" stance.
- One outlier: **248.4M shares on 6/26** and the volume cluster 7/30–8/3 are clearly event-driven spikes; they should not be extrapolated as a trend signal.

---

## 7. Actionable Levels & Scenarios

**Support:**
- **255.25** — rising 50 SMA (first-line support; price closed just above it on 9/11).
- **251.3–249.6** — Bollinger lower band (251.26) + 9/10 intraday low (249.58). A decisive close below this zone would break the consolidation floor.
- **239.80** — 200 SMA (deeper strategic support).

**Resistance:**
- **258.96** — Bollinger middle / immediate ceiling.
- **266.4–267.6** — Bollinger upper band (266.66) and the late-August congestion highs (8/19 high 266.40; 8/28 high 267.56).
- **271–284** — August distribution zone (peak close 284.02 on 8/3).

**Scenarios:**
- **Bullish resolution:** A daily close **above 259 (Boll middle)** on rising volume that also reclaims VWMA (257.95), followed by MACD crossing back above its signal, would target the 266–267 zone. The 9/11 candle (open 254.09, close 256.78, near the highs) is an early constructive tell.
- **Bearish resolution:** A close **below 249.5** (violating both the Bollinger lower band and the 9/10 low) would confirm the short-term downtrend and open the door toward the 200 SMA at 239.80.
- **Base case (now):** Continued low-volatility chop between ~251 and ~259 until MACD and price resolve the standoff.

**Risk management:** With ATR at 6.22 (~2.4% of price), a reasonable swing stop is ~1.5–2× ATR (**roughly 9–12 points**) from entry, and position size should be scaled to that volatility. Volatility compression means stops placed too tight risk noise-driven exits.

---

## 8. Overall Assessment

AMZN presents a **tale of two timeframes**. The strategic picture is bullish — price is above a rising 200 SMA and rising 50 SMA, with the long-term trend never threatened. The tactical picture is corrective — MACD has crossed bearish and gone negative, price is below the Bollinger middle and VWMA, and short-term momentum has flatlined for a month. Crucially, none of the bearish evidence is *extreme* (RSI ~49, not oversold; price in the lower band, not at it), and volatility is quietly compressing — a setup that typically resolves into a range expansion rather than a sustained trend on its own.

The cleanest read: **a neutral, consolidation regime inside a larger uptrend.** The prudent stance is to let the range resolve rather than fight it — accumulate only on a confirmed reclaim of 259 with volume, or step aside if 249.5 fails.

---

## Key Points Summary

| Dimension | Indicator | Current Reading | Signal |
|---|---|---|---|
| Long-term trend | close_200_sma | 239.80 (rising); price +7.1% above | **Bullish** |
| Medium-term trend | close_50_sma | 255.25 (rising); price +0.6% above | **Mildly bullish / support** |
| Short-term trend | close_10_ema | 256.59 (falling); price +0.07% | **Neutral / flattening** |
| Momentum | macd / macds / macdh | -0.84 / 0.27 / -1.11 | **Bearish (fresh crossunder, below zero)** |
| Momentum oscillator | rsi | 48.91 | **Neutral** |
| Volatility (bands) | boll_lb / boll / boll_ub | 251.26 / 258.96 / 266.66 | **Price in lower half; compression** |
| Volatility (range) | atr | 6.22 (from 9.98 on 8/5) | **Contracting** |
| Volume trend | vwma | 257.95 (falling); price below | **Mildly bearish** |
| Key support | — | 255.25 (50 SMA) → 251.3–249.6 → 239.80 | Watch for holds/breaks |
| Key resistance | — | 258.96 → 266.4–267.6 → 271–284 | Breakout trigger ≈259 |
| Overall | — | Uptrend intact, short-term corrective consolidation | **HOLD / await range resolution** |

**FINAL TRANSACTION PROPOSAL: HOLD**