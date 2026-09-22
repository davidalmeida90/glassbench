# JPM (JPMorgan Chase & Co.) — Technical Analysis Report
**Analysis date:** 2026-09-13 (last completed trading session: Friday, 2026-09-11)
**Exchange:** NYQ | **Sector:** Financial Services / Banks – Diversified

> All price, level, and indicator values below are sourced from the verified market snapshot (latest row 2026-09-11) and the indicator time series retrieved for the same date. Where my own arithmetic is layered on top (e.g., point spreads, bandwidth), it is labeled as computed. No conflict was found between the price tool output and the verified snapshot — the two agree exactly on every overlapping value.

---

## 1. Verified Snapshot — The Anchor Numbers

| Metric | Value |
|---|---:|
| Open / High / Low / Close (09-11) | 358.32 / 360.05 / 354.79 / **356.23** |
| Volume (09-11) | 5,354,600 |
| close_10_ema | 355.96 |
| close_50_sma | 351.71 |
| close_200_sma | 317.50 |
| Bollinger middle (20 SMA) | 356.74 |
| Bollinger upper / lower | 363.53 / 349.94 |
| RSI (14) | 51.90 |
| MACD / Signal / Histogram | 0.98 / 1.82 / **−0.83** |
| ATR (14) | 5.92 |
| VWMA | 356.20 |

**Computed spreads (from verified values):**
- Close − 50 SMA = **+4.52 pts (+1.27%)**
- Close − 200 SMA = **+38.73 pts (+12.19%)**
- 50 SMA − 200 SMA = **+34.21 pts (+10.78%)** → a wide, mature bullish separation (the long-term golden-cross configuration is firmly in place)
- Bollinger width = **13.59 pts ≈ 3.81% of the middle band**

---

## 2. Indicator Selection Rationale (8 core + 2 supplementary)

| # | Indicator | Why it earns a slot in *this* market context |
|---|---|---|
| 1 | **close_200_sma** | The primary trend arbiter. Needed to confirm whether the March→August advance is a durable structural uptrend or a bounce. |
| 2 | **close_50_sma** | The medium-term trend and the operative dynamic support that price has been riding during the entire consolidation. |
| 3 | **close_10_ema** | Captures the short-term momentum decay that a 50/200 pair cannot see; essential for timing entries inside a range. |
| 4 | **macd** | Identifies the momentum inflection/crossover regime; currently the single most informative "is the trend stalling?" gauge. |
| 5 | **macds** | Required to make MACD actionable (crossover vs. signal), not just descriptive. |
| 6 | **rsi** | Independent momentum oscillator for overbought/oversold and divergence checks; currently neutral, which matters given a squeeze. |
| 7 | **boll_ub** | Defines the realistic upside breakout trigger rather than guessing a round number. |
| 8 | **boll_lb** | Defines the downside risk envelope / mean-reversion buy zone in a compressing range. |
| + | **atr** (supplementary) | Sizing and stop placement — mandatory because volatility is contracting. |
| + | **vwma** (supplementary) | Volume-weighted confirmation; the only tool here that checks whether the tape *agrees* with the price. |

I deliberately avoided redundant pairings (e.g., RSI + StochRSI, or MACD + a second momentum oscillator) so each slot adds orthogonal information.

---

## 3. Trend Structure: Bullish Backbone, Stalled Engine

**The long and medium-term picture is unambiguously constructive.**
- Price (356.23) sits above the 50 SMA (351.71) **and** well above the 200 SMA (317.50), with all three in correct bullish order — a textbook stacked alignment.
- The **50 SMA has risen on every single trading day** in the retrieved series, from **315.69 (2026-07-15) to 351.71 (2026-09-11)** — an unbroken ~36-point climb with zero down-days. That is a trend that has not been violated at the medium-term timeframe at any point in the last two months.
- The **200 SMA has likewise risen monotonically**, from **306.65 (2026-07-15) to 317.50 (2026-09-11)**.
- The 50/200 spread of **+34.21 pts** is wide and still adjusting upward, meaning the golden-cross regime is mature but not deteriorating.

**But the short-term engine has cooled materially.**
- The **10 EMA peaked around 2026-08-18 at 360.48** and has drifted down to **355.96** by 09-11. It has essentially flat-lined since 08-21 (values oscillating in a tight 355.9–357.5 band).
- The 10 EMA vs. 50 SMA gap has compressed dramatically: from roughly **+19.6 pts on 08-18** (360.48 vs 340.87) to just **+4.25 pts on 09-11** (355.96 vs 351.71) — computed. Short-term momentum has converged into the medium-term trend. That convergence cuts both ways: it is the classic precursor to either a resumption leg or a short-term bearish roll.

**Net read:** an intact, rising multi-month uptrend that has entered a *digestion* phase. This is a "trend healthy, timing neutral" configuration — not a distribution top, but also not a momentum-driven buy.

---

## 4. Range/Consolidation Structure and Levels

From the verified close series, JPM has traded a well-defined band for the last ~4 weeks:

- **Range floor:** closes of **351.55 (08-20)**, **351.58 (08-21)**, **353.51 (09-08)**, **353.56 (09-10)**; intraday lows of **350.37 (08-21)** and notably **348.69 (09-09)**.
- **Range ceiling:** closes of **362.06 (09-03)** and **363.25 (08-18)**; intraday highs of **365.18 close / 366.09 high (08-12)**, **362.85 (09-03)**, **362.86 (09-04)**.
- **Mid-range:** the Bollinger middle (356.74) and the VWMA (356.20) are both within a fraction of a point of the close (356.23) — statistically, price is sitting at *fair value* with no volume-derived edge in either direction.

**The most important structural observation in the dataset:** on **2026-09-09**, JPM printed an intraday low of **348.69** — piercing *below* both the 50 SMA (350.68 that day) and the lower Bollinger band (349.67 that day) — yet **closed at 354.71**, back above both. That is a failed breakdown / band-rejection, and it establishes **348.5–350.0 as the line that has held under pressure.**

**Level map (derived from tool output only):**

| Type | Level | Source |
|---|---|---|
| Hard resistance | 365–366 | 08-12 close 365.18 / intraday high 366.09 |
| Breakout trigger | 362–363.5 | 09-03/09-04 highs 362.85/362.86; boll_ub 363.53 |
| Pivot / fair value | 356.2–356.7 | Close, VWMA 356.20, Boll middle 356.74 |
| First support | 350–352 | 50 SMA 351.71 + boll_lb 349.94 |
| Structural line in the sand | 348.5 | 09-09 intraday low 348.69 |
| Secondary downside magnets | ~344 / ~341 | 07-29 low 343.78; 07-16 low 341.11 |

---

## 5. Momentum: Neutral, With a Bearish Lean Under the Surface

- **RSI = 51.90** — dead-center neutral. RSI has traveled from **65.31 (08-14)** down to a trough of **48.18 (09-08)**, and has recovered to ~51.9. It has not touched 70 or 30 in the retrieved window, confirming there is no overbought exhaustion to relieve *nor* oversold fuel to ignite. In a squeeze, a mid-range RSI is a genuine *no-signal*, and should be traded as such.
- **MACD = 0.98 vs. Signal = 1.82, Histogram = −0.83.** This is the most bearish-tinged element of the entire picture:
  - The MACD line has fallen from **7.16 (08-14)** to **0.98 (09-11)** — an almost complete round-trip of the momentum impulse generated by the July–August run.
  - The MACD line has been **below its signal line throughout the retrieved window** (from 08-14 onward), so the bearish crossover is not fresh news — it is a ~4-week-old, maturing condition.
  - Critically, **both lines are converging toward zero**. The histogram has narrowed from −0.017 (08-14) to −0.83 today, but the MACD/Signal gap is now only **0.83 pts**, the tightest of the period. This is a coiling setup: the next resolution (a bull cross back above signal, or MACD slicing below zero) is likely to be the directional tell for the next leg.
- **Divergence check:** price made its closing high of **365.18 on 08-12** while RSI was already rolling from 65.3 (08-14) and MACD was already beneath its signal — a mild, non-textbook bearish momentum divergence. It has been resolved by *time* (sideways drift) rather than *price* (sharp decline), which is the more benign resolution.

---

## 6. Volatility: A Textbook Squeeze in Progress

- **Bollinger bandwidth has roughly halved:** upper − lower = **27.68 pts on 08-14** vs. **13.59 pts on 09-11** (~51% compression, computed). Normalized, that is ~7.8% of price down to ~3.8%.
- The compression is **asymmetric and bullish-leaning**: the *lower* band has risen from **340.78 (08-14) to 349.94 (09-11)** (+9.16 pts), while the *upper* band has only eased from **368.46 to 363.53** (−4.93 pts). Rising lower bands mean downside volatility is being squeezed out and lows are being made at higher prices — a constructive internal signature.
- **ATR = 5.92**, down from **6.34 (08-14)** and a low of **5.61 (08-31)**. Realized volatility is contracting on both measures, which typically precedes an expansion move.
- **Implication:** a volatility breakout is statistically overdue. Because the trend backdrop is bullish (price > rising 50 SMA > rising 200 SMA), the *higher-probability* resolution is upward — but a squeeze gives no guarantee of direction, so the trade must be conditional on the trigger level, not on the forecast.

---

## 7. Volume: Light Tape, Constructive but Unconvincing

- The last 20 sessions (08-14 → 09-11) average **≈5.56M shares** (computed by summing the verified volume column). The most recent session printed **5.35M**.
- Compare that with the July activity: **18.5M on 07-08**, **15.6M on 07-09**, **14.5M on 07-14** — recent volume is roughly **65–70% below** those expansion days.
- **VWMA = 356.20** is essentially identical to the close (356.23). The volume-weighted fair value and the market price agree — there is no divergence between the tape and the price, and no evidence that either buyers or sellers are dominating on a volume-adjusted basis.
- The **bullish interpretation** of low volume during a sideways drift after a strong advance: no aggressive supply is hitting the market, and sellers are not pressing.
- The **cautionary interpretation:** there is no institutional accumulation visible either. **A breakout above 362–363 on volume at or below ~5.5M shares would be suspect.** Demand confirmation should be sought at **≥7–8M shares** (roughly 1.4x the 20-day average) before treating a breakout as genuine.

*Note: the data includes $1.50/share dividends with ex-dates 2026-04-06 and 2026-07-06 (quarterly cadence, implying a next ex-div window in early October) — worth flagging as a mechanical price adjustment, not a trend signal.*

---

## 8. Actionable Trading Plan

**Base case (highest probability): range resolution higher, but only on a trigger.**
The trend is up, the squeeze is tight, and the 09-09 band rejection proves buyers are defending 348–350. This favors a **buy-the-dip / buy-the-breakout** posture, with a hard no-trade zone in the middle of the range.

**Scenario A — Accumulate on pullback (preferred risk/reward):**
- **Trigger zone:** **350.0–352.0** (50 SMA 351.71 + boll_lb 349.94 confluence).
- **Confirmation required:** a daily close back above ~353.5 after tagging the zone (as happened on 09-08/09-10).
- **Stop:** below the 09-09 low of **348.69**. ~1.0× ATR (5.92) from a 352 entry ≈ 346.1, which sits safely under the structural low — clean.
- **Rationale:** you are buying at the exact juncture where the medium-term trend, the volatility envelope, and a demonstrated intraday rejection all overlap.

**Scenario B — Breakout continuation:**
- **Trigger:** a **daily close above 363.53** (boll_ub) — clearing the 09-03/09-04 highs at 362.85/362.86.
- **Volume filter:** require **≥7M shares** (≈1.4× the 20-day average) to validate.
- **Objective:** the 365.18–366.09 zone (08-12), then measured-move extension.
- **Stop:** back inside the range, below ~358, or a 1× ATR trailing stop (≈5.9 pts) whichever is tighter.

**Scenario C — Breakdown (invalidation):**
- **Trigger:** a **daily close below 348.50**, especially on expanding volume. This would break the 09-09 low, snap the 50 SMA, and split the Bollinger envelope to the downside.
- **Targets:** ~343.78 (07-29 low), then ~341.11 (07-16 low). The 200 SMA at 317.50 is far too distant to be a tactical target.
- **Note the MACD warning:** if MACD (0.98) crosses below zero at the same time, that would confirm Scenario C with two independent systems.

**Do not trade:** the 355–359 chop zone. With RSI at 51.9, MACD in a maturing bear cross, price glued to the flat 10 EMA, and VWMA = price, the middle of the range offers no edge and poor stop placement.

**Risk management (ATR-based, ATR = 5.92 ≈ 1.66% of price):**
- 1× ATR ≈ 5.9 pts | 2× ATR ≈ 11.8 pts.
- The stock's daily noise is modest relative to its $356 price — position sizing can be relatively generous, but cap risk at 1% of equity per idea. With an ~$8 structural stop on Scenario A (±2.3% of price), the implied notional exposure is roughly 40–45% of equity to keep risk at 1%; scale down if using a wider 2× ATR stop.
- Because a squeeze is in force, expect the *first* move out of the range to be fast. Pre-define both triggers; do not improvise directional bias in the middle of a compression.

---

## 9. Summary Table

| Dimension | Indicator / Evidence | Reading | Bullish / Bearish / Neutral |
|---|---|---|---|
| **Long-term trend** | close_200_sma = 317.50, rising every day since 07-15 (306.65) | Price +12.19% above; structural uptrend intact | **Bullish** |
| **Medium-term trend** | close_50_sma = 351.71, rising unbroken from 315.69 (07-15) | Price +1.27% above; dynamic support holds | **Bullish** |
| **Trend alignment** | Close 356.23 > 10EMA 355.96 > 50SMA 351.71 > 200SMA 317.50 | Perfect bullish stack | **Bullish** |
| **Short-term momentum** | close_10_ema = 355.96, peaked 360.48 (08-18), flat since 08-21 | Decaying into neutral; 10EMA/50SMA gap collapsed from ~19.6 to ~4.25 pts | **Neutral** |
| **MACD regime** | MACD 0.98 vs Signal 1.82; Hist −0.83 | Bear cross maturing, both lines converging on zero — coiled | **Neutral-to-Bearish** |
| **RSI** | 51.90 (range 48.18–65.31 over the window) | Dead center; neither overbought nor oversold | **Neutral** |
| **Volatility** | Boll width 27.68 → 13.59 pts since 08-14; ATR 6.34 → 5.92 | ~51% bandwidth compression = squeeze | **Neutral (expansion pending)** |
| **Band positioning** | Close 356.23 vs middle 356.74, LB 349.94, UB 363.53 | Price at fair value; lower band rising (constructive) | **Neutral** |
| **Volume** | VWMA 356.20 ≈ close; 20-day avg vol ≈5.56M vs 18.5M on 07-08 | Light tape — no distribution, but no accumulation either | **Neutral** |
| **Key support** | 350.0–352.0 (50 SMA 351.71 + boll_lb 349.94); structural line 348.69 (09-09 low) | Defended on 09-09 with a band rejection | **Bullish until broken** |
| **Key resistance** | 362.0–363.5 (09-03/09-04 highs; boll_ub 363.53), then 365.2–366.1 (08-12) | Untested since 08-12 | **Neutral** |
| **Overall stance** | Rising 50/200 SMA stack + neutral RSI + MACD coiling + squeeze | Trend healthy, timing neutral → accumulate on dip or trade the breakout | **HOLD with buy-the-dip / buy-the-breakout bias** |

---

**Bottom line:** JPM's primary and intermediate uptrends remain fully intact — the 50 SMA and 200 SMA have not declined for a single session in the retrieved window, and price sits above both. What has changed is *momentum*: MACD has round-tripped from 7.16 to 0.98 and sits below its signal, RSI has settled at 51.9, the 10 EMA has flattened into the 50 SMA, and the Bollinger bands have compressed by roughly half. This is a coiling, not a topping, formation. The tradeable edges are at the edges: **buy 350–352 with a stop under 348.69**, or **buy a close above 363.53 on ≥7M shares** — and stand aside in the 355–359 middle.

FINAL TRANSACTION PROPOSAL: **HOLD**