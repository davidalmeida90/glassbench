# MSFT (Microsoft Corporation — NMS) Technical Analysis Report
**Analysis date: 2026-09-21 | Latest verified trading row: 2026-09-21 | Prev. close 492.30**

---

## 1. Data Verification & Integrity Notes

**Verified source of truth (2026-09-21 snapshot):**

| Field | Value |
|---|---:|
| Open | 495.58 |
| High | 497.39 |
| Low | 491.50 |
| Close | 492.30 |
| Volume | 6,383,963 |

**Reconciliation check:** Every indicator value returned by the technical-indicator vendor matches the verified snapshot to the penny (10 EMA 495.4739 vs 495.47; 50 SMA 466.3581 vs 466.36; 200 SMA 430.1027 vs 430.10; MACD 6.1752 vs 6.18; MACD signal 9.3848 vs 9.38; MACD hist −3.2096 vs −3.21; RSI 52.3366 vs 52.34; ATR 10.2737 vs 10.27; Boll upper 512.12, lower 483.80 — both exact). **No conflicting values were found between tools.**

**One anomaly to flag, not to resolve:** the 2026-09-21 volume of **6.38M shares** is an outlier versus the surrounding tape (12.9M on 9/9, 17.8M on 9/17, 39.5M on 9/18). This looks like a partial/incomplete session print or a very thin Monday. I am **not** inferring distribution or accumulation from it; treat the 9/21 bar's volume signal as unreliable and use price levels from it with caution. All other OHLCV rows appear internally consistent.

Data window retrieved: 2026-03-01 → 2026-09-21 (141 rows). **Retrieved-window extremes: high 517.78 (2026-08-28 intraday), low 348.54 (2026-06-25 intraday).**

---

## 2. Selected Indicator Set (8) and Why

| # | Indicator | Role in this context |
|---|---|---|
| 1 | **close_10_ema** | Fast read on whether the September stall is a pause or a rollover. Price is now oscillating *around* it — the cleanest short-term tell. |
| 2 | **close_50_sma** | Medium-term trend spine and dynamic support; also the fast leg of the golden cross. |
| 3 | **close_200_sma** | Long-term regime benchmark; confirms the strategic uptrend and the August cross. |
| 4 | **macd** | Detects momentum decay after a large advance (a primary risk right now). |
| 5 | **macds** | Provides the crossover trigger reference (MACD is already below signal). |
| 6 | **rsi** | Confirms whether price is stretched or neutral; currently the key "room to move" gauge. |
| 7 | **atr** | Volatility/stop sizing in a compressing tape; converts levels into risk units. |
| 8 | **vwma** | Adds the volume dimension — is the volume-weighted participant above or below spot? |

*Ancillary:* the verified snapshot's **Bollinger envelope (mid 497.96 / upper 512.12 / lower 483.80)** is used for level framing; it overlaps functionally with ATR for the volatility slot, so it was not counted among the 8.

**Redundancy avoided:** no RSI+StochRSI pairing, no triple-MACD stack (MACD + signal suffice; the histogram value is quoted as context only), and only one volume indicator exists in the menu.

---

## 3. Long-Term & Medium-Term Trend Structure

**The strategic trend is unambiguously up, and it re-established itself in late July/August after a violent mid-year drawdown.**

- **200 SMA at 430.10**, and it has *turned up marginally* — it bottomed around 429.26 (2026-08-25) after gliding down from 434.61 (2026-07-23). A flat-to-rising 200 SMA on a price 14.5% above it is a constructive long-term configuration.
- **50 SMA at 466.36 and rising steeply** — it has climbed every single session in the retrieved window from 397.11 (2026-07-29) to 466.36 (2026-09-21). That is an unbroken 30+ session advance in the medium-term trend line.
- **Golden cross confirmed:** on 2026-07-23 the 50 SMA (398.82) sat **below** the 200 SMA (434.61) — a death-cross regime. On 2026-08-27 the 50 SMA (427.27) was still below the 200 SMA (429.34); on **2026-08-28 the 50 SMA (429.97) crossed above the 200 SMA (429.40)**. The spread has since widened to **36.26 points** (466.36 vs 430.10), i.e., the cross is being confirmed, not immediately failing.
- **Price reclaimed the 200 SMA on 2026-07-30** (close 450.25 vs 200 SMA 431.67, following 389.81 vs 431.96 on 2026-07-29). That gap-up day printed **110.2M shares** — a genuine regime-change bar, not drift.

**Breadth of the move:** close 492.30 is **+26.3%** from the 2026-07-29 close of 389.81 and **+39.8%** from the 2026-06-25 close of 352.17. This is a large, fast recovery — which is precisely why the current momentum decay matters.

**Distance from trend:** price is **+5.6% above the 50 SMA** and **+14.5% above the 200 SMA**. That is a healthy-but-extended posture; the 50 SMA is far enough below to be a poor near-term stop reference.

---

## 4. Short-Term Structure: A Coiling Range, Not a Trend

The last ~5 weeks are a **high-level consolidation with a slight downward bias in momentum**:

- **10 EMA at 495.47 and flattening.** It peaked near 499.83 (2026-09-03) and has since drifted sideways in a tight 495–500 band. **Price closed at 492.30 — below the 10 EMA for the first time in several sessions (9/17 and 9/18 closed at 497.75 and 493.78, straddling it).**
- **Range behavior since 2026-08-28:** closes have pinballed between 479.45 (8/17) and 513.53 (8/28), and in September specifically between 490.30 (9/16) and 510.12 (9/3).
- **Repeated supply at 505–515:** 505.11 (8/10 close), 505.06 (8/27 close), 510.12 (9/3 close, high 515.65), 505.41 (9/14 close). Four separate attempts into this zone have failed to hold.
- **Repeated demand at 487–492:** 491.50 (8/12 close), 487.23 (9/16 low), 491.50 (9/21 low). Notably, the **8/12 close and the 9/21 low are both exactly 491.50** — a level the market has respected twice in six weeks. This is the pivot to watch.

**Bollinger position:** mid-band 497.96, price 492.30 → **%B ≈ 0.30** (lower third of the envelope). Price is below the 20-period mean but nowhere near the lower band at 483.80. Translation: **mild distribution within a range, not a breakdown.**

---

## 5. Momentum: The Key Deterioration

This is the most important nuance in the entire report.

**MACD is decaying quickly while price merely chops sideways.**

| Date | MACD | Signal | Histogram |
|---|---:|---:|---:|
| 2026-08-28 | 18.97 | 20.11 | −1.14 |
| 2026-08-31 | 18.76 | 19.84 | −1.07 |
| 2026-09-04 | 15.48 | 17.84 | −2.36 |
| 2026-09-10 | 11.22 | 15.17 | −3.94 |
| 2026-09-14 | 10.35 | 13.43 | −3.09 |
| 2026-09-18 | 7.00 | 10.19 | −3.19 |
| **2026-09-21** | **6.18** | **9.38** | **−3.21** |

- **Bearish MACD/signal crossover occurred around 2026-08-19** (histogram flipped from +1.11 on 8/17 to −0.61 on 8/18 to −1.71 on 8/19) and has persisted for over a month.
- The **MACD line is still positive (6.18 > 0)**, so the *uptrend* is intact — this is momentum decay, **not yet a trend reversal**.
- **The rate of decline is the warning:** MACD fell from 10.35 (9/14) to 6.18 (9/21), roughly **−0.83/day over five sessions**. Extrapolated at that pace, the MACD line reaches zero in roughly 7–8 trading sessions. **A zero-line cross would be a materially more serious signal than the current signal-line cross**, and it is the single highest-value thing to monitor next.
- The **histogram has stopped deteriorating** (−3.94 on 9/10 → −3.21 on 9/21), suggesting the *second derivative* of price momentum is stabilizing. That is the one scrap of near-term encouragement for bulls.

**RSI at 52.34 — neutral, with no extremes in either direction.** This is important for two reasons:
1. There is **no oversold cushion** to bounce from; downside acceleration would be unencumbered by a washed-out oscillator.
2. There is **no overbought condition capping upside**; a breakout to 505–515 would not be immediately rejected by RSI.
- RSI registered overbought readings in August (73.53 on 8/28, 71.84 on 8/13, 70.92 on 8/14) — a strong-trend signature. It has since cooled to 52.34 via **lower highs in both price and RSI** (513.53 close / 73.53 RSI on 8/28 → 510.12 / 66.41 on 9/3 → 505.41 / 61.58 on 9/14). That is consistent momentum decay, **but it does not meet the bar of a formal divergence signal**, so I will not label it one.

---

## 6. Volatility: Compression Setup

**ATR has contracted persistently: 14.79 (2026-08-12) → 13.51 (8/18) → 12.05 (8/28) → 11.82 (9/4) → 10.27 (9/21).**

- Current ATR of **10.27 is ≈2.1% of the 492.30 close** — about a **31% contraction** from the mid-August peak. Compute: 10.27/14.79 − 1 = **−30.6%**.
- **Bollinger bandwidth has collapsed** from an enormous 128.3 points on 2026-08-24 (upper 541.38 / lower 413.10, an artifact of the late-July gap) to **28.32 points on 2026-09-21 (512.12 − 483.80)**. Looking only at stable weeks: 8/28 width ≈ 37.7, 9/11 width ≈ 39.8, 9/21 width = 28.3. **The envelope is squeezing.**
- **Coiling after a large impulse resolves directionally, and the resolution usually comes on expanding volume.** With ATR compressed and MACD decaying, the bias of the next resolution is slightly to the downside — but the setup itself is neutral until the 487 / 505 boundaries break.
- **Risk-sizing consequence:** a reasonable 1.5×ATR stop is **15.4 points (≈3.1% of price)**; a 1×ATR stop is **10.3 points (≈2.1%)**. Sizing on ATR means position size can be increased modestly versus August's 14–15 point ATR environment on an equal-risk basis.

---

## 7. Volume: The Volume-Weighted Participant Is Above Spot

**VWMA at 497.86 versus close 492.30 → spot is trading ≈5.6 points (≈1.1%) BELOW the volume-weighted average price.**

- VWMA rose in a near-straight line from 458.41 (2026-08-12) to 500.56 (9/14), then **flattened at 500.6 → 501.2 → 501.0 → 499.0 → 497.9 (9/21)**.
- The fact that VWMA has **stopped rising while price is below it** means recent volume has transacted at higher average prices than the current print — **mild overhead supply / distribution pressure in the 497–501 area**.
- **Read-through:** rallies back toward 497–501 should be tested for whether buyers can reclaim the volume-weighted mean. A decisive close back above ~498 would neutralize this bearish tell; continued failure at/under 498 keeps the pressure on.
- **Caveat (important):** the 9/21 VWMA is computed including an anomalously low 6.38M-share volume print. Volume-skew indicators are sensitive to such outliers, so treat the 9/21 VWMA value as slightly less reliable than the trend of the preceding two weeks.

---

## 8. Levels, Scenarios, and Actionable Plan

### Price map (all levels derived from tool output with dates)
| Level | Value | Source |
|---|---:|---|
| Retrieved-window high | 517.78 | 2026-08-28 intraday high |
| Hard supply / breakout trigger | 512–516 | Boll upper 512.12; 9/3 high 515.65 |
| Supply shelf | 505–510 | 8/10 close 505.11; 8/27 close 505.06; 9/3 close 510.12; 9/14 close 505.41 |
| Bollinger mid / VWMA | 497.96 / 497.86 | Verified snapshot |
| Spot | 492.30 | 2026-09-21 close |
| Pivot / repeated level | 491.50 | 8/12 close and 9/21 low (both exactly 491.50) |
| First support | 487.23 | 9/16 low |
| Bollinger lower | 483.80 | Verified snapshot |
| Trend support | 466.36 | 50 SMA, rising |
| Long-term floor | 430.10 | 200 SMA, flattening/edging up |

### Scenario A — Bullish breakout (needs confirmation)
**Trigger:** daily close **above 505**, ideally on volume >20M shares (i.e., back to the September norm), which would put price above the 10 EMA, VWMA, and the mid-band simultaneously.
**Targets:** 512.12 (upper band) → 515.65 (9/3 high) → 517.78 (8/28 high).
**Invalidation:** close back below 497.96 (mid-band).
**Caveat:** for this to be more than a range bounce, the **MACD histogram must turn positive** and the **MACD line must hold above zero**. Without that, treat a push to 505–510 as another fade candidate — the tape has already failed there four times.

### Scenario B — Range continuation (currently the highest-probability path)
**Structure:** 487–505 chop with the 20-day mid (497.96) as the magnet.
**Playbook:** mean-reversion fades at the extremes with tight, ATR-based stops; do not chase mid-range entries. The **VWMA at 497.86** is the natural reversion pivot.
**Invalidation:** a decisive close outside 487 or 505.

### Scenario C — Bearish breakdown
**Trigger:** daily close **below 487.23** (9/16 low), which also breaks the 491.50 shelf.
**Targets:** 483.80 (lower Bollinger) → 466.36 (50 SMA, ~2.5 ATR below spot).
**Confirmation to require:** **MACD crossing below zero** (from 6.18, ~7–8 sessions away at the current decay rate) and RSI losing 45–50.
**Caveat:** with RSI at 52.34 there is no oversold buffer, so a breakdown can travel further than a range-trader would expect — the 50 SMA at 466.36 is a realistic magnet, and it is **25.9 points (5.3%) below spot**.

### Risk management specifics
- **Stop distance:** 1×ATR = 10.27 pts; 1.5×ATR = 15.4 pts; 2×ATR = 20.5 pts.
- **Long stop reference:** 486.9 (= 492.30 − ~0.5×ATR, below the 487.23 low) for a tight trade; 477.9 (= 492.30 − 1.4×ATR) for a swing position that respects the 8/17–8/21 base at 479.45–483.40.
- **Do not use the 50 SMA (466.36) as a stop** for a near-term long — it is >5% away and implies oversized risk.
- **Position sizing:** with ATR at 2.1% of price (down from ~3.0% in mid-August), equal-risk sizing permits a modestly larger position than a month ago; scale inversely to ATR if volatility expands on a breakout.

---

## 9. Synthesis — The Nuanced Read

**Bull case (structural):** a confirmed golden cross on 2026-08-28, a rising 50 SMA for over 30 consecutive sessions, a 200 SMA that has stopped falling and edged up to 430.10, price 14.5% above it, and a volatility squeeze that typically precedes a directional expansion. RSI at 52.34 leaves plenty of room before overbought.

**Bear case (tactical):** MACD has been below its signal since ~2026-08-19 and is **falling ~0.83/day**, on pace for a zero-line cross within two weeks. The 10 EMA has rolled flat at 495–500 and price closed beneath it. VWMA (497.86) sits **above** spot, indicating volume-weighted supply overhead. Price has failed at 505–515 four separate times and %B is only 0.30.

**The honest verdict:** this is a **consolidation inside a larger uptrend, with decaying momentum and compressing volatility** — a "wait for the break" tape, not a "pick a direction" tape. The 487–505 box is the decision zone. The two things that would materially change the picture are **(1) a MACD zero-line cross** (bearish escalation) and **(2) a volume-confirmed close above 505** (bullish re-acceleration). Until one occurs, range logic dominates and stops belong tight relative to ATR.

---

## 10. Summary Table

| Dimension | Indicator | Latest value (2026-09-21) | Signal | Key evidence dated |
|---|---|---:|---|---|
| Short trend | **close_10_ema** | 495.47 | **Neutral / rolling over** | Peaked ~499.83 on 9/3; close 492.30 now below it |
| Medium trend | **close_50_sma** | 466.36 | **Bullish** | Rose every session from 397.11 (7/29) → 466.36; price +5.6% above |
| Long trend | **close_200_sma** | 430.10 | **Bullish (improving)** | Bottomed ~429.26 (8/25); 50 SMA crossed above on 8/28 (429.97 vs 429.40) |
| Momentum | **macd** | 6.18 | **Deteriorating, still positive** | 18.97 (8/28) → 10.35 (9/14) → 6.18; ~−0.83/day |
| Momentum | **macds** | 9.38 | **Bearish crossover intact** | Crossed ~8/19 (hist +1.11 on 8/17 → −1.71 on 8/19) |
| Momentum | *macdh (context)* | −3.21 | **Negative but stabilising** | −3.94 (9/10) → −3.21 (9/21) |
| Momentum | **rsi** | 52.34 | **Neutral** | Cooled from 73.53 (8/28) via lower highs; no extreme |
| Volatility | **atr** | 10.27 | **Compressing** | 14.79 (8/12) → 10.27; −30.6%; ≈2.1% of price |
| Volatility | *Bollinger (context)* | mid 497.96 / ub 512.12 / lb 483.80 | **Squeeze; %B ≈ 0.30** | Width 28.32 vs 128.3 on 8/24 |
| Volume | **vwma** | 497.86 | **Mildly bearish** | Flat 500.6→497.9 since 9/14 while spot is below it |
| Price level | Pivot | 491.50 | **Watch** | Equals 8/12 close and 9/21 low |
| Price level | Support | 487.23 → 483.80 → 466.36 | **Ladder down** | 9/16 low; lower band; 50 SMA |
| Price level | Resistance | 505 → 512.12 → 517.78 | **Ladder up** | Four failed tests since 8/10; upper band; 8/28 high |

**Bottom line for MSFT:** Strategic trend up (golden cross confirmed 2026-08-28), tactical momentum down (MACD below signal since ~2026-08-19), volatility coiling (ATR −30.6% since 8/12). **Range 487–505 until proven otherwise; the MACD zero-line cross is the bearish trigger to pre-commit to, and a volume-confirmed close above 505 is the bullish trigger.** Flag: the 9/21 volume print of 6.38M is anomalous and should not be used as a standalone signal.