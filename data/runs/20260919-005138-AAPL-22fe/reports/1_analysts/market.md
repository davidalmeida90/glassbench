# AAPL (Apple Inc.) — Technical Analysis Report
**Analysis date:** 2026-02-13 | **Exchange:** NMS | **Sector:** Technology / Consumer Electronics
**Verified by:** `get_verified_market_snapshot` (treated as source of truth). All indicator values below were cross-checked against `get_indicators` output and matched — no discrepancies to flag.

---

## 1. Where AAPL stands right now (verified)

| Field (2026-02-13) | Value |
|---|---:|
| Open | 261.54 |
| High | 261.76 |
| Low | 254.99 |
| **Close** | **255.32** |
| Volume | 56,290,700 |

AAPL is in the middle of a sharp, high‑volume two‑day selloff. Using the verified snapshot closes:
- **Feb 11 close 275.01 → Feb 13 close 255.32 = −19.69 points (−7.16%).**
- **Feb 6 close 277.36 (recent swing high) → Feb 13 close 255.32 = −22.04 points (−7.95%).**

The drop was front‑loaded on **Feb 12 (close 261.26, volume 81,077,200 — the largest of the last 30 sessions)** and continued **Feb 13 (close 255.32, volume 56,290,700)**. That volume signature indicates institutional distribution rather than a quiet drift.

**Context matters:** This selloff comes *within a still‑intact longer‑term uptrend*. The 200‑day SMA is at 239.18 and rising, and the 50‑day SMA (266.77) remains above the 200‑day SMA — the long‑term bullish structure has not been broken. What has broken is the **short‑ and medium‑term structure**.

---

## 2. Indicator selection & rationale

I selected 8 complementary indicators spanning trend, momentum, volatility, and volume — deliberately avoiding redundancy (e.g., no RSI + Stochastic):

| Indicator | Category | Why it's the right tool here |
|---|---|---|
| `close_10_ema` | Short-term trend | AAPL's price just sliced through this; fastest read on the momentum break. |
| `close_50_sma` | Medium-term trend | The pivot that flipped from support to potential resistance; defines the "damaged" intermediate trend. |
| `close_200_sma` | Long-term trend | The line that separates a healthy pullback from a genuine trend change. |
| `macd` | Momentum | Captures the rollover in trend momentum. |
| `macds` | Momentum trigger | Provides the crossover signal against the MACD line. |
| `rsi` | Momentum oscillator | Gauges whether the drop is merely corrective or approaching oversold exhaustion. |
| `atr` | Volatility | Sets realistic stops and position sizes now that volatility is expanding. |
| `vwma` | Volume | Confirms whether price action is backed by volume (distribution vs. noise). |

---

## 3. Trend analysis — long-term intact, short/medium-term broken

- **`close_200_sma` = 239.18 (rising).** AAPL closed at 255.32, still **~6.7% above** the long‑term benchmark. The 200‑SMA has climbed every session over the lookback (238.02 on Feb 9 → 239.18 on Feb 13), so the primary uptrend is technically undisturbed so far.
- **`close_50_sma` = 266.77 (turning down).** It peaked around 268.34 (Jan 27) and has been rolling over. Critically, **price (255.32) is now below the 50‑SMA** — the intermediate trend has flipped from tailwind to headwind.
- **`close_10_ema` = 266.33.** Price has fallen sharply below it (255.32 vs 266.33). The 10‑EMA is the most damning near‑term signal: the short‑term average is now *above* the close and flattening, confirming the short‑term trend has turned down.
- **50/200 relationship:** 50‑SMA (266.77) still sits **well above** the 200‑SMA (239.18) → the golden‑cross regime established earlier remains in force. No death cross is close.

**Read:** This is a *discipline test* for the long-term trend. The bull structure holds as long as the 200‑SMA and the ~246 area contain the pullback, but tactical (days–weeks) positioning has shifted to defensive.

---

## 4. Momentum analysis — a fresh, fast negative turn

- **RSI = 39.59.** Collapsed from **63.55 (Feb 11) → 44.97 (Feb 12) → 39.59 (Feb 13)** — a ~24‑point dive in two sessions. It has crossed below the 50 midline (momentum now bearish) but is **not yet oversold** (<30). Two implications: (a) momentum has clearly turned negative; (b) there is **still room to fall** before a classic oversold bounce signal appears.
- **MACD = 1.18 vs Signal = 1.19 → Histogram ≈ −0.01.** The MACD line has just **crossed below its signal line**, a freshly triggered **bearish crossover**. Note the MACD had only recently recovered from a deeply negative January stretch (as low as −6.23 on Jan 23, produced by the mid‑January selloff), so this crossover aborts that recovery.
- **Divergence context:** RSI made a lower high while price made a higher high into Feb 6–11 (price 277.36; RSI never reclaimed its Jan peaks) — a classic momentum‑vs‑price divergence that preceded this drop.

**Read:** Momentum is unambiguously negative and freshly so. The bearish MACD cross combined with RSI below 50 argues the path of least resistance is lower until stabilization signals emerge.

---

## 5. Volatility analysis — expanding, size down

- **ATR = 6.52**, up from 5.81 (Feb 11) and ~5.0 in mid‑December. Volatility is **expanding**, consistent with the violent two‑day move.
  - Practical use: a 1× ATR daily range is ~$6.5; a 2× ATR stop is ~$13 (about 5% of the current price). Stops set too tight relative to ATR will get shaken out.
- **Bollinger (20‑day) — Middle = 261.62, Upper = 283.50, Lower = 239.75.** Band width ≈ **$43.75**, unusually wide, reflecting the recent spike in realized volatility.
  - Price (255.32) is now **below the middle band (261.62)** — a bearish shift toward the lower half of the envelope.
  - The **lower band (239.75)** sits almost exactly on the **200‑SMA (239.18)** — a meaningful **confluence zone around 239–240** if the decline extends.

**Read:** With ATR widening and Bollinger bands stretched, expect larger daily swings. Risk per position should be reduced, and any stop should be ATR‑aware.

---

## 6. Volume analysis — distribution confirmed

- **VWMA = 266.61.** Price (255.32) is **~4.2% below** the volume‑weighted average. Because VWMA weights recent activity by volume, a close below it means the *heaviest* trading (Feb 12–13 selloff) has been on the downside — a bearish near‑term signal.
- The Feb 12 down day carried **81.08M shares** vs. the prior week's ~40–50M range, and Feb 13 added **56.29M** — confirming that this decline was volume‑supported, not a thin drift.

**Read:** VWMA and heavy down‑volume corroborate distribution. Bulls need to see this reverse — i.e., a rebound on *expanding* up‑volume — before trusting a bottom.

---

## 7. Synthesis & actionable insights

**The big picture:** AAPL's *strategic* (long‑term) trend is still up — the 200‑SMA is rising and far below price. But the *tactical* picture has decisively weakened: price is below the 10‑EMA, 50‑SMA, VWMA, and Bollinger midline; RSI has broken below 50; MACD has just crossed bearish; and volume confirms distribution.

**Level map (all drawn from tool output — reference levels, not confirmed bounces):**
- **Immediate overhead resistance cluster: ~266–267** — where the 10‑EMA (266.33), VWMA (266.61), and 50‑SMA (266.77) converge. A rally that fails here keeps the bearish tilt intact; a decisive reclaim would be the first bullish tell.
- **First support reference: ~246** — the Jan 20 close (246.03) and Jan 20 intraday low (242.76), the launch point of the prior advance.
- **Major support confluence: ~239–240** — the 200‑SMA (239.18) and Bollinger lower band (239.75) overlap here.

**Actionable guidance by stance:**
1. **Trend/momentum traders (short-term):** Momentum and structure favor the downside while price is capped by the 266–267 cluster. RSI at 39.59 is *not yet oversold*, so chasing an immediate bounce is premature; there is technical room toward the 246 and then 239–240 zones.
2. **Swing/position buyers (medium-term):** Best practice is to **wait for stabilization** rather than catch the falling knife — e.g., RSI turning back up through ~45–50, price reclaiming the 10‑EMA (~266), or a MACD histogram that stops deteriorating. The **239–240 confluence** is the higher‑conviction area to watch for a constructive entry *if* it holds.
3. **Long-term holders:** The setup is a *pullback within an uptrend* only as long as the 200‑SMA (~239) holds. A weekly close below ~239 would meaningfully damage the long‑term trend and warrant re‑evaluation.
4. **Risk management:** With ATR at 6.52 and rising, size positions down; use ATR‑based stops (~2× ATR ≈ $13) rather than tight fixed stops. Expect continued wide intraday ranges.

**Watch list / triggers:** (a) Volume on any bounce — a low‑volume drift up is a warning, a high‑volume reclaim of 266 is bullish; (b) RSI behavior near 40 (stabilize = constructive; break toward 30 = deeper correction); (c) MACD histogram — does it keep expanding negatively or flatten?

---

## 8. Key points summary

| Dimension | Indicator (2026-02-13) | Reading | Interpretation |
|---|---|---|---|
| Price | Close 255.32 (High 261.76 / Low 254.99) | −7.16% in 2 sessions from Feb 11 (275.01) | Sharp, high-volume reversal |
| Short-term trend | `close_10_ema` = 266.33 | Price **below** | Short-term trend down |
| Medium-term trend | `close_50_sma` = 266.77 (rolling over) | Price **below** | Intermediate trend flipped to resistance |
| Long-term trend | `close_200_sma` = 239.18 (rising) | Price **~6.7% above** | Primary uptrend still intact |
| 50/200 structure | 266.77 > 239.18 | Golden-cross regime | No death cross; bull structure holds |
| Momentum | `rsi` = 39.59 | Below 50, not oversold | Bearish, room to fall |
| Momentum trigger | `macd` 1.18 vs `macds` 1.19 | Histogram ≈ −0.01 | **Fresh bearish crossover** |
| Volatility | `atr` = 6.52 (rising) | Expanding | Wider ranges; size down |
| Volatility band | Boll middle 261.62 / UB 283.50 / LB 239.75 | Price below middle | Bearish half of envelope; LB ≈ 200-SMA |
| Volume | `vwma` = 266.61 | Price **~4.2% below** | Distribution confirmed |
| Key resistance | ~266–267 (10-EMA / VWMA / 50-SMA cluster) | Confluence | Caps near-term rallies |
| Key support | ~246 (Jan 20) then ~239–240 (200-SMA + Boll LB) | Confluence | Higher-conviction demand zone |

**Bottom line:** AAPL is in a volume-confirmed short-term downtrend inside a still-intact long-term uptrend. Momentum and trend signals are negatively aligned and *fresh* (MACD cross, RSI < 50, price below all short/medium averages and VWMA). The most prudent posture is **defensive/patient** — respect the ~266–267 cap for the bearish case, and look to the ~246 and especially ~239–240 (200-SMA + lower Bollinger confluence) zones for potential stabilization, confirming any bottom with rising volume and a recovering RSI/MACD histogram before committing.