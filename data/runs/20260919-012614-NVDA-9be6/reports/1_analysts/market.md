# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date:** 2026-05-15 | **Sector:** Technology / Semiconductors | **Exchange:** NMS
**Latest verified close:** $224.81 (2026-05-15)

---

## 1. Market Context & Price Action

NVDA is in a **well-established, multi-timeframe uptrend** that has recently entered an **acceleration phase**, followed by a sharp one-day pullback on the analysis date.

**Verified OHLCV (2026-05-15):** Open 229.24 / High 230.97 / Low 223.73 / **Close 224.81** / Volume 180,977,600

Key price-path observations (all from tool output):
- **Late-March trough:** Close of **164.79 on 2026-03-30** (with RSI at just 34.0 — the most oversold reading in the window).
- **Rally leg:** Steady climb through April, then an acceleration from **196.05 (2026-05-05)** to **235.20 (2026-05-14)** — a gain of ~39.15 points / **+19.97% in 7 trading sessions**.
- **Reversal on the analysis date:** The stock gapped down from the prior close of 235.20, printed an intraday high of only 230.97, and closed at **224.81 — a one-day decline of 10.39 points, or −4.42%** on elevated volume (180.98M vs. 136–160M on the prior up-days).
- **Candle character:** The 5/15 down-body (228.24 open→224.81 close region) fully engulfs the prior day's 229.33 open, forming a **bearish engulfing-style reversal candle** at the top of an extended run. This is a classic near-term distribution warning after a stretched move.

---

## 2. Selected Indicators & Rationale (8 chosen)

I selected a **complementary, non-redundant** set spanning trend, momentum, volatility, and volume:

| # | Indicator | Category | Why it's relevant here |
|---|-----------|----------|------------------------|
| 1 | **close_10_ema** | Short trend/momentum | Captures the fast-moving trend and gives the first dynamic support level in an accelerating market. |
| 2 | **close_50_sma** | Medium trend | Confirms the intermediate trend and serves as the key "line in the sand" for the swing structure. |
| 3 | **close_200_sma** | Long trend | Validates the strategic bull structure (golden-cross regime) and long-term trend health. |
| 4 | **macd** | Momentum | Measures the underlying trend impulse; confirms whether the recent surge has genuine momentum behind it. |
| 5 | **rsi** | Momentum/overbought | Critical for flagging the overbought condition that preceded the 5/15 reversal and gauging whether cooling is a buyable dip. |
| 6 | **boll_ub** | Volatility/breakout | Identifies where price rode the upper band (overextension) — the mechanism behind the 5/15 pullback. |
| 7 | **atr** | Volatility/risk | ATR is expanding sharply; essential for sizing positions and setting realistic stops in a volatile tape. |
| 8 | **vwma** | Volume-weighted trend | Volume-weights the trend to distinguish genuine institutional participation from thin, noise-driven moves. |

*(Deliberately excluded: `macds`/`macdh` and `boll`/`boll_lb` to avoid redundancy, and `stochrsi`-type oscillators that would duplicate RSI's role.)*

---

## 3. Trend Analysis

### Trend structure — Bullish and aligned
The moving-average stack is in a textbook **bullish alignment**:

| Level | Value (2026-05-15) | Price relationship |
|---|---|---|
| close_10_ema | **218.44** | Price is ~2.9% **above** |
| close_50_sma | **192.63** | Price is ~16.7% **above** |
| close_200_sma | **185.53** | Price is ~21.2% **above** |

- **10 EMA > 50 SMA > 200 SMA**, and all three are rising — a healthy, layered uptrend.
- The **50 SMA sits above the 200 SMA**, confirming the market is in a **golden-cross regime** (long-term bull structure).
- Notably, the 10 EMA has surged from ~192.90 (4/20) to 218.44 (5/15) — a rapid steepening that signals a parabolic short-term advance and raises the odds of a mean-reversion pause (which is exactly what 5/15 delivered).

### Momentum — Strong but showing its first crack
- **MACD = 9.31**, **Signal = 7.47**, **Histogram = +1.84**. MACD crossed above zero around **2026-04-13/04-14** (from −2.48 on 4/6) and has been rising strongly since — the underlying impulse is firmly bullish.
- **RSI = 64.66** on 5/15, having collapsed from **76.72 on 5/14** (a fresh overbought extreme). Earlier the RSI hit **76.28 on 4/27** — so this is the **second overbought push in three weeks**, and the momentum oscillator has now cooled into neutral-bullish territory without breaking down.
- **Interpretation:** RSI cooling from >76 to ~65 in a single session, while MACD remains positive and rising, is consistent with a **healthy momentum reset inside an ongoing uptrend**, not yet a confirmed trend reversal.

### Volatility — Expanding rapidly
- **ATR = 7.48**, up sharply from **4.86 (4/22)** and **5.06 (4/20)** — roughly **+54% expansion in under a month**. As a share of price, ATR is ~3.3% of the close.
- **Bollinger Upper Band = 231.91**, expanding from 218.79 (5/11). On **5/14 the close of 235.20 pierced above the upper band** (band then ~229.87) — the classic "riding the band" overextension. On **5/15 the close (224.81) fell back inside the band**, resolving that stretch.
- **Bollinger middle = 209.82**; the band width is widening, confirming a high-volatility regime. Rising ATR + widening bands = **larger swings in both directions**, demanding wider stops and smaller position sizes.

### Volume — Warning sign on the reversal
- **VWMA = 212.67** and rising, with price ~5.7% above it — the **volume-weighted trend remains bullish**, meaning the advance had genuine volume support.
- **However**, the 5/15 down day carried **180.98M shares** — comparable to the 5/14 up day (180.78M) and above the 136–160M seen on several prior up-days. **Heavy volume on a down/reversal candle** is a distribution-style tell that argues for near-term caution.

---

## 4. Key Levels (derived strictly from tool values)

**Resistance:**
- **236.00** — 5/14 intraday high (highest high in the dataset)
- **231.91** — Bollinger Upper Band
- **230.97** — 5/15 intraday high

**Support:**
- **218.44** — 10 EMA (first dynamic support; a close below it would signal the short-term trend is cracking)
- **214.71** (5/8 close) / **216.12** (4/27 close) — prior breakout zone
- **212.67** — VWMA (volume-weighted trend floor)
- **209.82** — Bollinger middle band (~20 SMA)
- **192.63** — 50 SMA (major intermediate support, ~14% below spot)

---

## 5. Actionable Insights

1. **Primary bias remains constructive.** All trend indicators (10 EMA > 50 SMA > 200 SMA, price above VWMA, positive & rising MACD) point to a bull trend. Dips should be viewed as opportunities *while* the structure holds — but the 5/15 reversal argues for **patience rather than chasing**.

2. **The 5/15 candle is a tactical caution flag.** A bearish engulfing-style reversal on heavy volume after price pierced the upper Bollinger band and RSI reached 76 signals **near-term consolidation risk**. Do not initiate fresh momentum longs into strength above 230.

3. **Watch the 10 EMA (218.44) as the pivot.** 
   - A **hold/defense of ~218** on light volume keeps the uptrend intact and offers a preferred pullback entry.
   - A **decisive close below 218**, especially toward the VWMA (212.67) / Bollinger mid (209.82), would confirm a deeper mean-reversion leg and shift the tactical bias to neutral.

4. **Position sizing & stops must respect the higher ATR.** With **ATR = 7.48**, a reasonable volatility-based stop for a swing long entered near 225 would sit roughly **1.5–2× ATR below entry (~11–15 points)**, i.e., in the **~210–214 zone** — which conveniently aligns with the VWMA and the prior breakout shelf. Risk per share is large, so **size down**.

5. **Risk/reward is currently asymmetric against new longs at the highs.** Upside to resistance (236.00) is ~5% while ATR-driven risk is ~3.3% per day. Better to **wait for either (a) a controlled pullback into 218–213, or (b) a fresh breakout above 236 on strong volume** before adding exposure.

6. **Momentum divergence to monitor.** If price makes a new high above 235–236 but RSI fails to exceed its 5/14 peak of 76.72, that would form **bearish momentum divergence** — a strong signal to reduce/hedge.

---

## 6. Summary Table

| Dimension | Reading (2026-05-15) | Signal | Notes |
|---|---|---|---|
| **Close** | $224.81 | — | −4.42% vs 5/14 close (235.20); bearish reversal candle |
| **close_10_ema** | 218.44 | Bullish | Price ~2.9% above; first support & short-term trend gauge |
| **close_50_sma** | 192.63 | Bullish | Price ~16.7% above; intermediate uptrend intact |
| **close_200_sma** | 185.53 | Bullish | Price ~21.2% above; 50>200 = golden-cross regime |
| **MACD** | 9.31 (signal 7.47, hist +1.84) | Bullish | Positive & rising since ~4/13; impulse still strong |
| **RSI** | 64.66 | Neutral-Bullish | Cooled sharply from 76.72 (5/14) overbought peak |
| **Bollinger Upper** | 231.91 | Caution | Price pierced band 5/14 then fell back inside on 5/15 |
| **ATR** | 7.48 | High volatility | Up ~54% since 4/22; size positions smaller, wider stops |
| **VWMA** | 212.67 | Bullish | Price ~5.7% above; volume-weighted trend rising |
| **Volume (5/15)** | 180.98M | Caution | Heavy volume on a down day = distribution-style tell |

**Bottom line:** NVDA's **primary trend is up and technically healthy**, but the **2026-05-15 reversal on heavy volume after an overbought, band-riding advance** introduces meaningful short-term consolidation risk. The tactical plan: **stay constructive on the trend, avoid chasing at the highs, buy controlled dips toward the 218 (10 EMA) / 213 (VWMA) zone, and use ATR-scaled stops with reduced size** given the elevated volatility regime.