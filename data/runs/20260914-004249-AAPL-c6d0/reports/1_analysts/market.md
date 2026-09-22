# AAPL Technical Analysis Report — As of 2026-01-09

**Resolved identity:** Apple Inc. (AAPL) — Technology / Consumer Electronics — Exchange: NMS.
**Analysis date:** 2026-01-09 (source of truth: verified market snapshot).

---

## 1. Price Action & Market Context

AAPL topped out in early December and has been in a persistent corrective decline that accelerated into January.

- **Peak close:** 285.41 on 2025-12-02 (intraday high 286.62 on the same row).
- **Latest close:** 258.67 on 2026-01-09 (verified snapshot).
- **Peak-to-current decline:** 285.41 → 258.67, a **−9.37%** move supported by those two concrete closes.
- **Sharp January leg:** the stock fell from 270.27 (2026-01-02) to 258.34 (2026-01-08) — **five consecutive lower closes** — before a marginal stabilization on 2026-01-09 (258.67, up +0.33 on the day).

The defining near-term character is a **short-term downtrend nested inside a longer-term uptrend**. The long-term structure (price above the 200 SMA, 50 SMA above 200 SMA) is still constructive, but the intermediate and short-term structure has clearly deteriorated.

---

## 2. Indicator Selection & Rationale

I selected a complementary set spanning trend, momentum, volatility, and volume — avoiding redundancy:

| Selected | Category | Why it fits this context |
|---|---|---|
| close_10_ema | Short-term trend | Captures the rapid January momentum shift / potential reversal pivot |
| close_50_sma | Medium-term trend | Defines the intermediate trend and now acts as overhead resistance |
| close_200_sma | Long-term trend | Confirms the still-intact structural bull market; key line in the sand |
| rsi | Momentum | Flags the oversold condition that raises bounce risk |
| macd / macds / macdh | Momentum | Confirms negative momentum and whether it is decelerating |
| boll / boll_ub / boll_lb | Volatility | Locates price at the lower band (mean-reversion zone) & measures band expansion |
| atr | Volatility/Risk | Sizes stops/positions given elevated volatility |
| vwma | Volume | Confirms whether the decline is volume-backed (distribution) |

---

## 3. Trend Analysis (Moving Averages)

- **Close 258.67 vs 10 EMA 264.63** → price is **below** the short-term average. The 10 EMA itself is falling sharply: 272.62 (2025-12-31) → 264.63 (2026-01-09).
- **Close 258.67 vs 50 SMA 271.84** → price is **well below** the medium-term average, and the 50 SMA has flattened/rolled (270.70 on 2025-12-26 → 271.84 on 2026-01-09) after rising for most of December.
- **Bearish short-term crossover:** the 10 EMA was still above the 50 SMA on 2026-01-02 (272.20 vs 272.02) but dropped below it by 2026-01-05 (271.17 vs 272.20). This 10/50 bearish cross is a classic short-term trend-break signal.
- **Long-term intact:** the 50 SMA (271.84) remains far **above** the 200 SMA (232.17), so **no death cross**. Price at 258.67 sits roughly **+11.4% above** the 200 SMA — the long-term uptrend is not threatened at current levels.

**Interpretation:** The near/medium-term trend is down; the long-term trend is up. This is a pullback/correction, not (yet) a structural breakdown.

---

## 4. Momentum Analysis (RSI + MACD)

**RSI = 27.27** (verified snapshot; 26.28 on 2026-01-08 was the low).

- RSI has collapsed from **75.25** (overbought, 2025-12-02) to **27.27** — a swing from overbought to **oversold (<30)** in about five weeks.
- This is the single most important nuance: momentum is decisively negative, **but the market is now stretched to the downside.** In a strong downtrend RSI can stay pinned low, so oversold alone is not a buy — it is a *warning against chasing shorts at the lows*.

**MACD:**
- **macd = −3.28**, **macds (signal) = −1.46**, **macdh = −1.82** (verified snapshot).
- The MACD line crossed **below** its signal around 2026-01-02 (macd −0.29 vs signal 0.45) and slid below zero afterward — a confirmed **bearish crossover**.
- The MACD line is still **falling faster than its signal** (macd −3.28 vs signal −1.46), i.e., the histogram is negative and momentum is still down.
- **Early hint of deceleration:** the histogram troughed at −1.84 (2026-01-08) and ticked up to −1.82 (2026-01-09). This is a very small flattening — worth watching, but not yet a reversal signal.

**Interpretation:** Momentum is bearish and confirmed, with the first faint sign of downside momentum no longer accelerating.

---

## 5. Volatility Analysis (Bollinger Bands + ATR)

- **Bollinger middle (20 SMA) = 269.83**, **upper = 281.41**, **lower = 258.26**.
- The close (258.67) is sitting **essentially on the lower band** (258.26) — a classic oversold/mean-reversion zone. In strong trends price can "ride the band," so this flags *bounce potential* rather than guaranteeing a reversal.
- **Band expansion:** the lower band fell from 267.69 (2025-12-31) to 258.26 (2026-01-09) and the bandwidth (UB−LB) widened to ~23.15 points (~8.6% of the middle). Expanding bands during a decline confirm the trend move and elevated volatility.
- **ATR = 4.39** (~1.7% of price). ATR has *declined* from ~5.5 in early December, so while still elevated, per-day range is moderating slightly. ATR remains the right tool for stop placement and position sizing.

---

## 6. Volume Confirmation (VWMA)

- **VWMA = 267.76**, and price (258.67) is **below** it → the volume-weighted average confirms the downside; recent selling is occurring on meaningful volume, not on thin tape.
- **Distribution evidence:** the January decline came with **rising volume** — 2026-01-06 = 52.35M, 2026-01-07 = 48.31M, 2026-01-08 = 50.42M — noticeably heavier than much of the December drift (~30–40M). Heavier volume on down days is characteristic of **distribution**, which argues against a "clean" immediate reversal.

---

## 7. Synthesis & Actionable Insights

AAPL presents a **bearish short-term / bullish long-term** picture with an oversold counter-trend bounce risk:

1. **Trend is down short-term.** Price is below the 10 EMA, 50 SMA, Bollinger middle, and VWMA, with a fresh 10/50 bearish cross. This favors selling rallies rather than buying dips *until* momentum stabilizes.
2. **But the tape is stretched.** RSI ~27 and price on the lower Bollinger band mean fresh short entries here have **poor reward/risk** — a snap-back bounce is a live probability. The MACD histogram flattening (2026-01-08 → 2026-01-09) is the first tentative sign of that.
3. **Key levels to watch:**
   - **Resistance/overhead:** 10 EMA ≈ 264.63, Bollinger middle ≈ 269.83, 50 SMA ≈ 271.84. A reclaim of the 10 EMA and then the 50 SMA would be the first evidence of a genuine reversal rather than a dead-cat bounce.
   - **Support:** Bollinger lower band ≈ 258.26; current close 258.67 is barely above it. A decisive close **below** the lower band with the bands still expanding would open continuation risk. The 200 SMA (232.17) is the deep structural floor.
4. **Confirmation checklist for a bounce/buy:** RSI reclaiming and holding above 30; MACD histogram turning positive; price closing back above the 10 EMA; a down-day on *drying* volume (selling exhaustion). None are present yet.
5. **Confirmation checklist for continuation/sell:** a close below the lower band (258.26); MACD histogram making new lows; continued heavy volume on red days.

**Risk management:** With ATR ≈ 4.39 (~1.7% of price), size positions accordingly and place stops beyond roughly 1–1.5× ATR from entry to avoid being stopped by normal noise.

**Net stance:** The weight of evidence is bearish across trend and momentum, but the oversold RSI and lower-band proximity make chasing downside here unattractive. The prudent posture is to **hold / stay neutral and wait for confirmation** — either a momentum reversal to go long, or a lower-band break to press short — rather than to buy an unconfirmed dip or short an oversold market.

> **Data note:** All exact OHLCV and indicator values above are taken from the verified market snapshot (latest row 2026-01-09). No conflicting values were observed between the raw price data pull and the snapshot.

---

## 8. Key Points Summary Table

| Dimension | Indicator | Latest Value (2026-01-09) | Signal | Interpretation |
|---|---|---|---|---|
| Price | Close | 258.67 | Down | 5 straight down closes into 2026-01-08; flat 2026-01-09 |
| Short trend | close_10_ema | 264.63 | Bearish | Price below; 10 EMA falling fast |
| Medium trend | close_50_sma | 271.84 | Bearish | Price below; 50 SMA flattening overhead |
| Long trend | close_200_sma | 232.17 | Bullish | Price ~+11.4% above; 50>200, no death cross |
| Momentum | rsi | 27.27 | Oversold | Down from 75.25 (2025-12-02); bounce risk |
| Momentum | macd / macds | −3.28 / −1.46 | Bearish | Below signal & below zero since ~2026-01-02 |
| Momentum | macdh | −1.82 | Bearish (easing) | Ticked up from −1.84; early deceleration hint |
| Volatility | boll / boll_ub / boll_lb | 269.83 / 281.41 / 258.26 | At lower band | Price 258.67 ≈ lower band; bands expanding |
| Volatility/Risk | atr | 4.39 | Elevated | ~1.7% of price; calibrate stops/size |
| Volume | vwma | 267.76 | Bearish | Price below VWMA; heavy down-day volume = distribution |

**Watch levels:** Resistance 264.63 (10 EMA) → 269.83 (Boll mid) → 271.84 (50 SMA). Support 258.26 (Boll lower) → 232.17 (200 SMA).

FINAL TRANSACTION PROPOSAL: **HOLD**