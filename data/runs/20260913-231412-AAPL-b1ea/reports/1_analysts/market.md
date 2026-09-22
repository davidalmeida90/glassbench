# AAPL — Technical Analysis Report
**Analysis date:** 2026-05-15 | **Last verified close:** $299.97 | **Company:** Apple Inc. (NMS)

---

## 1. Executive Summary

AAPL is in a **well-established, broad-based uptrend** that has accelerated sharply over the last two weeks. Price sits above every major moving average (10 EMA, 50 SMA, 200 SMA, and VWMA), MACD momentum is positive and expanding, and the 50/200 SMA configuration remains bullish ("golden cross" alignment). The one caution flag is that momentum is stretched: **RSI = 76.02** (overbought) and price is **~16% above the 200 SMA**, making the advance extended and vulnerable to profit-taking or mean-reversion pullbacks. The trend is up, but the *risk/reward for fresh entries at the highs is deteriorating*.

All figures below are cross-checked against the verified market snapshot for 2026-05-15; the raw OHLCV from `get_stock_data` matches the snapshot (no discrepancies found).

---

## 2. Price Structure & Trend (Moving Averages)

**Selected indicators:** `close_10_ema`, `close_50_sma`, `close_200_sma`

| Level | Value (2026-05-15) | Close vs Level |
|---|---:|---:|
| Close | 299.97 | — |
| 10 EMA | 291.35 | +2.96% above |
| 50 SMA | 265.74 | +12.88% above |
| 200 SMA | 258.43 | +16.08% above |

- **Perfect bullish stacking.** Price > 10 EMA > 50 SMA > 200 SMA, the classic signature of a healthy primary uptrend. None of these averages has been tested on the downside during the current leg.
- **Golden-cross regime.** The 50 SMA (265.74) is comfortably above the 200 SMA (258.43), and both are *rising* — the 50 SMA has climbed every session over the last month (260.33 on 4/15 → 265.74 on 5/15), and the 200 SMA has risen in lockstep (250.77 → 258.43). This is trend *confirmation*, not a fresh crossover signal.
- **Extension is the risk.** At +12.9% above the 50 SMA and +16.1% above the 200 SMA, the stock is stretched far from its mean. Historically such separation tends to resolve either through a pause/consolidation (time) or a pullback (price). Trend-followers can stay long, but new buyers at $300 are paying a premium to every average.

**Interpretation:** The trend structure is unambiguously bullish, but entries at current levels carry elevated pullback risk back toward the 10 EMA (291.35) first, then the VWMA (~285).

---

## 3. Momentum

**Selected indicators:** `macd`, `rsi`

**MACD (trend momentum):**
- MACD line = **9.51**, Signal = **7.73**, Histogram = **+1.77**.
- The MACD line is above its signal line (bullish), and the histogram is *positive and widening* — momentum is still accelerating, not decaying.
- The MACD line has risen steadily and steeply: 0.96 (4/15) → 4.35 (5/1) → 9.51 (5/15). There has been no bearish crossover; the uptrend has uninterrupted momentum confirmation.
- **Caveat:** a MACD reading of 9.51 near multi-month highs means any slowdown in the rate of advance will show up quickly as histogram contraction — an early warning to watch.

**RSI (overbought/oversold momentum):**
- RSI = **76.02**, up from 58.75 on 4/30 and 66.44 on 5/1. RSI has now held **above 70 for roughly five consecutive sessions** (5/8 through 5/15).
- This is *overbought* by the classic 70 threshold, but in a strong trend RSI can stay pinned in the 70s without an immediate reversal. The relevant read is not "sell because overbought" but "trend is strong yet increasingly extended."
- Watch for **bearish divergence** (price making higher highs while RSI makes lower highs) and for an RSI break back below 70 — either would be the first concrete momentum-decay signal.

**Interpretation:** Momentum is bullish but mature. MACD says the trend is intact; RSI says the easy part of the move may be behind us.

---

## 4. Volatility & Risk

**Selected indicators:** `boll_ub`, `atr`

**Bollinger Bands:**
- Middle (20 SMA basis) = **281.11**; Upper = **304.51**; Lower = **257.72**.
- Close of 299.97 sits **~81% of the way from the middle to the upper band** — in the upper half, pressing toward the upper band but not yet riding it (no blow-off).
- The bands are **expanding**: upper band rose from 264.53 (4/15) to 304.51 (5/15). Expanding bands with price in the upper half = a *volatility breakout / trend leg*, which typically favors continuation while it lasts but also marks a higher-volatility environment.
- The upper band at ~$304.51 is a natural ceiling/breakout reference; a decisive close above it would signal an even stronger thrust, while failure near it often precedes mean-reversion toward the 281 middle band.

**ATR:**
- ATR = **6.23**, up from ~5.86 mid-April. Annualized/percentage: **6.23 / 299.97 ≈ 2.1% of price per day**.
- Elevated-but-not-extreme volatility. Practical use: a 1×ATR stop below the current close is ~$293.7; a 2×ATR stop is ~$287.5 — the latter sits near the 10 EMA and VWMA, a logical "if the trend is real, it shouldn't reach here" invalidation zone.

**Interpretation:** Volatility is expanding in the direction of the trend, which supports the bullish case but also widens the appropriate stop distance and shrinks prudent position size.

---

## 5. Volume Confirmation

**Selected indicator:** `vwma` (+ raw volume from OHLCV)

- **VWMA = 284.95.** Price (299.97) is **+5.27% above** the volume-weighted average, confirming that recent gains have occurred on meaningful volume — the advance is volume-supported, not a thin drift.
- Both VWMA and the 10 EMA are rising together, and price holding above both reinforces that buyers are in control.
- **Raw volume context:** the breakout was accompanied by strong participation — 79.9M shares on 5/1 (the gap-up day), 58.3M on 5/6, 52.7M on 5/8, 52.7M on 5/13, and 54.9M on 5/15. This level of activity on up-days supports accumulation rather than distribution.
- **Caveat:** VWMA can be skewed by volume spikes; here the consistency of elevated volume across multiple sessions (not a single outlier) makes the signal more credible.

---

## 6. The Move in Context (dates & prices from tool output)

- The stock bottomed on a closing basis at **$246.03 (2026-01-20)** and **$246.98 (2026-01-21)** following a January pullback.
- From there it rebuilt, then launched: close **$270.87 on 2026-04-30** → close **$299.97 on 2026-05-15**, a gain of **+$29.10 (+10.74%)** in eleven trading sessions.
- A notable **gap-up** occurred on **2026-05-01** (prior close 270.87 → open 278.36 → close 279.64).
- On 2026-05-13 and 2026-05-15 the intraday high reached **300.66** and **302.94** respectively, i.e., the stock is probing the $300–303 zone for the first time in this leg.

*These are reported as factual tool-output observations, not as validated support/resistance bounces.*

---

## 7. Actionable Insights

**For trend-followers / existing longs:**
- Stay with the trend. All trend and momentum filters (10 EMA > 50 SMA > 200 SMA, MACD > signal, price > VWMA) are bullish. Nothing in the tool output signals a trend reversal yet.
- **Trail stops** rather than exit outright. A reference could be below the 10 EMA (~291) or a 2×ATR band (~287), which also aligns with the VWMA (~285). This protects gains while allowing the trend to breathe.
- The first momentum warning would be **MACD histogram contraction toward zero** or **RSI dropping back below 70**.

**For prospective buyers / adding:**
- Chasing at ~$300 means buying **+16% above the 200 SMA with RSI at 76** — poor asymmetry. Prefer to wait for either (a) a pullback that holds the 10 EMA (~291) or VWMA (~285) zone, or (b) a decisive breakout close above the upper Bollinger band (~304.5) that confirms a fresh volatility thrust.
- If entering now, size down given ATR ≈ $6.23 and place invalidation at a level a normal 1–2×ATR wiggle won't hit (~$287–294).

**For short-sellers / contrarians:**
- Nothing here supports shorting a stock in a stacked bullish trend with rising MACD. The only contrarian case is *fade-the-extension* near the upper band (~$304.5), and even that is high-risk until RSI divergence or a MACD histogram rollover appears.

**Key levels to monitor (indicator-derived references):**
- **Resistance/breakout trigger:** ~$302.94 (5/15 intraday high), ~$304.51 (upper Bollinger band).
- **First dynamic support:** ~$291.35 (10 EMA).
- **Secondary support/trend-integrity line:** ~$284.95 (VWMA) and ~$281.11 (Bollinger middle).
- **Structural trend floor:** ~$265.74 (50 SMA), with the ~$258.43 (200 SMA) well below.

---

## 8. Risks / Considerations

- **Overbought & extended:** RSI 76 + 16% above the 200 SMA raise the odds of a sharp mean-reversion move without warning.
- **Earnings/event gap risk:** A one-day ATR move is ~$6; the stock has recently demonstrated it can gap several points overnight (e.g., the 5/1 gap). Stops can be jumped.
- **Momentum dependence:** The bullish thesis rests on continued MACD expansion; the histogram (1.77) is the leading edge to watch for decay.
- **Rising volatility cuts both ways:** Expanding Bollinger bands support continuation *until* they mark exhaustion.

---

## 9. Key Points Summary Table

| Category | Indicator | Latest Value (2026-05-15) | Signal / Read | Implication |
|---|---|---:|---|---|
| Trend | Close price | $299.97 | Uptrend, near highs | Bullish, extended |
| Trend | close_10_ema | 291.35 | Price +2.96% above | First dynamic support |
| Trend | close_50_sma | 265.74 | Price +12.88% above, rising | Medium-term trend up; extended |
| Trend | close_200_sma | 258.43 | Price +16.08% above, rising | Long-term uptrend confirmed; golden-cross regime |
| Momentum | macd | 9.51 (signal 7.73) | Above signal, histogram +1.77 | Bullish, accelerating, no crossover |
| Momentum | rsi | 76.02 | Overbought (>70 for ~5 sessions) | Strong but stretched; watch for divergence |
| Volatility | boll_ub | 304.51 | Price ~81% to upper band | Breakout zone / near-term ceiling |
| Volatility | atr | 6.23 (~2.1% of price) | Expanding | Wider stops, smaller size |
| Volume | vwma | 284.95 | Price +5.27% above, rising | Volume-confirmed advance |
| Volume | Raw volume | 54.86M on 5/15 | Elevated on up-days | Accumulation, not distribution |

---

**Overall technical bias: BULLISH TREND, EXTENDED CONDITION.** The weight of evidence (stacked rising MAs, positive/expanding MACD, price above VWMA, volume confirmation) favors continued upside, but RSI overbought and the large gap above the 200 SMA argue that *new* entries at $300 carry poor risk/reward. Preferred approaches: hold/trail for existing longs; wait for a pullback into the 291/285 zone or a confirmed close above ~304.5 for fresh entries.

FINAL TRANSACTION PROPOSAL: **HOLD**