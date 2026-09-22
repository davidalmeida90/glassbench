# PFE (Pfizer Inc.) — Technical Analysis Report
**Analysis date:** 2026-05-15 | **Exchange:** NYQ | **Sector:** Healthcare / Drug Manufacturers – General

---

## 1. Data Basis & Verification Note

All exact price and indicator claims below are anchored to the **verified market snapshot** for 2026-05-15 (latest trading row used: 2026-05-15), cross-checked against the indicator time-series pulls. No material discrepancies were found between the snapshot and the `get_indicators` series (e.g., `close_50_sma` 26.093 vs. snapshot 26.09; `close_200_sma` 24.5295 vs. snapshot 24.53; `rsi` 36.12, `macd` −0.269, `atr` 0.52 — all consistent).

**Verified OHLCV (2026-05-15):** Open 25.31 | High 25.39 | Low 24.81 | Close **24.89** | Volume 37,110,100

**Important ex-dividend nuance:** The price tape carries a **$0.43 dividend with an ex-date of 2026-05-08** (and a prior $0.43 on 2026-01-23). The 2026-05-07 close of 25.60 → 2026-05-08 close of 25.24 is a −0.36 move — i.e., **roughly the dividend amount**. That single-day "drop" should therefore NOT be read as fresh selling pressure; on a total-return basis the stock was essentially flat that session. This matters for correctly interpreting the recent slope.

---

## 2. Indicator Selection & Rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume — deliberately avoiding redundancy:

| Indicator | Why chosen for this context |
|---|---|
| **close_200_sma** | Long-term trend anchor; PFE is testing this level, making it the pivotal strategic line. |
| **close_50_sma** | Medium-term trend/support-resistance; distinguishes a pullback from a trend break. |
| **close_10_ema** | Fast momentum read for near-term entry/exit timing. |
| **rsi** | Gauges whether the decline is approaching oversold (mean-reversion risk). |
| **macd** | Confirms momentum direction and zero-line/signal crossovers. |
| **boll_ub / boll_lb** | Frame price relative to a volatility envelope; identify extension and band compression. |
| **vwma** | Volume-weighted confirmation — distinguishes "real" selling from noise (especially post-dividend). |

(*ATR from the snapshot is referenced for risk/stop sizing but not double-counted as a selected momentum/volatility signal.*)

---

## 3. Trend Structure

**Long-term (200 SMA): still constructive, but price is barely holding on.**
- `close_200_sma` = **24.53** and has been **rising steadily** (23.76 on 2026-03-16 → 24.53 on 2026-05-15), reflecting the recovery off the late-2025 lows.
- Price (24.89) sits only **~1.5% above** the 200 SMA — a thin margin. This is the single most important line in the report.

**Medium-term (50 SMA): bearish.**
- `close_50_sma` = **26.09** and is **declining** (26.34 on 2026-04-21 → 26.09 on 2026-05-15). Price is **~4.6% below** it.
- The 50 SMA remains **above** the 200 SMA (spread ≈ **1.56**, or ~6.4% of the 200 SMA), so the "golden-cross" regime from the recovery is technically intact — **but the gap is narrowing**, and continued weakness risks a **death cross** (50 crossing below 200).

**Short-term (10 EMA): bearish.**
- `close_10_ema` = **25.39** and **falling** (26.47 on 2026-04-20 → 25.39 on 2026-05-15). Price is **~2.0% below** it.

**Alignment:** Short-term and medium-term structure is **bearish** (price < 10 EMA < 50 SMA), while the long-term structure is **neutral-to-bullish** (price > rising 200 SMA). Net: a **corrective downtrend within a larger base**, currently pressing the last line of long-term defense.

**Trend path in context:** From the 2026-04-01 close of 27.60, PFE has declined to 24.89 by 2026-05-15 — a **~9.8% drawdown** (computed from verified closes), with the 2026-04-02 intraday high of 27.80 marking the swing peak.

---

## 4. Momentum

**RSI(14) = 36.12** — weak but **not yet oversold**.
- The path is decisively lower: 55.5 (2026-04-06) → 53.3 (2026-04-17) → 47.2 (2026-04-24) → 41.5 (2026-05-14) → **36.1 (2026-05-15)**.
- It has not broken 30, so there is **room to fall further** before a classic oversold mean-reversion signal appears. No confirmed bullish divergence: price made a lower low (24.89 vs. 25.24 on 05-08) while RSI also made a lower low (36.1 vs. 39.4) — i.e., **momentum confirms the price decline** rather than diverging from it.

**MACD = −0.269**, below its signal (**−0.23**), with a **negative histogram (−0.04)**.
- MACD peaked around **+0.328 (2026-04-02)** and has trended down since, **crossing below zero around 2026-04-22/23** (+0.005 → −0.043).
- The histogram has been persistently negative; the most recent reading shows **renewed deterioration** (MACD −0.231 on 05-13 → −0.269 on 05-15), i.e., **bearish momentum is re-accelerating** on the latest bar.

---

## 5. Volatility & Price Envelope

**Bollinger Bands (20, 2σ):** `boll` (mid) = **25.65**, `boll_ub` = **26.45**, `boll_lb` = **24.85**.
- The 2026-05-15 close (24.89) sits **essentially on the lower band (24.85)**, and the intraday low (24.81) **pierced below it**. This is a short-term **extension / selling-climax-type signal** that often precedes at least a technical bounce — though in a firm downtrend price can "ride the band."
- **Bandwidth ≈ 6.2%** ((26.45 − 24.85) / 25.65), **narrower** than earlier in April (~8% on 2026-04-02). This is **volatility compression** — noteworthy because a squeeze resolving from a low can produce a sharp directional move.

**ATR = 0.52** (~2.1% of price). This is a moderate absolute tolerance and is the right unit for setting stops (see §7).

---

## 6. Volume Confirmation

**VWMA = 25.52** — price (24.89) is **~2.5% below** the volume-weighted average, confirming that **recent volume has transacted at higher prices and sellers hold the near-term advantage**.
- The 2026-05-15 down day came on **37.1M shares**, elevated versus the immediately prior sessions (e.g., 05-14: 24.1M; 05-12: 26.8M) — a **distribution-leaning** print on the break to a new swing low.
- Caveat: April 28 (58.1M) was the heaviest recent down-volume print; the general character of recent high-volume days has been **downside**, reinforcing a bearish near-term bias.

---

## 7. Actionable Insights & Levels

**Bias: Bearish short/medium-term, with a critical long-term support test underway.**

Support (in order):
1. **24.81–24.85** — 2026-05-15 intraday low + lower Bollinger band (immediate).
2. **24.53** — **200 SMA** (the pivotal line; a sustained close below shifts the long-term thesis bearish).
3. ~24.0 — ~1 ATR below the 200 SMA if support fails.

Resistance (in order):
1. **25.39** — 10 EMA (first hurdle for any bounce).
2. **25.52** — VWMA (volume-weighted "fair value").
3. **26.09** — 50 SMA (medium-term trend cap).
4. **26.45** — upper Bollinger band.

**Playbook considerations:**
- **For bearish/trend-following traders:** The setup favors selling strength into the 25.39–25.52 zone (10 EMA / VWMA) or on a confirmed break below the **24.53** 200 SMA. A logical invalidation stop for shorts is a close back above the 10 EMA / VWMA cluster. Watch for a **death cross** (50 SMA crossing under 200 SMA) as a confirmation trigger.
- **For mean-reversion buyers:** The stock is stretched to the lower band with RSI at 36 and ATR only 0.52. A stabilizing close back above **24.85–24.89** with a positive MACD-histogram turn could offer a tactical bounce toward 25.39. However, note RSI has **not** reached oversold and shows **no bullish divergence**, so this is a lower-conviction counter-trend trade; a break of 24.53 negates it.
- **Risk sizing:** Use ATR (0.52) for stops — e.g., roughly 1 ATR beyond a level. With moderate ATR and compressed bands, expect a **resolution move** (either a bounce off 24.53 or a break lower) rather than prolonged quiet drift.
- **Dividend awareness:** Do not misinterpret the 2026-05-08 decline as accelerating selling — it was largely the $0.43 ex-dividend adjustment. Focus selling-pressure analysis on 2026-05-15's 37.1M-share down day instead.

**The single decision level: the 200 SMA at 24.53.** A hold (with a lower-band bounce) keeps the longer-term base intact and sets up a rebound toward 25.39–26.09. A decisive close below it, especially with expanding Bollinger bandwidth and MACD pushing further negative, would confirm the medium-term downtrend is graduating into a long-term trend break.

---

## 8. Key Points Summary

| Dimension | Indicator | Verified Value (2026-05-15) | Signal / Interpretation |
|---|---|---|---|
| Price | Close | 24.89 | Down ~1.7% from 25.31; new swing low |
| Long-term trend | 200 SMA | 24.53 (rising) | Price ~1.5% above; **key support / last line** |
| Medium-term trend | 50 SMA | 26.09 (falling) | Price ~4.6% below; bearish |
| Short-term trend | 10 EMA | 25.39 (falling) | Price ~2.0% below; bearish |
| Trend cross | 50 vs 200 SMA | Spread ≈ 1.56 (narrowing) | Golden cross intact but **death-cross risk building** |
| Momentum | RSI | 36.12 | Weak, not oversold; no bullish divergence |
| Momentum | MACD / Signal / Hist | −0.269 / −0.23 / −0.04 | Below zero & below signal; **bearish, re-accelerating** |
| Volatility | Bollinger mid/UB/LB | 25.65 / 26.45 / 24.85 | Close at lower band; **squeeze (~6.2% width)** |
| Volatility | ATR | 0.52 (~2.1%) | Use for stops / position sizing |
| Volume | VWMA | 25.52 | Price below → **sellers in control** |
| Volume | 05-15 Volume | 37.1M | Elevated on down day → distribution lean |
| Corporate | Ex-dividend | $0.43 (ex 2026-05-08) | Explains 05-08 drop; not fresh selling |

**Bottom line:** PFE is in a **short/medium-term downtrend** (price below 10 EMA, VWMA, and 50 SMA; negative MACD; RSI sliding) **within an intact long-term uptrend** (price still above a rising 200 SMA). The stock is **pressing the 200 SMA at 24.53** with compressed Bollinger bands, which argues a **resolution move is near**. A hold of 24.53 favors a mean-reversion bounce toward 25.39–26.09; a decisive break below 24.53 would confirm a broader trend breakdown and raise the odds of a 50/200 death cross.