# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date:** 2025-11-14 | **Exchange:** NMS | **Sector:** Technology / Semiconductors

*All price levels and indicator values below are drawn from the verified market snapshot and confirmed tool outputs for 2025-11-14. No forward-looking or unverified claims are made.*

---

## 1. Market Context & Recent Price Behavior

NVDA has just come off a **sharp late-October vertical advance followed by a two-week pullback**. The relevant verified closes tell the story:

- A long basing/choppy phase from early September through late October, oscillating mostly between ~166 and ~192 (e.g., close 166.61 on 2025-09-05; close 192.11 on 2025-10-09).
- A breakout leg in the final days of October: closes of **191.03 (10-27), 200.55 (10-28), 206.55 (10-29), 202.41 (10-30), 202.01 (10-31), 206.39 (11-03)**. The 2025-10-29 session printed an intraday high of **211.68** on elevated volume of **308.8M** shares (and 2025-10-28 saw 298.0M shares).
- A subsequent distribution/pullback: closes slid to **198.22 (11-04), 194.74 (11-05), 187.63 (11-06), 187.70 (11-07), 192.70 (11-11), 186.41 (11-13)**, with a **rebound to 189.72 on 2025-11-14**.

The 2025-11-14 candle is notable: it opened at **182.42**, dipped to a low of **180.15**, then closed at **189.72** — near the top of its range (high 190.55). That is a wide-range recovery day, but it occurred on volume of 186.6M, *below* the late-October spike volumes.

Net move from the 2025-10-29 peak close (206.55) to the 2025-11-13 pullback close (186.41) is **−9.8%**; the 2025-11-14 rebound recovers part of that to −8.2% from the peak. (Computed from the concrete closes above.)

---

## 2. Selected Indicators (8) and Rationale

I selected a **complementary, non-redundant** set spanning trend, momentum, volatility, and volume — deliberately avoiding duplicate signals (e.g., no RSI + StochRSI pairing):

| # | Indicator | Value (2025-11-14) | Role in this context |
|---|---|---|---|
| 1 | **close_200_sma** | 150.82 | Strategic long-term trend anchor |
| 2 | **close_50_sma** | 185.16 | Medium-term trend + nearest dynamic support |
| 3 | **close_10_ema** | 192.11 | Short-term momentum / immediate resistance |
| 4 | **macd** | 1.70 | Momentum/trend-change detection |
| 5 | **macds** | 3.01 | Crossover trigger confirmation |
| 6 | **rsi** | 49.42 | Overbought/oversold + divergence gauge |
| 7 | **atr** | 7.71 | Volatility sizing & stop placement |
| 8 | **vwma** | 196.39 | Volume-weighted trend confirmation |

*(Bollinger values — mid 192.41, upper 209.44, lower 175.38 — are referenced from the verified snapshot for price-location context, not counted as a separate selection.)*

---

## 3. Trend Analysis

### Long-term: firmly bullish
The **200 SMA is at 150.82 and rising monotonically** — from 139.79 on 2025-09-15 to 150.82 on 2025-11-14, roughly +0.32/day. Price at 189.72 sits **~25.8% above** the 200 SMA. This is a textbook sustained uptrend; strategic longs remain structurally supported.

### Medium-term: bullish but flattening
The **50 SMA is at 185.16**, also rising (from 174.06 on 2025-09-15). Price is **~2.46% above** it. Critically, **50 SMA (185.16) > 200 SMA (150.82)** — bullish MA alignment, no death-cross risk. However, the 50 SMA has flattened recently (183.49 on 11-10 → 185.16 on 11-14), consistent with the choppy base.

### Short-term: corrective / momentum fading
The **10 EMA is at 192.11 and has been declining** (from ~196.95 on 2025-11-04 to 192.11 on 2025-11-14). Price (189.72) closed **below the 10 EMA**, and also below the Bollinger middle (20 SMA = 192.41). This is the key near-term pivot: **price is trapped between the 50 SMA (~185 support zone) and the 10 EMA / 20 SMA (~192 resistance zone).**

---

## 4. Momentum Analysis

### MACD — bearish crossover in progress
- **macd = 1.70, signal = 3.01, histogram = −1.32** (verified).
- The MACD line **crossed below its signal on or about 2025-11-05/11-06** (macd 5.234 vs signal 4.348 on 11-05 → macd 4.216 vs signal 4.322 on 11-06) and the gap has widened since. Both lines are declining from their early-November peaks (macd peaked near 5.93 on 2025-11-03; signal near 4.35 on 2025-11-05).
- Interpretation: **short-term momentum has turned negative**, but the MACD remains *above zero* (1.70), so this is a cooling-off within a larger uptrend rather than a confirmed downtrend signal.

### RSI — perfectly neutral
- **RSI = 49.42**, essentially mid-range. It peaked at **73.13 on 2025-10-29** (overbought at the top) and bottomed at **46.41 on 2025-11-13** before ticking back up. 
- There is **no oversold condition** and **no bullish divergence** evident in the tool data; RSI simply reset from overbought to neutral, meaning the pullback has relieved froth without triggering a reversal signal.

---

## 5. Volatility Analysis (ATR)

- **ATR = 7.71**, and it is **expanding markedly**: from 5.39 on 2025-10-24 to 7.71 on 2025-11-14 (+43%). This reflects the violent late-October rally and the equally sharp November reversal.
- Practical implications:
  - A daily swing of ~$7.7 is now normal. Stops tighter than ~$8–10 around entry are prone to noise-based failure.
  - The Bollinger band width (209.44 − 175.38 = **34.06**, ~18% of price) confirms a high-volatility regime.
  - **Position sizing should be reduced** relative to a low-ATR regime to keep per-trade risk constant.

---

## 6. Volume Analysis (VWMA)

- **VWMA = 196.39**, which is **above the current price (189.72)** and above both the 50 SMA and the Bollinger middle. 
- Because VWMA weights by volume, its position *above* spot price indicates that **the bulk of recent volume transacted at higher prices (~194–197)** — i.e., recent buyers are, on average, underwater, a sign of near-term distributive/supply pressure.
- VWMA did continue rising through the pullback (185.74 on 10-28 → 196.39 on 11-14), but at a decelerating pace. For the trend to reassert, price would ideally need to **reclaim the VWMA (~196)** to flip recent volume-weighted participants back to profit.

---

## 7. Actionable Insights & Scenarios

**Current posture:** A structurally strong long-term uptrend in a **short-term corrective consolidation** with elevated volatility and neutral-to-soft momentum. Price is mid-range between defined support and resistance.

**Key levels (from verified tool data):**
- **Support zone 1:** 50 SMA **~185.16** (dynamic).
- **Support zone 2:** **~179–180** — an area repeatedly traded (closes 179.60 on 10-14, 179.40 on 10-15, 179.85 on 10-22; intraday low 178.48 on 11-07; 11-14 low 180.15).
- **Lower band:** Bollinger lower **~175.38** as a deeper volatility floor.
- **Resistance zone 1:** **~192** — the confluence of 10 EMA (192.11) and Bollinger middle/20 SMA (192.41).
- **Resistance zone 2:** **~196–198** (VWMA 196.39 and the 198 area).
- **Resistance zone 3:** **~206** — the recent peak closes (206.55 on 10-29, 206.39 on 11-03), with the 211.68 intraday high above it.

**Scenario playbook:**
1. **Bullish continuation (needs confirmation):** A daily close **back above ~192** (reclaiming the 10 EMA / 20 SMA) would signal the short-term corrective phase is ending. A follow-through close above the **VWMA ~196** would flip volume-weighted sentiment and open the path back toward **~206** and the **211.68** high. The unresolved **MACD bearish crossover** (histogram −1.32) is the main caveat — momentum would need to re-cross.
2. **Consolidation/base case:** Choppy trade **between ~185 (50 SMA) and ~192 (10 EMA/20 SMA)**. RSI at 49 and neutral Bollinger positioning support a range-bound interpretation until a decisive breakout on expanding volume.
3. **Bearish risk:** A decisive close **below the 50 SMA (~185)** with rising volume would expose the **~179–180** shelf and potentially the **~175.38** lower band. A break there would be the first serious medium-term trend challenge, though the 200 SMA at 150.82 remains far below.

**Risk management:** With ATR at 7.71, use volatility-scaled stops. Consider sizing so that a ~1.5×ATR (~$11.6) adverse move equals the maximum acceptable per-trade loss, and reduce position size versus a low-volatility regime.

---

## 8. Summary Table

| Dimension | Indicator | Value (11-14) | Signal | Implication |
|---|---|---|---|---|
| Long-term trend | close_200_sma | 150.82 | **Bullish** | Price +25.8% above rising 200 SMA |
| Medium-term trend | close_50_sma | 185.16 | **Bullish/neutral** | Price ~2.5% above; acts as nearest support |
| Short-term trend | close_10_ema | 192.11 | **Bearish** | Price (189.72) below falling 10 EMA = immediate resistance |
| Momentum | macd | 1.70 | **Bearish** | Declining; below zero-crossout watch |
| Momentum trigger | macds | 3.01 | **Bearish** | MACD crossed below signal ~11-05/11-06 |
| Momentum strength | macdh | −1.32 | **Bearish** | Negative & widening gap |
| Overbought/oversold | rsi | 49.42 | **Neutral** | Reset from 73.1 (10-29) peak; no divergence |
| Volatility | atr | 7.71 | **Expanding** | +43% since 10-24; wider stops, smaller size |
| Volume trend | vwma | 196.39 | **Soft bearish** | Above price → recent volume-weighted buyers underwater |
| Band context | boll_ub / boll / boll_lb | 209.44 / 192.41 / 175.38 | **Mid-range** | Price (189.72) below mid-band, above lower |
| Price structure | Close 189.72 | — | **Rebound day** | Opened 182.42, low 180.15, closed near high 190.55 |

**Bottom line:** NVDA remains in a powerful longer-term uptrend (well above a rising 200 SMA) but is working through a **short-term corrective consolidation** characterized by a bearish MACD crossover, a price tag below the 10 EMA/20 SMA/VWMA, neutral RSI, and **expanding volatility**. The 2025-11-14 rebound off the ~180 low is encouraging but unconfirmed. The decisive near-term gates are a **reclaim of ~192** (bullish) versus a **break of ~185** (bearish), with the **~179–180** shelf and **~175.38** lower band as deeper supports and **~196 → ~206 → 211.68** as overhead targets.

*Note: Snapshot values and get_indicators outputs were cross-checked and are consistent (e.g., close_10_ema 192.11, RSI 49.42, MACD 1.70/3.01/−1.32, ATR 7.71). No discrepant figures were found.*