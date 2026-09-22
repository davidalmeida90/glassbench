# MSFT (Microsoft Corporation) — Technical Analysis Report
**Analysis date: 2026-09-14 | Latest verified trading row: 2026-09-11 (Friday close)**

---

## 0. Scope, Data Provenance & Caveats

- **Verified source of truth:** `get_verified_market_snapshot` for MSFT, requested 2026-09-14, latest trading row used = **2026-09-11**.
- **Data caveat (flagged):** Although today's date is 2026-09-14, **no 2026-09-14 bar exists in any tool output** — both the price CSV (ends 2026-09-11) and `get_indicators` (which labels 2026-09-14 "Not a trading day") stop at 2026-09-11. I therefore treat **every claim below as of the 2026-09-11 close** and make no assumptions about Monday's session. No conflicts between tools were found; `get_stock_data`, `get_indicators`, and the snapshot agree on the 2026-09-11 close of **495.63**.
- All percentage figures are my arithmetic applied to tool-supplied OHLC values, and are labeled with the concrete dates used.

**Last verified OHLCV (2026-09-11):** Open 495.65 / High 498.97 / Low 492.58 / **Close 495.63** / Volume 14,510,500.

**Verified indicator set (2026-09-11):**

| Indicator | Value | Indicator | Value |
|---|---:|---|---:|
| close_10_ema | 496.37 | macd | 10.36 |
| close_50_sma | 453.12 | macds | 14.21 |
| close_200_sma | 429.65 | macdh | −3.85 |
| rsi | 56.88 | atr | 10.65 |
| boll (20 SMA) | 494.25 | boll_ub | 514.13 |
| boll_lb | 474.38 | (vwma, from tool) | 499.47 |

---

## 1. Market Regime & Big-Picture Context

MSFT's trailing 12 months contain **two violent, single-session repricings** that dominate the tape:

- **Bear phase (Jan–Jun 2026):** Prior close 478.59 (2026-01-28) → next open 437.22 (2026-01-29) = an **~8.6% opening gap down**, with volume 128.9M (vs ~30M typical). Price then bled to a closing low of **355.33 on 2026-03-27**, recovered into April–May, then made a *lower* closing low of **352.17 on 2026-06-25**.
- **Bull phase (Jul–Sep 2026):** Prior close 389.81 (2026-07-29) → next open 437.08 (2026-07-30) = an **~12.1% opening gap up** (volume 110.2M). Price rallied from ~390 to a **closing high of 513.53 on 2026-08-28** (intraday high 517.78).

The pattern of isolated mega-volume gaps on single dates is *characteristic of event-driven (e.g., earnings) repricing*, though the dataset does not explicitly confirm the catalyst — I flag that as inference, not fact. The practical takeaway: **MSFT is a gap-driven, headline-sensitive name**, which argues for wider stops (see §6).

**Current regime verdict: recovering uptrend, mid-consolidation.** Price sits in the *middle* of its Bollinger structure — (495.63 − 474.38) / (514.13 − 474.38) = **53.5% of the band width** — i.e., neither a breakout nor a breakdown.

---

## 2. Trend Structure — Multi-Timeframe (Bullish, but Stretched)

This is the strongest part of the setup:

- **Long-term (200 SMA = 429.65):** Price is **+65.98 (+15.4%) above** the 200 SMA. Critically, the 200 SMA **stopped falling and turned up**: it bottomed at 429.26–429.28 on 2026-08-25/26 and printed 429.65 on 2026-09-11 — a genuine (if shallow) inflection in the long-term trend line.
- **Medium-term (50 SMA = 453.12):** Rising steeply — 400.89 (2026-07-16) → 453.12 (2026-09-11), about **+52 points in under two months**. Price is **+9.4% above** it.
- **Golden cross confirmed:** On 2026-08-27 the 50 SMA (427.27) was *below* the 200 SMA (429.34); on **2026-08-28 the 50 SMA (429.97) crossed above the 200 SMA (429.40)**. The 50 SMA is now ~5.5% above the 200 SMA. This is a classic strategic bull confirmation.
- **Short-term (10 EMA = 496.37):** Price (495.63) has slipped **just below** the 10 EMA, which itself has rolled over from ~499.80 (2026-09-03/04) to 496.37 (2026-09-11). This is the first hint that the *fast* trend has flattened.

**Interpretation:** The trend hierarchy (price > 10 EMA ≈ flat, price ≫ 50 SMA rising, 50 SMA > 200 SMA turning up) is a textbook bull stack. However, price being **9.4% above the 50 SMA** is extended; historically such gaps resolve either via sideways time-correction (base building) or a sharper mean-reversion dip. The current action looks like the *former*.

---

## 3. Momentum — Cooling Sharply From Overbought

Momentum is where the caution lives:

- **RSI = 56.88.** Neutral-bullish. It ran hot: 79.15 (2026-08-10), 78.15 (2026-08-07), 74.52 (2026-07-31), then 73.53 (2026-08-28), and cooled to a trough of **54.82 (2026-09-09)** before ticking back to 56.88.
- **Bearish RSI divergence:** MSFT printed a **higher price high on 2026-08-28 (close 513.53)** on a **lower RSI high (73.53)** than the 2026-08-11 close (502.86, RSI 77.72). Non-confirmation — a classic warning that preceded this pullback.
- **MACD = 10.36, Signal (macds) = 14.21, Histogram (macdh) = −3.85.** The MACD line is still **above zero** (it crossed above zero on 2026-07-30: −0.49 → +4.42) but has decelerated hard from its 2026-08-11 peak of **30.25**. The **MACD/signal bearish cross occurred on 2026-08-18** (histogram +1.11 on 08-17 → −0.61 on 08-18) and the histogram has been negative ever since, widening to −3.94 (2026-09-10) and marginally narrowing to −3.85 (2026-09-11).
- **Same divergence on MACD:** higher price high on 2026-08-28 (MACD 18.97) vs 2026-08-11 (MACD 30.25) — momentum peaked *well before* price did.

**Interpretation:** This is a **bullish primary trend with a bearish intermediate momentum impulse**. The correct read is a *corrective pullback within an uptrend*, not a trend reversal — because the MACD remains above zero, the 50/200 SMA stack is intact and rising, and RSI never broke below 50 for more than a session. But there is **no long trigger yet**: the histogram would need to curl back toward/above zero and RSI reclaim the high-50s to confirm the pullback has ended.

---

## 4. Volatility — Contracting (Coiled Spring)

- **ATR = 10.65**, which is **~2.15% of the 495.63 close** and the **lowest reading in the entire 60-day window** (peak 17.01 on 2026-08-04; ~11.8–12.1 through mid-July).
- **Bollinger bands:** Middle 494.25, Upper 514.13, Lower 474.38 → width ~39.75, i.e. **~8.0% of the middle band**. Bands are wide in absolute terms but the price has stopped riding the upper band — the 2026-08-28 close (513.53) essentially tagged the upper band (514.13) and was rejected.
- Bollinger lower (474.38) and the 2×ATR stop (495.63 − 2×10.65 = **474.33**) sit almost exactly on top of each other — a strong **confluence support cluster near 474**.

**Interpretation:** Volatility is **compressing after a volatility event**, and price is pinned to the middle band. Compression after an impulse typically resolves in a directional expansion — direction is unconfirmed. This is a "wait for the break" environment rather than a "chase" environment.

---

## 5. Volume & Participation — Selling Is Drying Up

- **VWMA = 499.47** vs close 495.63 → price is **~0.77% BELOW** the volume-weighted average. That means recent transacted volume has, on average, changed hands at prices north of the current print — a mild **distribution/dilution signal** that argues against aggressive chasing at 495.
- However, VWMA is itself **rising** (492.08 on 2026-08-28 → 499.47 on 2026-09-11), so the volume-weighted trend is still up.
- **Volume is fading on the pullback:** 2026-08-28 = 29.2M, 2026-09-03 = 24.1M, 2026-09-04 = 18.1M, 2026-09-08 = 18.9M, 2026-09-09 = 12.9M, 2026-09-10 = 16.0M, **2026-09-11 = 14.5M**. Declining volume into a decline is constructive — it suggests **supply exhaustion rather than institutional dumping**.

**Interpretation:** No distribution climax. If anything, the low-volume drift lower is the fingerprint of a **healthy consolidation**.

---

## 6. Key Levels — Evidence-Based

| Level | Price | Evidence (dated) |
|---|---:|---|
| **Resistance zone 2** | ~517.8 | Intraday high 517.78 (2026-08-28) |
| **Resistance zone 1** | ~514–516 | Bollinger upper 514.13 (verified); intraday high 515.65 (2026-09-03) |
| **Pivot / mid-band** | 494.25 | Bollinger middle (20 SMA), verified 2026-09-11 |
| **Immediate support** | ~490–492 | Intraday lows 490.15 (09-08), 489.80 (09-09), 486.00 (09-10) |
| **Secondary support** | ~479–483 | Aug 17–21 congestion; closes 479.45, 480.73, 483.40, 481.15, 483.24 |
| **Major support cluster** | ~474 | Bollinger lower 474.38 + 2×ATR stop 474.33 |
| **Trend support (medium)** | 453.12 | 50 SMA, rising ~2.2 pts/session |
| **Trend support (long)** | 429.65 | 200 SMA, turning up |

Note: this is a **structural map**, not a claim that price has "bounced" off these levels. I am not asserting historical test-and-hold behavior beyond what the dated OHLC above shows.

---

## 7. Actionable Framework

**Bias: Constructive (long) on the primary trend; patient/tactical on entry.**

The problem with buying *right now* at 495.63 is location, not direction: price is **mid-band**, roughly equidistant from the 514 resistance and the 474 support cluster, momentum is negative, and price is below both the 10 EMA (496.37) and VWMA (499.47). Risk/reward from spot is only ~1:1.

**Plan A — Reclaim trigger (momentum confirmation):** Wait for a close back above the **10 EMA / 496–500 zone** with the MACD histogram turning back toward zero and volume expanding above the recent ~14–18M run-rate. That converts the setup into a trend-continuation entry toward **514–518**.

**Plan B — Pullback buy (preferred risk/reward):**
- **First tranche:** 490–492 (immediate support / just above the 20-SMA mid-band).
- **Second tranche:** 479–483 (Aug congestion shelf).
- **Stop:** below **479** for a tight version, or below the 474 confluence cluster (Bollinger lower 474.38 / 2×ATR 474.33) for a wider, structure-based version.
- **Target:** 514–518 resistance zone first, then measured continuation if the 2026-08-28 high (517.78 intraday / 513.53 close) is cleared on volume.

**Plan C — Invalidation / bear case:** A decisive close **below 474** would break the Bollinger lower band, the 2×ATR stop, and the Aug congestion shelf simultaneously, opening a path toward the **50 SMA at 453.12**. A further break of the rising 50 SMA would meaningfully damage the golden-cross thesis.

**Position sizing:** With ATR at 10.65 (~2.15% of price), size positions so that a 1.5–2.0 ATR adverse move is within tolerance. The ATR compression means stops can be set tighter than in early August (when ATR ~17), but also that a volatility expansion could gap through them — hence the preference for a tranched entry rather than a single all-in fill.

---

## 8. Summary Table

| Dimension | Reading (2026-09-11) | Signal | Confidence |
|---|---|---|---|
| Close | 495.63 | — | Verified |
| Long-term trend | Price +15.4% vs 200 SMA (429.65); 200 SMA inflecting up | **Bullish** | High |
| Medium-term trend | Price +9.4% vs 50 SMA (453.12), steeply rising | **Bullish but extended** | High |
| Golden cross | 50 SMA crossed above 200 SMA on **2026-08-28** | **Bullish** | High |
| Short-term trend | Price just below 10 EMA (496.37), 10 EMA rolling over | **Neutral/soft** | Medium |
| RSI | 56.88 (down from 79.15 on 08-10); bearish divergence into 08-28 high | **Cooling / caution** | High |
| MACD | 10.36 vs signal 14.21; histogram −3.85; bearish cross 2026-08-18; MACD > 0 | **Bearish intermediate, bullish primary** | High |
| Bollinger | Mid 494.25 / UB 514.13 / LB 474.38; price at 53.5% of band | **Neutral, mid-range** | High |
| ATR | 10.65 (2.15% of price), lowest in 60 sessions | **Volatility contraction** | High |
| VWMA | 499.47; price 0.77% below, but VWMA rising | **Mild caution** | Medium |
| Volume | Declining on pullback (14.5M on 09-11 vs 29.2M on 08-28) | **Constructive (supply drying up)** | Medium |
| Key resistance | 514–518 (UB 514.13; highs 517.78 / 515.65) | Trigger for new leg | High |
| Key support | 490–492 → 479–483 → 474 confluence → 453 (50 SMA) | Tranche entries / invalidation | High |

---

## Verdict

MSFT is in a **confirmed, maturing uptrend** (golden cross 2026-08-28, price above both major moving averages, 200 SMA turning up) that is currently in a **low-volume, volatility-compressing consolidation** just below the 10 EMA and VWMA. Momentum indicators (MACD histogram negative since 2026-08-18, RSI cooled from ~79 to ~57, dual bearish divergences into the 2026-08-28 high) argue **against chasing at 495.63**, while the trend stack and drying-up volume argue **against selling**. The highest-expectancy posture is to hold existing exposure and deploy new capital on either (a) a reclaim of 496–500, or (b) a pullback into 490–492 / 479–483 with a stop below the 474 confluence.

FINAL TRANSACTION PROPOSAL: **HOLD** (maintain core long; add on a 490–492 or 479–483 pullback, or on a volume-confirmed reclaim above 500; invalidate below 474).