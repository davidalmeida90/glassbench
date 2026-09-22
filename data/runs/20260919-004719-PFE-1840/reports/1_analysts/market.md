I now have the full data set. Here is my detailed analysis.

---

# PFE (Pfizer Inc.) — Technical Analysis Report
**Analysis date:** 2025-11-14 | **Exchange:** NYQ | **Sector:** Healthcare / Drug Manufacturers – General
**Verified latest close:** $23.83 (O 24.41 / H 24.51 / L 23.74), Volume 96,507,600

*Source of truth: the verified market snapshot for 2025-11-14. The OHLCV row from `get_stock_data` (O 24.41, H 24.51, L 23.74, C 23.83, V 96.5M) matches the snapshot exactly — no discrepancy to flag.*

---

## 1. Market Context: A Wide, Mean-Reverting Range

PFE is not in a clean directional trend. Over the trailing ~12 months the stock traded from the mid-$24s (Nov 2024) down to a low of **$19.46** (close, 2025-04-10) and back up. The long-term average is essentially flat, confirming a **range/mean-reversion regime** rather than a sustained trend:

- **close_200_sma = 22.61**, and it has barely moved in two months (22.62 on 2025-09-15 → 22.61 on 2025-11-14). A flat 200-SMA is the signature of a sideways market.
- The recent two legs have been sharp, news-style impulses rather than steady trends:
  - **2025-09-30 → 2025-10-01:** a violent re-rating — close ran 22.29 → 23.81 → 25.43 (Oct 3 high close 25.58) on volumes of 164.9M and 150.9M.
  - **2025-10-06 → 2025-10-16:** a full retracement back down to 22.64.
  - **2025-11-10 → 2025-11-13:** a *second* impulse — close 23.19 → 24.26 → 24.60 → 24.52 on elevated volume (140–150M).
  - **2025-11-14:** a sharp give-back to 23.83 on 96.5M.

The takeaway: **momentum bursts are being sold into**, and the market has repeatedly rejected the low-$25s. This is the key context for every signal below.

---

## 2. Trend Structure — Bullish Alignment, but Compressed

| Relationship | Value (2025-11-14) | Read |
|---|---|---|
| Close vs 10 EMA | 23.83 vs **23.73** | Price ~$0.10 above short EMA — barely holding |
| Close vs 50 SMA | 23.83 vs **23.22** | +2.6% above medium-term trend |
| Close vs 200 SMA | 23.83 vs **22.61** | +5.4% above long-term trend |
| 50 SMA vs 200 SMA | 23.22 > 22.61 | 50 above 200 = constructive (golden-cross posture) |

- The **stack is bullish** (price > 10 EMA > 50 SMA > 200 SMA), which favors dip-buyers over trend-followers.
- **But the moving averages are tightly clustered** ($22.6–$23.7), reflecting the same "flat 200-SMA" observation — this is not a strongly trending tape. The 50-SMA itself has oscillated in a narrow $23.13–$23.25 band for weeks, i.e., it is *not* accelerating.
- The **10 EMA (23.73)** is the line in the sand for the short-term bullish impulse. Price closed fractionally above it on 2025-11-14, so the up-thrust from Nov 11 is *technically intact but fragile.*

---

## 3. Momentum — Fresh Bullish Cross, Now Cooling

**MACD (0.23) vs Signal (0.08), Histogram (0.15):**
- The **MACD line crossed above its signal** around 2025-11-06/11-10 (histogram flipped positive on 11-06 at +0.005, expanding to +0.19 on 11-13).
- The **MACD line crossed above zero on 2025-11-11** (from −0.044 on 11-10 to +0.054), a classic bullish momentum confirmation.
- **However, the histogram peaked on 2025-11-13 (0.191) and shrank to 0.153 on 2025-11-14** — an early warning that the up-momentum is decelerating, consistent with the price give-back that same day.

**RSI (55.59):**
- RSI collapsed from **68.80 (11-12)** and **67.32 (11-13)** to **55.59 (11-14)** — a ~13-point single-day drop in momentum, not matched by an equivalent price drop (close only fell from 24.52 to 23.83). This is momentum fading faster than price — a caution flag.
- Context: RSI hit **74.4 on 2025-10-01** at the prior spike and was never able to hold overbought — a direct precedent that **overbought RSI readings in this name get sold.**
- RSI is now mid-range (neither overbought nor oversold), meaning **no fresh directional edge from RSI alone** — it supports a "neutral until the range breaks" stance.

---

## 4. Volatility — Bands Expanding, ATR Rising

- **Bollinger:** middle **23.28**, upper **24.41**, lower **22.15**. Band width ≈ **$2.26 (~9.7% of the mid-band)** and it has widened sharply week-over-week (upper band moved 23.37 → 24.41 between 11-10 and 11-14). Expanding bands = volatility regime shifting up.
- On **2025-11-12 and 11-13**, closes (24.60, 24.52) pushed **above the upper band** — a classic overbought/breakout-stretch signal. On 11-14 the close returned *inside* the band (23.83 below UB 24.41), i.e., the stretch is being worked off. **This is the "ride the band, then revert" pattern that has punished chasers in this name.**
- **ATR = 0.58** (~2.4% of price) and rising from ~0.42 in late October. Higher ATR supports **wider stops and smaller position sizes** right now.

---

## 5. Volume — Confirmation for the Move, but Watch the Spike Skew

- **VWMA = 23.34**, slightly *below* the 23.83 close, so price is above the volume-weighted average — mildly constructive, and VWMA has turned up (22.92 on 11-03 → 23.34 on 11-14).
- The Nov 11 up-leg came on **heavy, above-average volume** (150M, 140M, 123M vs a typical 35–50M), which is genuine confirmation of demand.
- Caveat: this name has produced **violent single-day volume spikes** that distort VWMA (e.g., 349.9M on 2025-03-21, 164.9M on 2025-09-30). VWMA should be read *directionally*, not as a precise line.

---

## 6. Key Levels & Scenarios (all levels derived from tool output)

**Resistance / upside triggers**
- **$24.41** — Bollinger upper band
- **$24.52–$24.60** — Nov 12–13 closes (the immediate rejection shelf)
- **$25.43–$25.58** — Oct 1–3 spike highs (the "ceiling" that must break to change regime)

**Support / downside triggers**
- **$23.7** — 10 EMA (first line of defense)
- **$23.2–$23.3** — a tight *cluster*: 50 SMA (23.22) + Bollinger middle (23.28) + VWMA (23.34). This is the pivotal zone.
- **$22.61** — 200 SMA (long-term trend anchor)
- **$22.15** — Bollinger lower band

**Scenario map**
- **Bullish continuation:** Requires a *daily close back above $24.41–$24.60* on strong volume. Only a decisive break and hold above **$25.58** truly escapes the year-long range.
- **Base case (range, mild bullish bias):** Price chops between the **$23.2 pivot cluster and $24.6**, with the Nov 14 pullback being a normal cool-off after a two-day stretch above the upper band. Alignment of price > 50 SMA > 200 SMA keeps the odds slightly tilted to buyers.
- **Bearish turn:** A daily close *below ~$23.2* (losing 50 SMA + mid-band + VWMA simultaneously) opens the door to **$22.61 (200 SMA)** and then **$22.15 (lower band)**. Note the MACD histogram rollover and RSI fade on 11-14 are *early* evidence favoring this scenario if $23.2 gives way.

---

## 7. Actionable Insights

1. **Do not chase.** Both prior impulses in this range were rejected near the upper band/high-$25s. Entering at $24+ has repeatedly been the losing side; the risk/reward is better on pullbacks.
2. **Preferred entry zone: $23.2–$23.4** (50 SMA / mid-band / VWMA cluster), with confirmation that the 10 EMA ($23.73) is reclaimed on any bounce. This aligns with the bullish MA stack and the rising VWMA.
3. **Risk management:** With ATR at **0.58**, use ~1–1.5× ATR stops. A long from ~$23.3 could stop near **$22.60–$22.70** (below the 200 SMA) — about a 0.6–0.7 ($1.0–1.2 ATR) cushion. Size positions for ~2.4% daily range.
4. **Take-profit discipline fits this regime:** scale out toward **$24.41–$24.60** and again at **$25.4–$25.6**, rather than assuming a breakout.
5. **Invalidation levels are clean:** longs are wrong on a close below **$23.2**; the range is broken to the upside only on a close above **$25.58**.
6. **Dividend note:** PFE goes ex-dividend quarterly (latest **$0.43 ex-date 2025-11-07**); the high yield (~7%) cushions the downside but the price is ex-div-adjusted in the series above.

---

## 8. Selected Indicators & Rationale

| Indicator | Value (11-14) | Why it was chosen for PFE |
|---|---|---|
| **close_10_ema** | 23.73 | Best short-term read; shows the Nov 11 impulse is barely holding. Fast entry/exit trigger. |
| **close_50_sma** | 23.22 | Medium-term trend/support; part of the pivotal $23.2 pivot cluster. |
| **close_200_sma** | 22.61 | Flat 200-SMA confirms range regime; key longer-term support and golden-cross posture gauge. |
| **macd** | 0.23 | Confirms the fresh bullish cross above signal and zero line on Nov 11. |
| **rsi** | 55.59 | Shows momentum fading faster than price; mid-range = no edge, and precedent of failed overboughts. |
| **boll_ub** | 24.41 | Captures the overbought stretch (Nov 12–13 closings above band) and the first resistance. |
| **atr** | 0.58 | Rising volatility → sets stop distance and position sizing. |
| **vwma** | 23.34 | Volume-weighted confirmation that the up-move has real participation; price above VWMA. |

*(MACD signal (0.08), MACD histogram (0.15), and the lower band (22.15) were also examined as sub-components to confirm the crossover and the downside boundary.)*

---

## 9. Key Points Summary Table

| Dimension | Reading (2025-11-14) | Interpretation |
|---|---|---|
| Latest close | $23.83 (O 24.41 / H 24.51 / L 23.74) | Pulled back 2.8% from 24.52 |
| Trend stack | Close > 10EMA(23.73) > 50SMA(23.22) > 200SMA(22.61) | Bullish alignment, but compressed |
| 50 vs 200 SMA | 23.22 > 22.61 | Constructive (golden-cross posture) |
| 200 SMA slope | ~flat (22.62→22.61 over 2 mo) | Range/mean-reversion regime |
| MACD / Signal / Hist | 0.23 / 0.08 / 0.15 | Bullish cross Nov 11; histogram cooling |
| RSI | 55.59 (from 68.8 on 11-12) | Momentum fading faster than price |
| Bollinger | mid 23.28, UB 24.41, LB 22.15 | Bands expanding; Nov 12–13 closed above UB |
| ATR | 0.58 (~2.4% of price), rising | Wider stops, smaller size |
| VWMA | 23.34 | Price above VWMA — up-move had volume |
| Immediate resistance | 24.41 / 24.52–24.60 / 25.43–25.58 | Chasers have been rejected here twice |
| Immediate support | 23.7 / 23.2–23.3 cluster / 22.61 / 22.15 | 23.2 pivot is the decision line |
| Bullish trigger | Close > 24.60; breakout > 25.58 | Range escape only above 25.58 |
| Bearish trigger | Close < 23.2 | Targets 22.61 then 22.15 |
| Bias | Mildly bullish range / buy-dips | Favor entries $23.2–23.4, fade $24.5+ |

**Bottom line:** PFE is a high-yield, range-bound large-cap that just produced a second failed push toward the upper Bollinger band. The moving-average stack is bullish and volume confirms real demand, but the MACD histogram rollover, the sharp RSI fade, and the long history of upper-band rejections argue **against chasing strength above $24.4**. The highest-probability, best-risk play is to **buy the $23.2–$23.4 pivot cluster with a stop below the 200 SMA (~$22.6)** and sell into the $24.4–$25.6 band, respecting a clean invalidation on a close below $23.2.