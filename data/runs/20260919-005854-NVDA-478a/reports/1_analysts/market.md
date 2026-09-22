# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date:** 2026-02-13 · **Exchange:** NMS · **Sector:** Technology / Semiconductors
**Verified close:** $182.38 (O 187.04 / H 187.06 / L 181.17 / Vol 161,888,000)

> All exact price, OHLCV, and indicator values below are taken from the **verified market snapshot** (latest row 2026-02-13). The `get_indicators` series returned identical latest values (close_50_sma 183.97, close_200_sma 171.26, close_10_ema 184.98, rsi 47.33, macd 0.108, macds 0.028, macdh 0.080, atr 6.40, boll_ub 196.01, boll_lb 173.73) — **no discrepancies to flag**. VWMA (184.91) came only from the indicator tool and is not in the snapshot.

---

## 1. Indicator selection & rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume:

| # | Indicator | Category | Why selected for this context |
|---|-----------|----------|-------------------------------|
| 1 | **close_200_sma** | Trend (long) | NVDA is in a multi-month uptrend; the 200 SMA is the definitive "is the primary trend intact?" filter. |
| 2 | **close_50_sma** | Trend (medium) | Price is **straddling** this line — it's the pivot of the current chop and the natural support/resistance to watch. |
| 3 | **close_10_ema** | Trend (short) | Captures the fast momentum roll-over after the February V-bounce. |
| 4 | **macd** | Momentum | Identifies the fresh (but weak) bullish crossover and its fading thrust. |
| 5 | **rsi** | Momentum oscillator | Independent, bounded momentum gauge — confirms whether the bounce had real strength or was a dead-cat. |
| 6 | **boll_lb** | Volatility | Lower band is the objective "oversold / mean-reversion" reference near the recent lows. |
| 7 | **atr** | Volatility | Sets risk in dollar terms; volatility has expanded, which changes position sizing and stop distance. |
| 8 | **vwma** | Volume | Distinguishes "real" moves from drift; critical given the high-volume sell-off and bounce. |

*(I referenced the Bollinger middle 184.87 and upper band 196.01 from the snapshot for channel context, but kept the formal selection at 8.)*

---

## 2. Price & trend structure

**Long term — intact and bullish.** The 200 SMA at **171.26 is rising steadily** (it climbed from 155.95 on 2025-12-15 to 171.26 on 2026-02-13). Price at 182.38 sits **+6.5% above it**, and the 50 SMA (183.97) remains comfortably above the 200 SMA — a persistent "golden-cross" configuration. Nothing in the tool output suggests the primary uptrend has broken; this is a correction **within** an uptrend, not a reversal of it.

**Medium term — flat / sideways chop.** The 50 SMA has barely moved: 186.18 on 2025-12-15 → 183.97 on 2026-02-13, hovering in a tight 183.1–186.3 band for roughly two months. This is textbook consolidation. The closing price (182.38) is **just below** the 50 SMA (−0.86%), meaning the market is slightly on the wrong side of its own medium-term mean.

**Short term — bouncing then fading.** The 10 EMA rose from 181.63 (2026-02-05) to 185.56 (2026-02-12), but the close on 2026-02-13 (182.38) is **below the 10 EMA (−1.4%)** and the EMA itself ticked down to 184.98. Short-term momentum is turning back down.

**The tape tells a clear V-then-fade story (close basis):**
- Swing high close **192.06 on 2026-01-29**
- Sharp five-session decline to **171.48 on 2026-02-05** (≈ −10.7% close-to-close; intraday low 170.63)
- Strong rebound to **189.61 on 2026-02-11** (≈ +10.6% off the low)
- Rejection back to **182.38 on 2026-02-13**

Net effect: two months of **range-bound action roughly between the low-170s and low-190s**, with the latest upswing now failing at the upper end.

---

## 3. Momentum

**MACD (0.108) vs Signal (0.028), Histogram (0.080).** The MACD line crossed **above** its signal on 2026-02-12 (0.378 vs 0.008) and held on 2026-02-13 — a technically fresh bullish crossover. **But the quality is weak:** both lines are essentially pinned at zero, and the histogram has already peaked and is contracting (0.382 on 2026-02-11 → 0.370 on 2026-02-12 → **0.080 on 2026-02-13**). That decay in the histogram signals the rebound's thrust is already dissipating — a classic "crossover with no follow-through" in a choppy tape.

**RSI (47.33).** Firmly neutral and now back **below the 50 midline**, having fallen from 55.4 (2026-02-09). Notably, RSI only reached **34.3** at the 2026-02-05 low — it never touched the 30 oversold threshold, implying the dip was a momentum wash-out rather than a capitulation. RSI is not confirming either an overbought top or an oversold bounce; it is consistent with sideways distribution.

**Read:** Momentum is neutral-to-softening. There is no momentum edge to trade right now.

---

## 4. Volatility & risk

**ATR = 6.40**, which is **≈3.5% of the $182.38 price** — elevated for a mega-cap and clearly higher than late January (ATR ~5.0 on 2026-01-28). The expansion from ~5.0 to ~6.4 coincided with the February sell-off/bounce.

**Bollinger channel (from snapshot):** Lower **173.73**, Middle **184.87**, Upper **196.01**. Band width = (196.01 − 173.73) / 184.87 ≈ **12.1%** — wide, confirming the elevated-volatility regime. The close (182.38) sits **above the lower band but below the middle**, i.e., in the lower half of the channel — the "weakening, but not yet oversold" zone.

**Risk implication:** With ATR ~6.4, a single day's noise is ±$6. Practical stops should be sized in ATR units (e.g., 1.5×ATR ≈ $9.6; 2×ATR ≈ $12.8) rather than tight fixed points. Position sizes should be **reduced** relative to a low-volatility regime.

---

## 5. Volume confirmation

**VWMA = 184.91, above the close (182.38).** The volume-weighted average price sits **$2.53 (≈1.4%) above spot**, meaning the bulk of recent volume transacted at higher prices — evidence of **overhead supply / distribution** into the recent bounce.

Volume pattern supports the caution: the sell-off days 2026-02-03 (204.0M), 2026-02-04 (207.0M), and 2026-02-05 (206.3M) all printed **above** the typical ~140–160M run-rate, and the bounce peak day 2026-02-06 (231.3M) was the heaviest. Heavy turnover on the decline and rally, followed by the 2026-02-13 pullback on 161.9M (unremarkable), suggests active repositioning rather than quiet accumulation.

---

## 6. Actionable scenarios

**Key reference levels (all from tool output):**

| Level | Value | Source |
|---|---|---|
| Bollinger Upper | 196.01 | snapshot |
| Jan swing-high close | 192.06 (2026-01-29) | price history |
| Feb rebound high close | 189.61 (2026-02-11) | price history |
| **Immediate resistance cluster** | **184–185** | 10 EMA 184.98 / VWMA 184.91 / BB mid 184.87 / 50 SMA 183.97 |
| **Current price** | **182.38** | 2026-02-13 |
| Bollinger Lower | 173.73 | snapshot |
| Feb swing-low close | 171.48 (2026-02-05) | price history |
| 200 SMA / intraday low | 171.26 / 170.63 (2026-02-05) | snapshot / price history |

**Bullish (breakout continuation):**
- Trigger: a **close back above the 184–185 cluster** (10 EMA / VWMA / BB middle / 50 SMA), ideally with expanding volume and VWMA turning up.
- Confirmation: MACD histogram re-expanding, RSI reclaiming >55.
- Objective: first **189–192** (Feb rebound / Jan swing highs), then **196** (Bollinger upper).
- Caveat: this is trading **against** fading short-term momentum, so it is a momentum-breakout trade requiring confirmation, not a dip-buy.

**Bearish (range resolution lower):**
- Trigger: a decisive break of the **173.73 (BB lower) → 171.48 (Feb swing low) → 171.26 (200 SMA)** confluence zone.
- Confirmation: RSI <40/30, MACD rolling back below signal, VWMA turning down.
- Downside: a breach of the 200 SMA would be the first objective technical warning that the multi-month uptrend is at risk.

**Base case (most probable given the tool data):**
- Continued **range chop between roughly 171 and 192**, with 184–185 acting as the pivot. MACD at zero, RSI at 47, and price mid-channel all point to **no trend edge**. Capital preservation and patience are favored over aggressive positioning.

---

## 7. Summary table

| Dimension | Indicator(s) | Value (2026-02-13) | Signal | Interpretation |
|---|---|---|---|---|
| Long-term trend | close_200_sma | 171.26 | **Bullish** | Rising; price +6.5% above — primary uptrend intact |
| Medium-term trend | close_50_sma | 183.97 | **Neutral** | Price slightly (−0.86%) below; flat for ~2 months |
| Short-term trend | close_10_ema | 184.98 | **Bearish tilt** | Price −1.4% below; EMA rolling over |
| Trend alignment | 50 vs 200 SMA | 183.97 vs 171.26 | **Bullish** | Golden-cross gap persists |
| Momentum (MACD) | macd / macds / macdh | 0.108 / 0.028 / 0.080 | **Weak bullish** | Fresh crossover but histogram fading |
| Momentum (oscillator) | rsi | 47.33 | **Neutral** | Below 50; never hit oversold at the low (34.3) |
| Volatility | boll_lb / boll_ub | 173.73 / 196.01 | **Wide bands** | ~12.1% width; price in lower half |
| Volatility/risk | atr | 6.40 (≈3.5%) | **Elevated** | Wider stops, smaller size required |
| Volume | vwma | 184.91 | **Bearish tilt** | Above spot → overhead supply/distribution |
| Range context | — | 171.48 → 192.06 | **Sideways** | Feb V-bounce (+10.6%) now fading |

**Bottom line:** NVDA remains in a **long-term uptrend that is currently digesting a sharp February correction inside a two-month sideways range.** Every short-term gauge (10 EMA, MACD histogram decay, RSI back under 50, VWMA above spot) points to waning momentum and near-term downside risk toward the 184–185 pivot, with the real line-in-the-sand at the **171–174 confluence** (Bollinger lower band, February low, and the rising 200 SMA). The setup is **neutral-to-cautious**: prefer patience, demand confirmation (close above ~185 with volume) before buying breakouts, and size positions to the elevated 3.5% ATR.