# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date: 2026-05-15 | Exchange: NMS | Sector: Technology / Semiconductors**

All figures below are drawn from the verified market snapshot (source of truth) and the indicator time series retrieved for NVDA. Derived arithmetic (e.g., point-to-point changes) is explicitly labeled as computed.

---

## 1. Market Context & Price Structure

NVDA is trading in a **well-established, multi-month uptrend** that resumed after a Q1 correction. Using the verified recent-closes series:

- The swing low in the window was the **2026-03-30 close of 164.79**.
- The rally then carried to the **2026-05-14 close of 235.20** — a computed advance of roughly **+42.7%** from that pivot.
- The most recent session, **2026-05-15**, closed at **224.81** (O 229.24 / H 230.97 / L 223.73 / V 180,977,600), a pullback of about **−4.4%** from the 5/14 close (computed).

So the tape shows a strong, accelerating advance that ran into an **overbought-and-extended condition on 5/14**, followed by a sharp single-day give-back. This is a classic "trend intact, but near-term stretched" setup.

---

## 2. Indicator Selection & Rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume — deliberately avoiding redundancy (e.g., I used RSI only, not a second oscillator; MACD line only rather than stacking MACD line + signal + histogram all as separate "views" for selection purposes, though I read the histogram from the snapshot):

| Indicator | Category | Why it fits this context |
|---|---|---|
| **close_10_ema** | Trend (short) | Captures the fast momentum shift and immediate dynamic support in a volatile advance |
| **close_50_sma** | Trend (medium) | Confirms the intermediate trend and defines pullback support |
| **close_200_sma** | Trend (long) | Strategic trend benchmark; establishes the golden-cross regime |
| **macd** | Momentum | Confirms trend momentum and zero-line/crossover regime |
| **rsi** | Momentum | Flags overbought/oversold extremes and momentum cooling |
| **boll_ub** | Volatility | Identifies stretch/breakout zones in a trending name |
| **atr** | Volatility | Sizes stops and positions in an expanding-volatility regime |
| **vwma** | Volume | Validates the trend with volume-weighted price |

---

## 3. Indicator-by-Indicator Detail

### Trend: Full bullish stack
- **10 EMA = 218.44**, **50 SMA = 192.63**, **200 SMA = 185.53**. The ordering **Price (224.81) > 10 EMA > 50 SMA > 200 SMA** is a textbook bullish alignment.
- The **50 SMA sits well above the 200 SMA** (192.63 vs 185.53), confirming a **golden-cross regime**, and both are rising steadily (50 SMA climbed from 184.96 on 3/16 to 192.63 on 5/15; 200 SMA from 177.21 to 185.53). The 50 SMA has been rising every session in the window — an unambiguous intermediate uptrend.
- The 10 EMA has risen from ~173.20 (3/30) to 218.44 (5/15), tracking the rally closely; the 5/15 close of 224.81 remains **above** the 10 EMA, so the short-term uptrend is not yet broken.

### Momentum: Strong but cooling
- **MACD = 9.31**, having crossed **above zero around 2026-04-10** (macd flipped from −0.78 on 4/9 to +0.13 on 4/10) and rising steadily since. MACD hit a local peak of ~9.22 on 5/14 and eased only marginally. The snapshot's **MACD signal = 7.47**, so the **histogram (+1.84)** remains positive — momentum is still bullish, though the histogram is worth watching for contraction.
- **RSI = 64.66** on 5/15, down sharply from **76.72 on 5/14** (overbought). The retreat from >70 to the mid-60s represents a **healthy momentum reset rather than a breakdown** — RSI remains comfortably above the 50 midline, consistent with an ongoing uptrend.
- Note the RSI pattern earlier: **76.28 on 2026-04-27** cooled to ~51 by 2026-05-05, then re-accelerated to 76.72 by 5/14. This shows RSI is capable of working off extremes via time/sideways digestion without breaking the trend.

### Volatility: Expanding, price now inside the band
- **Bollinger upper band = 231.91**, middle = **209.82**, lower = **187.73**.
- On **2026-05-14 the close (235.20) exceeded the upper band (229.87)** — a band breakout ("riding the band"), which in strong trends often signals continuation but also precedes mean-reversion. On **5/15 the close (224.81) fell back inside the band**, below the 5/15 upper band of 231.91 — consistent with a **near-term stretch/pullback** read.
- **ATR = 7.48** (≈3.3% of price), up from ~6.16 on 2026-05-05 — **volatility is rising**, so stops and position sizes should be adjusted accordingly.

### Volume: Trend confirmed
- **VWMA = 212.67**, and price (224.81) is **above VWMA** — the volume-weighted average confirms that recent buying is occurring at higher prices, i.e., the advance is being supported by volume. VWMA has risen monotonically from ~174.67 (4/6) to 212.67 (5/15).

---

## 4. Synthesis & Scenarios

**Base case (trend continuation):** The primary trend is up on every timeframe (10 EMA > 50 SMA > 200 SMA, MACD > 0, RSI > 50, price > VWMA). The 5/15 pullback looks like a normal digestion of an overbought spike. As long as price holds above the **10 EMA (~218.4)** and the **Bollinger middle / VWMA cluster (~210–213)**, the uptrend structure remains valid.

**Bullish continuation triggers:**
- Reclaim of the **5/14 high of 236.00** would confirm the pullback is complete and re-open upside.
- A close back **above the upper band (231.91)** would re-establish the "riding the band" breakout.

**Caution / pullback triggers:**
- **RSI falling below 50** and/or **MACD histogram turning negative** would warn momentum is rolling over.
- A **close below the 10 EMA (218.44)** raises the odds of a test of the **VWMA / Bollinger middle zone (≈210–213)**; a break there points to the **50 SMA (192.63)** as the deeper trend support.

**Key levels (verified values):**
- Resistance: **236.00** (5/14 high), **231.91** (upper band), **230.97** (5/15 high)
- Support: **218.44** (10 EMA), **212.67** (VWMA) / **209.82** (Boll middle), **192.63** (50 SMA), **185.53** (200 SMA)

---

## 5. Actionable Insights

1. **Stay biased long while above the 10 EMA (218.44).** The stack and momentum regime favor trend-following on pullbacks rather than counter-trend shorts.
2. **Use ATR (7.48) for risk.** A volatility-scaled stop of ~1.5×ATR (~11 points) below entry is reasonable; tighten if ATR keeps expanding.
3. **Watch the MACD histogram.** At +1.84 it's positive but should be monitored for contraction — a flip to negative would be an early momentum warning.
4. **Treat 210–213 (VWMA / Boll middle) as the first higher-conviction re-entry zone** if the pullback deepens; the 50 SMA (192.63) is the trend's last line of defense.
5. **Don't chase the 5/15 low.** RSI at 64.66 is neutral-positive, leaving room for either a resumption or further sideways digestion — wait for a reclaim of 231.91/236.00 to confirm the uptrend reasserting.

---

## 6. Key Metrics Summary

| Metric | Value (2026-05-15) | Interpretation |
|---|---:|---|
| Close | 224.81 | Pulled back −4.4% from 5/14 (computed) |
| Open / High / Low | 229.24 / 230.97 / 223.73 | Reversal day, closed near lows |
| Volume | 180,977,600 | Elevated; heavy supply on pullback |
| 10 EMA | 218.44 | Short-term support; price above it |
| 50 SMA | 192.63 | Rising; intermediate trend up |
| 200 SMA | 185.53 | Rising; long-term trend up |
| Golden cross | 50 SMA > 200 SMA | Bullish regime confirmed |
| MACD | 9.31 | Positive, above signal (7.47) |
| MACD signal | 7.47 | Histogram +1.84, still bullish |
| RSI | 64.66 | Cooled from 76.72; still > 50 |
| Boll middle | 209.82 | Dynamic benchmark |
| Boll upper | 231.91 | Price fell back inside band on 5/15 |
| Boll lower | 187.73 | Oversold reference |
| ATR | 7.48 | Rising volatility (~3.3% of price) |
| VWMA | 212.67 | Price above; volume confirms trend |

**Overall stance:** **Bullish trend, near-term overbought/consolidating.** The dominant trend remains clearly up, but the 5/14 overbought spike and 5/15 reversal argue for caution on chasing strength. Favor buying pullbacks toward 218 / 210–213 while the structure holds, with 192.63 (50 SMA) as the trend's key line in the sand.

*Discrepancy check: The verified snapshot and the indicator series are mutually consistent (e.g., close_10_ema 218.44, RSI 64.66, ATR 7.48 all match). No conflicts requiring reconciliation were found.*