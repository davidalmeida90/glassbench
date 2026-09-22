# INTC (Intel Corporation) — Technical Analysis Report
**Analysis date: 2026-02-13 | Exchange: NMS | Sector: Technology / Semiconductors**

## Source-of-truth snapshot (verified 2026-02-13)

| Field | Value |
|---|---:|
| Open / High / Low / Close | 45.76 / 47.69 / 44.97 / **46.79** |
| Volume | 69,740,400 |
| close_10_ema | 47.83 |
| close_50_sma | 43.30 |
| close_200_sma | 31.24 |
| rsi | 50.67 |
| boll / boll_ub / boll_lb | 48.20 / 53.95 / 42.44 |
| macd / macds / macdh | 1.20 / 1.72 / −0.53 |
| atr | 3.16 |

No conflicts were found between the raw OHLCV data and the verified snapshot; the two agree on the 2026-02-13 row and all indicator values used below.

---

## 1. Indicators selected and rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume:

1. **close_10_ema** — captures the short-term swing state (is the pullback accelerating or stabilizing?).
2. **close_50_sma** — the medium-term trend and the primary dynamic support zone in this correction.
3. **close_200_sma** — the strategic trend anchor; confirms whether the multi-quarter bull leg is intact.
4. **macd** — measures the momentum engine; used with the signal line for crossover timing.
5. **macds** — the crossover trigger that confirms trend inflection (MACD vs. signal).
6. **rsi** — momentum oscillator to gauge overbought/oversold and, critically, **divergence**.
7. **atr** — the risk unit for stops and position sizing given the outsized recent volatility.
8. **vwma** — volume-weighted confirmation of whether buyers or sellers "own" recent price.

Together these avoid redundancy (no two momentum oscillators, no duplicate MA logic) while covering all four decision dimensions.

---

## 2. Trend structure: macro bull, micro correction

**The primary trend is unambiguously up.** As of 2026-02-13:
- Price (46.79) sits **~49.8% above the 200 SMA (31.24)** — computed from verified values (46.79 vs 31.24).
- The 200 SMA is **rising steadily**: 27.60 on 2026-01-05 → 30.71 on 2026-02-09 → 31.24 on 2026-02-13. A climbing long-term average means higher lows are still being printed on a strategic horizon.
- The 50 SMA (43.30) is **well above the 200 SMA (31.24)** — a bullish (golden-cross alignment) configuration — and the 50 SMA is also rising: 38.06 (2026-01-05) → 42.74 (2026-02-09) → 43.30 (2026-02-13).
- Price remains **~8.1% above the 50 SMA** (46.79 vs 43.30), so even after the recent drop, medium-term buyers are still in profit.

**But the short-term trend has rolled over.** Price (46.79) is **below the 10 EMA (47.83)**, below the **Bollinger middle band (48.20)**, and below the **VWMA (48.05)**. This three-way cluster at ~47.8–48.2 is now the near-term ceiling the bulls must reclaim.

**The story in price action:** INTC staged a parabolic advance from roughly $36 (late Dec 2025) to a closing peak of **54.32 on 2026-01-22** (intraday high 54.60 the same day). That top was followed by a violent two-day collapse — closing **45.07 on 2026-01-23** and **42.49 on 2026-01-26**. A rebound then carried to **50.59 on 2026-02-06**, but the stock has since faded to 46.79 on 2026-02-13. The result is a classic **potential lower-high / double-top formation**: the January peak (54.32) and the February rebound peak (50.59) define the range's upper boundary.

---

## 3. Momentum: a confirmed bearish turn with a divergence

**MACD has crossed bearishly.** The MACD line has fallen sharply — from **3.67 on 2026-01-22** to **1.20 on 2026-02-13** — an extremely fast decay. The signal line (1.72) now sits **above** the MACD line, producing a **negative histogram (−0.53)**. Tracing the exact cross: on 2026-01-26 MACD (2.59) was still marginally above signal (2.58), but by **2026-01-27 MACD (2.20) had dropped below signal (2.51)** and has stayed below ever since. So the bearish MACD crossover is now more than two weeks old and remains intact — short-term momentum is still net negative.

**RSI shows a textbook bearish divergence and is now neutral.** RSI spiked to **76.9 on 2026-01-22** at the price peak, then — at the **2026-02-06 lower price high (50.59)** — RSI reached only **59.7**, a clear lower momentum peak against the January spike. That divergence flagged the rebound as corrective rather than impulsive. RSI has since cooled to **50.67 (2026-02-13)**, dead-neutral. This is important: there is **no oversold edge** here. In a stock that can move 15–20% in a day, a mid-50s RSI means plenty of room to fall before complacency is flushed.

---

## 4. Volatility and volume: wide bands, heavy distribution

**ATR is elevated and still near its recent peak.** ATR sits at **3.16 (2026-02-13)** — about **6.8% of the 46.79 close** — after rising from ~1.71 on 2026-01-06 and peaking at ~3.27 on 2026-02-10. This is extraordinarily high for a large-cap and it directly drives risk management (see below).

**Bollinger Bands are extremely wide**, confirming a high-volatility regime: middle 48.20, upper 53.95, lower 42.44. The band width (~11.5 points, ≈24% of the middle band) reflects the blow-off-and-reversal. Price is below the middle band, leaning toward the lower half but not yet at the lower band.

**VWMA at 48.05 vs. price 46.79** tells us the volume-weighted "average buyer" is slightly underwater — recent selling has been heavier than buying at the margin. Notably, the reversal was accompanied by **massive volume**: 220.6M on 2026-01-21, 190.1M on 2026-01-22, and **294.7M on 2026-01-23** (the down day) — a distribution signature. By contrast, 2026-02-13 volume was a lighter 69.7M.

---

## 5. Actionable interpretation

| Scenario | Trigger / Level | Evidence | Implication |
|---|---|---|---|
| **Bullish reclaim** | Price closes back above **~48.0–48.2** (VWMA 48.05 / BB mid 48.20 / 10 EMA 47.83) | Cluster of 3 indicators; would flip price back above short-term averages | Opens path to **50.5** (Feb 6 high) then **53.95 (BB upper) / 54.32 (Jan 22 peak)** |
| **Neutral / chop** | Price oscillates **44.97–48.20** | RSI 50.67, MACD negative but flattening | Range-trade; no trend edge |
| **Bearish break** | Lose **44.97 (Feb 13 low)** | Would confirm lower-high structure; MACD already < signal | Next supports **43.30 (50 SMA)**, then **42.44 (BB lower) / 42.49 (Jan 26 close, intraday low 42.28)** |
| **Trend invalidation** | Sustained close below **~42.3–42.5** | Breaks the Jan 26 swing low; 50 SMA begins to flatten | Medium-term uptrend at risk; 200 SMA (31.24) becomes the strategic stop-line |

**Risk management (using ATR):** With ATR = 3.16, a conventional 1.5×ATR stop is roughly **4.7 points** — meaning a swing entry near 46.8 should tolerate a stop near **~42.0**, which conveniently aligns with the BB lower band and the January swing low. Position sizes should be scaled **down materially** versus a low-volatility name, because a single day's range has recently exceeded 15%.

**Volume caveat:** The VWMA (48.05) is close to price, so it carries less edge than in a quieter tape; treat it as a *bias filter* (price below VWMA = net seller pressure) rather than a hard signal.

---

## 6. Nuanced summary

INTC is a **high-volatility, high-momentum large-cap in a bull-market correction**. The strategic picture (price ~50% above a rising 200 SMA, 50 SMA above 200 SMA) remains constructive, and the medium-term 50 SMA at 43.30 is still ~8% below price, offering a real cushion. However, the short-term tape is deteriorating: the **MACD bearish crossover (since 2026-01-27)**, the **negative histogram (−0.53)**, the **bearish RSI divergence** at the 2026-02-06 lower high, and price trading **below the 10 EMA, VWMA, and Bollinger mid-band** all argue that the January blow-off top is still being digested. RSI at 50.67 offers **no oversold comfort**.

The decisive levels are clear: **~48.2 overhead** (reclaim = bullish resumption) versus **~45.0/43.3/42.4 below** (break = deeper correction). Traders should respect the elevated ATR via smaller size and wider stops.

---

### Key Points — Markdown Summary Table

| Dimension | Indicator | Latest Value (2026-02-13) | Reading | Signal |
|---|---|---|---|---|
| Long-term trend | close_200_sma | 31.24 (rising) | Price ~49.8% above; strong uptrend | **Bullish (strategic)** |
| Medium-term trend | close_50_sma | 43.30 (rising) | Price ~8.1% above; dynamic support | **Bullish (medium)** |
| Short-term trend | close_10_ema | 47.83 | Price (46.79) below it | **Bearish (short-term)** |
| Momentum (line) | macd | 1.20 (down from 3.67 on 01-22) | Fast decay | **Bearish** |
| Momentum (trigger) | macds | 1.72 | Above MACD → negative histogram | **Bearish crossover (since 01-27)** |
| Momentum (osc.) | rsi | 50.67 | Neutral; bearish divergence at 02-06 lower high | **Neutral / warning** |
| Volatility | atr | 3.16 (~6.8% of price) | Near recent peak (~3.27) | **Elevated risk** |
| Volume | vwma | 48.05 | Price below volume-weighted avg | **Mild bearish** |
| Band context | boll / ub / lb | 48.20 / 53.95 / 42.44 | Price below mid; very wide bands | **High-vol consolidation** |
| Key resistance | 47.8–48.2 → 50.5 → 53.95/54.32 | 10 EMA / VWMA / BB mid cluster | Reclaim needed for upside | **Watch** |
| Key support | 44.97 → 43.30 → 42.44/42.49 | Feb 13 low / 50 SMA / BB lower & Jan 26 low | Break = deeper correction | **Watch** |

*Prepared 2026-02-13. All exact price and indicator values are taken from the verified snapshot; percentages are computed directly from the cited verified values. This is technical analysis, not investment advice.*