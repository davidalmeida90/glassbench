# NVDA (NVIDIA Corporation) — Technical Analysis Report
**Analysis date:** 2026-09-21 · **Exchange:** NMS · **Sector:** Technology / Semiconductors
**Verified snapshot close:** $224.87 (O 222.93 / H 225.50 / L 221.56)

---

## 1. Data Integrity Notes (read first)

- Every OHLCV and indicator value below is taken from the **verified market snapshot** for 2026-09-21, which agrees exactly with the raw OHLCV series for that date. No conflicts were found between tools.
- **Volume caveat:** the 2026-09-21 snapshot volume of **37,304,852** is roughly one-third to one-quarter of the typical recent session (most sessions in Aug–Sep printed between ~75M and ~195M, with an outlier of 298.9M on 2026-08-27). This strongly suggests a **partial / incomplete session**. Treat the 9/21 volume print and any single-day volume inference from it as unreliable; VWMA (a multi-day weighted average) is only marginally affected.
- **Corporate actions:** $0.25 dividends with ex-dates 2026-06-04 and 2026-09-10 (≈0.1% each). Immaterial to trend structure but worth noting for adjusted-vs-raw comparisons.

---

## 2. Indicator Selection & Rationale

I selected **8 complementary indicators** spanning trend, momentum, volatility, and volume, deliberately avoiding redundancy (e.g., no RSI + StochRSI pairing; no MACD histogram alongside MACD + signal, since the histogram is fully derived from those two).

| # | Indicator | Latest value (9/21) | Why it was chosen for this context |
|---|---|---|---|
| 1 | `close_10_ema` | **219.71** | NVDA just completed a 5-session, ~+6.6% impulse off the 9/14 low. The 10 EMA is the fastest reliable read on whether that thrust is still intact or fading. |
| 2 | `close_50_sma` | **214.35** | Medium-term trend spine and the most practical invalidation level for the current advance. Also rising every session since mid-August (205.89 on 8/10 → 214.35 on 9/21). |
| 3 | `close_200_sma` | **198.24** | Long-term regime benchmark. Confirms the structural bull trend and is the anchor of the 50/200 relationship. |
| 4 | `macd` | **1.29** | Captures the direction of medium-term momentum; currently in a recovery phase from a negative reading as recently as 2026-07-31 (−1.94). |
| 5 | `macds` | **1.51** | Needed as the crossover trigger line — the MACD/signal pair is the single most actionable momentum signal right now (see §4). |
| 6 | `rsi` | **56.50** | Neutral-zone momentum gauge with room in both directions, plus divergence detection. |
| 7 | `atr` | **6.23** | Volatility is compressing (down from 7.65 on 8/28). Essential for stop placement and position sizing. |
| 8 | `vwma` | **221.12** | Volume-weighted confirmation. Especially valuable here because the 2026-08-27 volume spike (298.9M) can distort simple averages. |

*Supplemental note:* I also reference the snapshot's Bollinger values (**mid 219.24, upper 232.28, lower 206.19**) purely as fixed price levels; they were not selected as separate indicators to avoid duplicating the 20-period mean already implicit in the 10 EMA / 50 SMA framework.

---

## 3. Trend Structure — Bullish Stack, But a Visible Supply Ceiling

**Long term (200 SMA): unambiguously bullish.**
- Price is **$26.63 (+13.4%) above** the 200 SMA at 198.24.
- The 200 SMA has risen every single session in the observed window (192.39 on 7/23 → 198.24 on 9/21), i.e., a persistently positive long-term slope, not a flattening one.
- The **50 SMA sits $16.11 above the 200 SMA**, and the spread has been widening (it was ~$16.75 on 7/23 → dipped to ~$13.26 on 8/10 → ~$16.11 now). This is a firmly established golden-cross regime, not a fresh/unconfirmed one.

**Medium term (50 SMA): bullish and accelerating.**
- The 50 SMA bottomed around 205.42 on 2026-08-04 and has climbed monotonically to 214.35. Price has closed above it on **every session since 2026-09-14**, and is currently 4.9% above it.
- Structurally important: from the 2026-07-29 closing low of **189.80**, NVDA has recovered to 224.87 (+18.5% on closes). That recovery also established a sequence of **higher closing lows** — 208.25 (8/24) → 210.96 (9/14) — which is the textbook signature of buyers defending progressively higher ground.

**Short term (10 EMA): bullish, freshly reclaimed.**
- Price ($224.87) is 2.3% above the 10 EMA ($219.71). The 10 EMA bottomed at **216.14 on 2026-08-24** and then at **217.39 on 2026-09-16**, and is now turning back up — a shallow "V" rather than a rollover.
- The last five closes are a clean ascending run: 212.17 (9/15) → 213.90 → 219.34 → 222.27 → 224.87 (9/21). Note that 9/21's close is the **highest close since 2026-09-04 (230.10)**, so this rally is now within striking distance of the September highs.

**The problem: a well-defined supply band at 227.7–230.1.**
Since late August, three separate attempts have stalled in the same zone:
- 2026-08-27 close **227.73** (on 298.9M shares — the largest volume in the window) — immediately rejected, next close 217.31.
- 2026-09-03 close **228.19**, 2026-09-04 close **230.10** — rejected, gave back to 210.96 by 9/14.
- Above that, the **232.28 upper Bollinger band** and the May 2026 closing high of **235.20** (intraday high 236.00 on 2026-05-14) form the next structural ceiling.

So we have a bullish trend and a bullish short-term impulse running directly into a zone that has already turned back two advances. That tension is the core of the setup.

---

## 4. Momentum — MACD Is the Key Tell Right Now

**MACD/signal state (verified):** MACD **1.29**, Signal **1.51**, Histogram **−0.22** (derived; snapshot confirms −0.22).

The MACD line crossed **below** its signal on 2026-09-10 (histogram flipped negative at −0.13) and the histogram then troughed at **−1.57 on 2026-09-16**. Since then it has narrowed on three consecutive sessions:

| Date | MACD | Signal | Histogram (derived) |
|---|---:|---:|---:|
| 2026-09-14 | 1.60 | 2.81 | −1.21 |
| 2026-09-15 | 0.89 | 2.43 | −1.54 |
| 2026-09-16 | 0.46 | 2.03 | −1.57 ← trough |
| 2026-09-17 | 0.55 | 1.74 | −1.18 |
| 2026-09-18 | 0.86 | 1.56 | −0.71 |
| **2026-09-21** | **1.29** | **1.51** | **−0.22** |

The MACD line has risen +0.83 over two sessions while the signal has fallen from 2.03 to 1.51. The gap is now only 0.22. **Mechanically, if this pace holds for one to two more sessions, MACD will cross back above its signal** — a fresh bullish trigger. This is the most time-sensitive observation in the report: the setup is *pre-crossover*, not post-crossover.

**RSI at 56.50 — neutral with headroom.** Key path:
- Oversold-ish trough of **37.97 on 2026-07-29** (marking the price low of the period).
- Overbought-adjacent peaks of **64.42 (8/7)**, **63.20 (8/13)**, and **60.39 (9/4)**.
- Pullback trough of **44.07 on 2026-09-14**, now recovered through 46.89 → 51.87 → 54.36 → **56.50**.

Two nuances:
1. RSI is **not** overbought — there is roughly 13–14 points of room before the 70 threshold. In a strong trend that matters: this rally does not yet have an "overbought excuse" to reverse.
2. There is a **mild bearish divergence in the rear-view mirror**: price made a higher close on 2026-09-04 (230.10) than on 2026-08-14 (224.91), but RSI made a *lower* peak (60.39 vs 63.04). That divergence was followed by the 9/8–9/14 pullback to 210.96. It has now played out. Track whether a **new** divergence forms if price retests 227–230 with RSI below ~60 again — that would be a meaningful warning.

---

## 5. Volatility — Compression That Argues for an Expansion Move

- **ATR: 6.23**, down from **7.65 on 2026-08-28** and **7.48 on 2026-09-08** — roughly an 18.6% contraction in average true range in under four weeks.
- ATR of 6.23 equates to **~2.8% of price** — still a genuinely volatile large cap, but the declining trend is the story.
- **Bollinger bandwidth: (232.28 − 206.19) / 219.24 = ~11.9%** of the mid-band, i.e., moderately narrow. Price at 224.87 sits in the **upper third** of the band, above the mid (219.24) but with 3.3% of room to the upper band.

**Interpretation:** simultaneous ATR compression and a squeeze in Bollinger bandwidth, occurring while price pushes against a defined resistance shelf, is the classic precondition for a **range expansion**. Direction is not pre-determined, but the *magnitude* likely will be. Plan for a decisive break rather than a slow grind.

**Risk framing using ATR:**
- 1× ATR below the close = **218.64** (essentially the 10 EMA at 219.71 — a nice coincidence that reinforces that zone).
- 2× ATR below = **212.41**, which sits just above the 9/14 swing close of 210.96 and above the 50 SMA at 214.35.

---

## 6. Volume Confirmation — VWMA Is the Quiet Bullish Input

- **VWMA at 221.12** vs. close 224.87 → price is **1.7% above** the volume-weighted benchmark.
- Critically, VWMA has been **rising for two weeks**: 219.66 (8/24) → 219.19 (8/27, the 298.9M spike day) → 219.42 (8/31) → 220.48 (9/8) → **221.12 (9/21)**. It did *not* break down during the 9/8–9/14 dip, and it is now making new local highs.

This is meaningful because a volume-weighted average is harder to lift than a simple average. The fact that VWMA is rising while price recovers means the **recent up-moves are being transacted at heavier volume than the down-moves** — genuine accumulation characteristics rather than a low-volume drift.

**Volume evidence to weigh, with the caveat in §1:**
- **2026-08-27:** 298.9M shares on a +7.1% close-to-close move (209.43 → 227.73), then an immediate give-back to 217.31 on 8/28. Classic blow-off/climax behavior at the top of the range.
- **2026-09-18:** 189.7M shares on a +1.34% up-day (219.34 → 222.27) — the heaviest participation since the 8/27 event, and notably on the **up** side. Bullish tell.
- **2026-09-14:** 132.3M shares on the −3.36% down-day (218.29 → 210.96) — selling pressure was present but the market absorbed it within four sessions.
- **2026-09-21:** 37.3M (partial session — do not annualize or extrapolate).

---

## 7. Actionable Playbook

### Scenario A — Bullish continuation (primary bias)
**Trigger:** A daily close **above 227.73** (the 8/27 rejection close), ideally with the MACD line crossing above its signal (needs only ~0.22 more convergence) and RSI pushing into the low 60s.
**Confirmation stack:** price > VWMA (221.12) > 10 EMA (219.71) > 50 SMA (214.35), with MACD histogram flipping positive.
**Targets:** 230.10 (9/4 close) → **232.28** (upper Bollinger) → **235.20 / 236.00** (May 2026 closing and intraday highs — the top of the entire multi-month range).
**Invalidation:** a close back below 219.71 (10 EMA) would negate the impulse; a close below 214.35 (50 SMA) would break the medium-term structure.

### Scenario B — Range-bound grind / rejection at supply
**Watch for:** a third rejection in the 227–230 zone, especially if accompanied by RSI failing to exceed ~62 (repeating the 8/14-vs-9/4 divergence pattern) or by a heavy-volume down-day.
**Implication:** the mult-month range (roughly 189.80 low close on 7/29 to 235.20 high close on 5/14) stays in force. Mean-reversion toward the 10 EMA/50 SMA would be the expectation, with 219–221 (10 EMA + VWMA confluence) as the first magnet and 214.35/212.41 (50 SMA + 2×ATR) as the second.

### Scenario C — Trend failure (lower probability given the stack)
**Trigger:** a decisive close below the **50 SMA at 214.35**, which would also break the 9/14 swing low of 210.96 on a closing basis.
**Next references:** 208.25 (8/24 close), then the 200 SMA at 198.24 as the long-term line in the sand.

### Risk management specifics
- **Stop placement:** with ATR at 6.23, a stop 1×ATR below an entry at ~225 lands at **218.6**; 2×ATR lands at **212.4**. The 2×ATR stop sits below the 50 SMA at 214.35, which is a defensible structural level.
- **Position sizing:** at ~2.8% daily ATR, risk per share is materially higher than the typical mega-cap. Size positions so that a 2-ATR adverse move is tolerable; the compressed ATR means the *current* sizing window is favorable relative to the 7.5–7.8 ATR readings of early August.
- **Do not chase:** the entry quality is best either (a) on a confirmed breakout close above 227.73, or (b) on a pullback to the 219.71/221.12 confluence that holds.

---

## 8. Risks, Caveats, and What Would Change the View

1. **Resistance has already won twice.** The 227.7–230.1 shelf produced two failed advances (8/27 and 9/3–9/4). A third failure would be materially more damaging to the bullish thesis than the prior two.
2. **MACD is still below signal.** The bullish crossover is *anticipated*, not confirmed. Momentum could stall at the 225–230 shelf and re-widen the negative histogram instead.
3. **Volume data for 9/21 is incomplete** (37.3M vs. a typical 75–195M). No volume-based conclusion should rest on that single print.
4. **ATR compression cuts both ways.** It argues for an expansion, but expansions resolve in whichever direction the range breaks.
5. **No claim of historical support/resistance "bounces" is made here** beyond the specific dated closes cited (189.80 on 7/29, 208.25 on 8/24, 210.96 on 9/14, 224.91 on 8/14, 227.73 on 8/27, 228.19 on 9/3, 230.10 on 9/4, 235.20 on 5/14, 236.00 intraday on 5/14) — all directly sourced from tool output.

---

## 9. Key Levels & Indicator Summary Table

| Category | Indicator / Level | Value (2026-09-21) | Signal | Interpretation |
|---|---|---:|---|---|
| Price | Verified close | **224.87** | — | Highest close since 9/4 (230.10) |
| Trend (LT) | `close_200_sma` | **198.24** | Bullish | Price +13.4% above; slope rising every session in window |
| Trend (MT) | `close_50_sma` | **214.35** | Bullish | Price +4.9% above; rose from 205.42 (8/4) monotonically |
| Trend (ST) | `close_10_ema` | **219.71** | Bullish | Price +2.3% above; EMA turning up from 9/16 trough (217.39) |
| Momentum | `macd` | **1.29** | Recovering | Up from 0.46 (9/16); was −1.94 on 7/31 |
| Momentum | `macds` | **1.51** | Caution | MACD still below signal; histogram −0.22 |
| Momentum | MACD histogram (derived) | **−0.22** | Improving | Narrowed from −1.57 (9/16) → −0.22 (9/21); crossover pending |
| Momentum | `rsi` | **56.50** | Neutral-bullish | Recovered from 44.07 (9/14); ~13 pts below overbought |
| Volatility | `atr` | **6.23** | Compressing | Down from 7.65 (8/28); ~2.8% of price |
| Volatility | Bollinger mid / upper / lower | **219.24 / 232.28 / 206.19** | Neutral | Price in upper third; bandwidth ~11.9% |
| Volume | `vwma` | **221.12** | Bullish | Price +1.7% above; VWMA rising since 8/24 |
| Resistance | 9/4 close | **230.10** | Pending test | Second of two failed breakouts |
| Resistance | Upper Bollinger | **232.28** | Pending test | 3.3% above current close |
| Resistance | 5/14 close / intraday high | **235.20 / 236.00** | Structural ceiling | Top of the multi-month range |
| Support | 9/14 swing close | **210.96** | Key | Higher low vs. 8/24's 208.25 |
| Support | 50 SMA / 2×ATR | **214.35 / 212.41** | Key | Trend invalidation zone |
| Support | 200 SMA | **198.24** | Long-term line | Bull-market demarcation |

**Bottom line:** NVDA is in a confirmed uptrend across all three moving-average horizons, with a rising VWMA, a recovering RSI at 56.50, and a MACD histogram that has compressed from −1.57 to −0.22 in four sessions — a bullish crossover is plausibly one to two sessions away. The offsetting risk is a hard, twice-tested supply band at **227.7–230.1**, with volatility compression (ATR down ~19% from its 8/28 peak) suggesting a decisive expansion is near. The highest-probability structure is a breakout attempt on 227.73; failure there would reframe the tape as range-bound between roughly 210.96 and 232–236.