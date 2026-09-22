# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date:** 2026-05-15 | **Exchange:** NMS | **Sector:** Technology / Semiconductors
**Verified latest close:** $224.81 (source of truth: verified market snapshot, 2026-05-15)

---

## 1. Indicator Selection Rationale

I chose **8 complementary indicators** spanning trend, momentum, volatility, and volume — deliberately avoiding redundancy (e.g., no RSI + StochRSI pairing; no MACD-signal/histogram double-count):

| Category | Indicators chosen | Why |
|---|---|---|
| Trend (multi-timeframe) | `close_10_ema`, `close_50_sma`, `close_200_sma` | Captures short, medium, and long-term trend structure + cross state |
| Momentum | `macd`, `rsi` | Two independent momentum engines (EMA-difference vs. gain/loss ratio) |
| Volatility / breakout | `boll_ub`, `atr` | Overbought band zones + position-sizing/stop placement |
| Volume confirmation | `vwma` | Validates whether price strength is volume-backed |

---

## 2. Trend Structure — Strong and Aligned Bullish

The moving-average configuration is textbook bullish stacking:

- **Price ($224.81) > 10-EMA ($218.44) > 50-SMA ($192.63) > 200-SMA ($185.53).**
- The **50-SMA sits ~$7.10 above the 200-SMA** (192.63 vs. 185.53), and both are **rising steadily** over the lookback (50-SMA climbed from ~181.7 on Apr 14 to 192.63 by May 15; 200-SMA rose from ~180.7 to 185.53). This is a confirmed, established uptrend — no death-cross risk remotely in view.
- Price is **~16.7% above the 50-SMA** and **~21.2% above the 200-SMA**, which confirms strong trend but also flags meaningful **extension** from the base trend lines.

**Interpretation:** The primary trend is unambiguously up. Buyers control the medium- and long-term structure. However, the wide distance from the 50/200-SMA means the trend is *stretched*, so the risk/reward of fresh entries at current levels is less favorable than on a pullback.

---

## 3. Short-Term Momentum — Powerful Upthrust, Now Cooling

- The **10-EMA has accelerated sharply**, rising from ~181.3 (Apr 13) to 218.44 (May 15) — a near-vertical slope reflecting the April–May rally.
- **MACD = 9.31, above its signal (7.47); histogram = +1.84.** MACD bottomed near -2.48 on Apr 6, crossed above zero around Apr 10–13, and has been positive since. Notably, MACD *dipped* into early May (to ~4.68 on May 5) then **re-accelerated** to 9.31 — a fresh momentum thrust.
- ⚠️ **Lag warning:** MACD is a closing-price-based, smoothed metric. On May 15 the MACD was essentially flat (9.31 vs. 9.22 the prior day) *despite* a large down day, because it hasn't yet absorbed the reversal. Do not read MACD as "confirming" the May 15 strength — it is stale relative to the price action.

---

## 4. Overbought Signal & Upper-Band Rejection (Key Near-Term Event)

This is the most important nuance in the data:

- **RSI reached overbought territory:** 72.13 (May 13) and **76.72 (May 14)**, then **collapsed to 64.66 on May 15**. The drop of ~12 points in a single session reflects a sharp loss of upside momentum.
- **Price pierced above the Bollinger Upper Band on May 14:** close $235.20 vs. upper band of $229.87 (May 14). On **May 15 the close ($224.81) fell back decisively below the upper band ($231.91)**.
- **May 15 was a bearish reversal bar:** Open 229.24, High 230.97, Low 223.73, Close 224.81 — closing near the lower part of its range, down **$10.39 (~4.4%)** from the May 14 close of $235.20.

**Interpretation:** This is a classic **"band ride → rejection"** pattern. Strong trends *can* keep riding the upper band, but the combination of (a) RSI >70, (b) a daily close above the upper band, and (c) an immediate high-volume reversal back below the band is a **near-term exhaustion/consolidation warning**, not necessarily a trend-ending signal.

---

## 5. Volatility — Expanding

- **ATR = 7.48**, up from ~5.0 in mid-April — a clear **volatility expansion** accompanying the rally.
- Recent daily ranges confirm it: May 14 range = 7.22 pts (228.78–236.00); May 15 range = 7.24 pts (223.73–230.97). Both ≈ 1× ATR.
- Rising ATR means **wider stops and smaller position sizes** are warranted.

---

## 6. Volume Confirmation — Strength Backed, But Watch the Down-Volume

- **VWMA = $212.67**, and price ($224.81) sits **above** it — volume-weighted trend confirms the advance.
- Volume on the two most recent sessions was **elevated and roughly equal**: May 14 = 180.78M, May 15 = 180.98M. The fact that a **high-volume day closed sharply lower** (May 15) introduces a mild **distribution/rejection concern** at the highs. It is not yet decisive, but it contrasts with the clean, high-volume up-days earlier in May.

---

## 7. Actionable Insights

1. **Trend bias remains LONG, but do not chase.** Price is extended (~17% above the 50-SMA) and just rejected its upper band. New entries here carry poor near-term risk/reward.
2. **Preferred entry zones on a pullback:**
   - First: **10-EMA ~$218.44** (short-term dynamic support)
   - Second: **VWMA ~$212.67**
   - Deeper: **Bollinger basis ~$209.82**
   These levels are tool-derived and logical pullback magnets; they are *not* validated historical bounce levels.
3. **Risk management:** With ATR = 7.48, a stop ~1.5–2× ATR (roughly **$11–15**) below entry is a reasonable volatility-adjusted buffer. Alternatively, a close below the 10-EMA would be an early momentum-loss warning.
4. **Momentum confirmation to watch:** A **MACD bearish cross** (MACD line crossing below signal) or RSI failing to reclaim ~60 would signal that the pullback is deepening.
5. **Bullish invalidation is distant:** Only a break below the 50-SMA (~$192.63) would challenge the medium-term uptrend; the 200-SMA (~$185.53) is the strategic line in the sand.
6. **Scenario planning:**
   - *Bullish continuation:* RSI resets toward 55–60 and price reclaims >$230 on strong volume → trend resumes.
   - *Consolidation:* Price chops between the 10-EMA (~$218) and upper band (~$232) while RSI cools → healthy digestion.
   - *Deeper pullback:* Loss of the 10-EMA targets VWMA/basis (~$210–213).

---

## 8. Summary Table

| Dimension | Indicator | Value (2026-05-15) | Signal | Note |
|---|---|---|---|---|
| Price | Close | $224.81 | — | Reversed down $10.39 (~4.4%) from May 14 close $235.20 |
| Short trend | close_10_ema | 218.44 | Bullish | Price above; steep rising slope |
| Medium trend | close_50_sma | 192.63 | Bullish | Price ~16.7% above; rising |
| Long trend | close_200_sma | 185.53 | Bullish | 50-SMA > 200-SMA (golden-cross state) |
| Momentum | macd | 9.31 | Bullish (lagging) | Above signal 7.47; has not yet absorbed May 15 drop |
| Momentum | macd signal | 7.47 | Bullish | Histogram +1.84 |
| Momentum | rsi | 64.66 | Cooling | Fell from 76.72 (May 14); was >70 on May 13–14 |
| Volatility | boll_ub | 231.91 | Caution | Price pierced band May 14, fell back below May 15 |
| Volatility | boll (basis) | 209.82 | Support | Mid-band pullback zone |
| Volatility | atr | 7.48 | Expanding | Up from ~5.0 mid-April; widen stops |
| Volume | vwma | 212.67 | Bullish | Price above volume-weighted average |

---

### Bottom Line
NVDA is in a **strong, well-aligned uptrend** (price > 10-EMA > 50-SMA > 200-SMA, all rising; positive MACD; price above VWMA). However, the stock is **short-term extended and just flashed an exhaustion signal** — RSI >70 into an upper-Bollinger-band close, followed by a **high-volume ~4.4% down day** that closed back inside the band. The trend is intact; the *entry* is not attractive at these levels.

**Recommendation: HOLD** existing positions, favor **adding only on pullbacks** toward the 10-EMA (~$218), VWMA (~$213), or Bollinger basis (~$210), and respect ATR-based stops.

FINAL TRANSACTION PROPOSAL: **HOLD**