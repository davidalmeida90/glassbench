# INTC (Intel Corporation) — Technical Analysis Report
**Analysis date:** 2026-05-15 | **Exchange:** NMS | **Sector:** Technology / Semiconductors

*Source of truth: the verified market snapshot for INTC (latest row 2026-05-15). All OHLCV and indicator values below are drawn from that snapshot and from the indicator tool outputs. No discrepancy was found between the raw OHLCV pull and the verified snapshot (both show 2026-05-15: O 109.79 / H 110.57 / L 105.02 / C 108.77 / Vol 135,206,000).*

---

## 1. The market context in one line
INTC is in a violent, parabolic **primary uptrend that has just stalled** at a short-term top. Price has rocketed from the mid-40s in mid-March to a 2026-05-11 intraday high of **132.75**, and is now **~18% off that high** after four consecutive down sessions into 2026-05-15's close of **108.77**. The regime is best described as *extended, high-volatility, and rolling over on the short timeframe while structurally intact on the longer timeframes.*

---

## 2. Indicators selected (8) and why
I chose a deliberately **non-redundant, multi-dimensional** set. Because the dominant feature right now is a decelerating parabolic advance, I weighted toward (a) trend context across three horizons, (b) momentum *rate-of-change* (crossover risk), (c) the statistical overbought boundary, and (d) volatility for risk sizing.

| Category | Indicator | Rationale in this context |
|---|---|---|
| Moving Averages | **close_10_ema** | The most responsive gauge — price has just **lost** this average (108.77 vs 111.65), the first short-term momentum failure signal. |
| Moving Averages | **close_50_sma** | Medium-term trend anchor; confirms the trend's health and gives a "distance-from-trend" extension reading (69.50). |
| Moving Averages | **close_200_sma** | Strategic long-term benchmark (44.79) and confirms a structural uptrend (no death-cross risk). |
| MACD | **macd** | Momentum magnitude and direction of the fast line (15.00) — still positive but declining. |
| MACD | **macds** | Signal line (14.89) — needed to judge the **imminent bearish crossover** (gap only +0.11). |
| Momentum | **rsi** | Overbought/oversold + divergence engine (62.25, cooling fast from 86+). |
| Volatility | **boll_ub** | Statistical overbought boundary (139.46); shows how far the extreme runs can stretch. |
| Volatility | **atr** | Absolute volatility (7.73) for stop placement and position sizing — critical in a ~7%/day range regime. |

*Supplementary (retrieved but not among the core 8): **vwma** (107.78) — used as a volume-weighted trend cross-check; price is only marginally above it, a notable "volume-weighted support" line.*

---

## 3. Trend analysis (multi-timeframe)

**Long-term (200 SMA = 44.79): structurally bullish and massively extended.**
Price (108.77) sits ~142.8% above the 200 SMA (108.77 − 44.79 = 64.0 points). The 200 SMA is rising steadily (44.79 on 05-15 vs 33.69 on 03-16), confirming a genuine, broad uptrend — not a dead-cat. There is no structural threat to the long-term trend at current levels.

**Medium-term (50 SMA = 69.50): bullish but dangerously stretched.**
Price is ~56.5% above the 50 SMA (108.77 − 69.50). The 50 SMA itself is accelerating upward (69.50 vs 46.18 on 03-16), reflecting the ferocious recent advance. When price travels this far above its mean, mean-reversion risk rises sharply even within an uptrend.

**Short-term (10 EMA = 111.65): the first crack.**
On 2026-05-15, INTC closed at **108.77, below the 10 EMA of 111.65** — the first close under the short-term average in this leg. The 10 EMA had been riding the advance (`83.81` on 05-01 → `107.05` on 05-11 → `111.65` on 05-15). Losing it signals that the immediate buy-the-dip dynamic has flipped to sell-the-rally.

**Trend sequencing (golden-cross structure):** 10 EMA (111.65) > 50 SMA (69.50) > 200 SMA (44.79), a textbook bullish stack, but the 10 EMA has started to curl (111.65 on 05-15 vs 112.29 on 05-14) — the first lower short-term reading, consistent with a momentum peak.

---

## 4. Momentum analysis

**MACD (15.00) vs Signal (14.89) — a bearish crossover is imminent.**
The MACD histogram (macd − signal) has collapsed:
- 2026-05-12: +3.14
- 2026-05-13: +2.40
- 2026-05-14: +1.40
- 2026-05-15: **+0.11**

The MACD line is still (just) above its signal, so the formal crossover has *not* yet occurred — but the histogram is at the razor's edge. Two more down sessions would likely flip MACD below signal, a classic trend-change trigger. Note the MACD line itself has begun to roll from its 05-12 peak of 17.05 down to 15.00, while the signal line keeps rising (13.91 → 14.89), which is exactly how a crossover forms.

**RSI (62.25) — sharp cooling from extreme overbought.**
RSI peaked at **87.48 on 2026-05-01** and registered **86.11 on 2026-05-11** — deeply overbought readings characteristic of a blow-off. Over the last four sessions it fell hard: 86.11 (05-11) → 75.14 (05-12) → 74.77 (05-13) → 69.71 (05-14) → **62.25 (05-15)**. This is a very fast momentum decompression (−24 RSI points in four sessions). Importantly, RSI at 62 is **not yet oversold** — there is room to fall further before a mean-reversion bounce becomes high-probability, and the speed of the decline argues the pullback is not finished maturing.

---

## 5. Volatility analysis

**ATR (7.73) — volatility has tripled and is still expanding.**
ATR has climbed from ~2.5–3.1 in late March/early April to **7.73 on 05-15** — a ~2.5–3x expansion. On a ~108 price, that's an average true range of roughly **7% of price per day**. ATR is still *rising* (6.89 on 05-11 → 7.48 on 05-14 → 7.73 on 05-15), meaning volatility is not yet contracting; the down-move is occurring on expanding range, a bearish texture.

**Bollinger Upper Band (139.46) with Middle (boll = 97.57).**
The bands are extraordinarily wide (upper 139.46, lower 55.68 → a full 83.8-point width), a direct consequence of the parabolic move. Position within the band (%B) is **~0.63** — price is *above the middle band (97.57)* but well below the upper band. In a healthy trend, price rides the upper band; the fact that it has dropped to ~63% of the band, and the upper band (139.46) is *rising* while price *falls*, is a classic warning of an over-extension unwinding. The middle band (97.57) is the natural first volatility-based downside magnet.

---

## 6. Volume analysis (VWMA)

**VWMA = 107.78; price (108.77) is barely above it.**
The volume-weighted average price is a volume-adjusted trend line, and it has risen strongly (79.04 on 05-01 → 107.78 on 05-15). Price closing essentially *on top of* VWMA (a mere ~1 point above) tells us the recent buying was heavily concentrated at these elevated levels — i.e., recent buyers are now roughly at break-even. A decisive break below VWMA would put that cohort underwater and tends to accelerate selling. Recent volume confirms unusual participation: 281.4M on 04-24 and 235.1M on 04-29 during the up-thrust; 135.2M on 05-15's down day — elevated but not a climactic capitulation, leaving room for further downside.

---

## 7. Key levels (tool-supported)

**Upside / resistance:**
- **111.65** — 10 EMA (immediate reclaim level)
- **115.93** — 05-14 close; **120.29–120.61** — 05-12/13 congestion
- **124.92** — 05-08 close; **129.44** — 05-11 closing high
- **132.75** — 05-11 intraday high; **139.46** — rising Bollinger upper band

**Downside / support:**
- **107.78** — VWMA (in-play now)
- **105.02** — 05-15 intraday low (first line)
- **99.62** — 05-01 close; **95.78** — 05-04 close (prior congestion shelf)
- **97.57** — Bollinger middle band (volatility mean)
- **82.20** — 04-24 gap-up open (major air-pocket reference)

---

## 8. Actionable insights & scenarios

**Base case (short-term corrective within a larger uptrend):** Momentum is decaying (MACD histogram +0.11, RSI −24 pts in four sessions) and price has lost both the 10 EMA and, effectively, is testing VWMA. Until RSI stabilizes and MACD re-expands, rallies should be treated as suspect.

- **Bullish trigger:** A close back **above the 10 EMA (111.65)** with a re-expanding MACD histogram and RSI turning up from ~60 would argue the pullback is a bull-flag and re-open the 120/129 path. Confirmation improves if VWMA holds and advances on strong volume.
- **Bearish trigger:** A daily close **below VWMA (107.78) and the 05-15 low (105.02)** confirms distribution; next objectives are the 99.62/95.78 shelf and the Bollinger middle at 97.57, with the 82.20 gap area as the deeper magnet if momentum breaks down.

**Risk management (given ATR = 7.73):**
- Position sizing must account for ~7%/day swings — size roughly a third to a half of a normal-volatility position for the same dollar risk.
- A volatility-aware stop on a long might be placed ~1.5×ATR (~11.6 points) below entry; a short-side stop could sit just above the reclaimed 10 EMA/VWMA. Fixed-tight stops in a 7%-ATR name invite whipsaw.

**Caveats / what would change the read:**
- RSI at 62 is *not* oversold — don't assume a bounce is imminent from "overbought unwound" alone.
- The MACD bearish crossover has *not yet occurred* — calling a trend change now would be anticipatory; the histogram edge (+0.11) is the concrete trigger to watch.
- Long-term trend is intact (price >50 SMA >200 SMA); this is currently a **correction risk**, not a confirmed reversal. A single strong session could repair the short-term damage.

---

## 9. Summary table

| Dimension | Indicator | Value (2026-05-15) | Signal | Interpretation |
|---|---|---|---|---|
| Price | Close | 108.77 | Pullback | −16.0% from 05-11 close (129.44); −18.1% from 05-11 intraday high (132.75) |
| Short trend | close_10_ema | 111.65 | **Bearish** | Price closed *below* it — first short-term momentum break |
| Medium trend | close_50_sma | 69.50 | Bullish (extended) | Price ~56.5% above; mean-reversion risk elevated |
| Long trend | close_200_sma | 44.79 | Bullish | Price ~142.8% above; structural uptrend intact |
| Momentum | macd | 15.00 | Weakening | Rolling over from 05-12 peak (17.05) |
| Momentum | macds | 14.89 | **Caution** | Signal rising toward MACD; gap only +0.11 → crossover imminent |
| Momentum | rsi | 62.25 | Cooling | Down from 87.48 (05-01)/86.11 (05-11); not yet oversold |
| Volatility | boll_ub | 139.46 | Context | Bands very wide; price at ~63% of band (%B) |
| Volatility | atr | 7.73 | **High/rising** | ~7% daily range; still expanding — bearish texture |
| Volume | vwma (supp.) | 107.78 | Neutral/bearish | Price barely above volume-weighted trend; loss = downside trigger |

**Bottom line:** INTC remains in a powerful long-term uptrend, but the short-term tape has clearly peaked and is in a fast, high-volatility correction. The two concrete decision points are: (1) **reclaim 111.65 (10 EMA)** to restore the bullish case, or (2) **lose 107.78 (VWMA) / 105.02 (05-15 low)** to confirm a deeper mean-reversion toward 97–100. The MACD histogram (+0.11) is the single cleanest early-warning gauge to monitor.