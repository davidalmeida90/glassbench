# Intel Corporation (INTC) — Fundamental Research Report
**Analysis date: 2025-11-14 | Ticker: INTC | Exchange: NMS | Sector: Technology / Semiconductors**

---

## 1. Scope, Data Sources & Limitations (read first)

This report is built **only** from point-in-time SEC EDGAR facts filed on or before **2025-11-14**, retrieved via the balance sheet, income statement and cash flow tools.

- **`get_fundamentals` returned no profile data for this vintage** — the vendor explicitly withholds market cap, valuation multiples, the 52-week range, TTM income and even current name/sector/industry because it only serves *present-day* (2026-09-19) values, which would inject look-ahead bias into a 2025-11-14 analysis. **Consequently no P/E, P/S, P/B, EV/EBITDA or market cap can be computed or quoted here.** Only statement-level (point-in-time) data is usable.
- **"Total Liabilities" is not tagged by this filer** — total liabilities are therefore derived as `Total Assets − Stockholders' Equity`.
- The **quarterly income statement skips Q4 2024** (gap between 2024-09-28 and 2025-03-29). Q4 2024 figures in this report are **derived** (FY2024 minus 9M2024) and flagged as estimates.
- The **quarterly cash flow series is sparse** (essentially one observation per year, dated end-March). Annual cash flow data (FY2007–FY2024) is complete and is used as the primary cash-flow evidence.

---

## 2. Latest Reported Results (Q3 2025, period ended 2025-09-27)

The most recent filing available before the analysis date is **Q3 FY2025**.

| Metric (USD millions) | Q3 2025 (09/27/25) | Q2 2025 (06/28/25) | Q1 2025 (03/29/25) | Q3 2024 (09/28/24) | QoQ | YoY |
|---|---|---|---|---|---|---|
| Revenue | **13,653** | 12,859 | 12,667 | 13,284 | +6.2% | **+2.8%** |
| Cost of Revenue | 8,435 | 9,317 | 7,995 | 11,287 | -9.5% | -25.3% |
| Gross Profit | **5,218** | 3,542 | 4,672 | 1,997 | +47.3% | +161.3% |
| Gross Margin | **38.2%** | 27.5% | 36.9% | 15.0% | +10.7 pts | +23.2 pts |
| Operating Income | **683** | (3,176) | (301) | (9,057) | +3,859 | +9,740 |
| Operating Margin | **5.0%** | -24.7% | -2.4% | -68.2% | +29.7 pts | +73.2 pts |
| **Net Income** | **4,063** | (2,918) | (821) | (16,639) | +6,981 | +20,702 |
| Diluted EPS | **$0.90** | $(0.67) | $(0.19) | $(3.88) | — | — |

**Interpretation:** Intel has crossed back above the operating break-even line for the first time in two years (operating income of $683M), and gross margin at 38.2% is the strongest since the 2022 deterioration began. **However, the headline GAAP profit of $4,063M is NOT operationally driven** — operating income was only $683M, meaning roughly **~$3.4B (or more, pre-tax) came from below-the-line items** (interest/other income, gains on equity investments, and/or one-time items). See §7 — this is the single most important earnings-quality flag in the report.

**Derived Q4 2024** (FY2024 minus 9M2024, estimate): Revenue ~**14,260**, Gross Profit ~5,584 (GM ~39.2%), Operating Income ~+412, Net Income ~(126), EPS ~$(0.03). This shows Q4 2024 was the operating trough before the 2025 recovery — the December quarter was actually the strongest revenue quarter of the FY2024 cycle.

---

## 3. Annual Financial History (FY2018 – FY2024)

| Fiscal Year (ended late Dec) | Revenue | Gross Profit | GM% | Operating Income | OpM% | Net Income | Diluted EPS | Operating CF | CapEx | Free Cash Flow |
|---|---|---|---|---|---|---|---|---|---|---|
| FY2024 | 53,101 | 17,345 | 32.7% | (11,678) | -22.0% | **(18,756)** | **$(4.38)** | 8,288 | 23,944 | **(15,656)** |
| FY2023 | 54,228 | 21,711 | 40.0% | 93 | 0.2% | 1,689 | $0.40 | 11,471 | 25,750 | (14,279) |
| FY2022 | 63,054 | 26,866 | 42.6% | 2,334 | 3.7% | 8,014 | $1.94 | 15,433 | 24,844 | (9,411) |
| FY2021 | 79,024 | 43,815 | 55.4% | 19,456 | 24.6% | 19,868 | $4.86 | 29,456 | 18,733 | **+10,723** |
| FY2020 | 77,867 | 43,612 | 56.0% | 23,678 | 30.4% | 20,899 | $4.94 | 35,864 | 14,259 | +21,605 |
| FY2019 | 71,965 | 42,140 | 58.6% | 22,035 | 30.6% | 21,048 | $4.71 | 33,145 | 16,213 | +16,932 |
| FY2018 | 70,848 | 43,737 | 61.7% | 23,316 | 32.9% | 21,053 | $4.48 | 29,432 | 15,181 | +14,251 |

*(All figures USD millions. FCF = Operating Cash Flow − CapEx.)*

**The multi-year arc is stark:**
- **Revenue shrank ~33%** from the FY2021 peak of $79.0B to FY2024's $53.1B (share loss to AMD, data-center/PC cyclicality, and exits from non-core lines).
- **Gross margin collapsed ~23 points**, from 55–62% (2018–2021) to 32.7% (2024) — a mix of pricing pressure and, critically, the **unabsorbed depreciation of a fab buildout running at low utilization**.
- **Profitability flipped from ~$20B net income (FY2019–2021) to an $(18.8)B net loss in FY2024** — driven by the huge Q3 2024 impairment (CQ3-24 net loss of $(16.6)B; operating loss $(9.1)B).
- **Free cash flow flipped from strongly positive (+$21.6B in FY2020) to deeply negative** — a cumulative **$(39.3)B of FCF burn across FY2022–FY2024**.

---

## 4. Balance Sheet & Capital Structure

| USD millions | 2025-09-27 (Q3'25) | 2025-06-28 (Q2'25) | 2025-03-29 (Q1'25) | 2024-12-28 (Q4'24) | 2024-09-28 (Q3'24) | 2023-12-30 (Q4'23) |
|---|---|---|---|---|---|---|
| Total Assets | **204,514** | 192,520 | 192,242 | 196,485 | 193,542 | 191,572 |
| Current Assets | **51,731** | 43,375 | 42,134 | 47,324 | 46,137 | 43,269 |
| Cash & Equivalents | **11,141** | 9,643 | n/a | 8,249 | n/a | n/a |
| Current Liabilities | **32,297** | 34,966 | 32,174 | 35,666 | 35,159 | 28,053 |
| Stockholders' Equity | **106,376** | 97,883 | 99,756 | 99,270 | 99,532 | 105,590 |
| Total Liabilities (derived)* | 98,138 | 94,637 | 92,486 | 97,215 | 94,010 | 85,982 |
| **Current Ratio** | **1.60** | 1.24 | 1.31 | 1.33 | 1.31 | 1.54 |
| **Liabilities / Equity** | **0.92** | 0.97 | 0.93 | 0.98 | 0.94 | 0.81 |

*\*Derived as Total Assets − Stockholders' Equity because "Total Liabilities" is untagged.*

**Key observations:**
- **Q3 2025 is a step-change in the balance sheet.** Total assets jumped **+$12.0B QoQ** (to $204.5B) and stockholders' equity jumped **+$8.5B QoQ** (to $106.4B) — the largest single-quarter equity increase in the dataset. This is the footprint of the **2025 strategic equity infusions** (US government ~10% stake, SoftBank $2B, NVIDIA $5B) — see §6. The cash line rose to $11.1B and current ratio improved sharply to **1.60**.
- **Liquidity has been substantially de-risked.** The current ratio bottomed near 1.24 in Q2 2025 and leverage (Liabilities/Equity) improved toward 0.9x, reversing the deterioration caused by the FY2022–FY2024 cash burn.
- **Book value ≈ $106.4B.** Against the post-issuance share count (roughly 4.5–5.2B shares after the government/SoftBank/NVIDIA issuances), implied **book value per share is approximately $20–24** — a useful anchor given that market multiples are unavailable for this vintage.
- **Note the share-count dilution risk:** the government took ~433.3M shares (~$8.9B at $20.47), NVIDIA ~$5B and SoftBank ~$2B, materially raising the share base and diluting per-share economics versus the ~4.29B diluted shares outstanding at FY2024.

---

## 5. Cash Flow, Capital Intensity & The Core Risk

| Fiscal Year | Operating CF | Investing CF | Financing CF | CapEx | FCF | CapEx / Revenue |
|---|---|---|---|---|---|---|
| FY2024 | 8,288 | (18,256) | +11,138 | 23,944 | **(15,656)** | **45.1%** |
| FY2023 | 11,471 | (24,041) | +8,505 | 25,750 | (14,279) | 47.5% |
| FY2022 | 15,433 | (10,231) | +1,115 | 24,844 | (9,411) | 39.4% |
| FY2021 | 29,456 | (24,283) | (6,211) | 18,733 | +10,723 | 23.7% |
| FY2020 | 35,864 | (21,524) | (12,669) | 14,259 | +21,605 | 18.3% |

**Latest quarterly cash-flow observation (Q1 2025, period ended 2025-03-29):** Operating CF **$813M**, CapEx **$5,183M**, Investing CF +$81M, Financing CF $(196)M → implied **FCF ≈ $(4.37)B in a single quarter**.

**This is the central fundamental tension for INTC:** the company is spending **~40–48% of revenue on capital expenditure** to build leading-edge fab capacity (18A/14A, Arizona/Ohio) while generating only modest operating cash flow. Financing CF was **+$11.1B in FY2024** — i.e., the buildout has been funded by **external capital, not internal cash generation** — which is precisely why the 2025 equity infusions were strategically necessary and why the balance sheet improved so dramatically in Q3 2025. Until operating cash flow covers CapEx, INTC remains dependent on capital-markets access and/or further asset sales.

---

## 6. Corporate & Strategic Developments Reflected in the Numbers

The Q3 2025 balance-sheet jump and the earnings pattern are consistent with a company undergoing a **strategic reset**:
1. **~$15–16B of strategic equity capital raised in 2025** — US government ~10% stake (announced Aug 2025, largely via conversion of un-paid CHIPS/Secure-Enclave awards into equity), SoftBank $2B (Aug 2025), NVIDIA $5B (Sept 2025, alongside an x86/AI partnership). These explain the Q3 2025 equity/asset surge and materially strengthen solvency.
2. **New CEO (Lip-Bu Tan, from March 2025)** executing a cost and portfolio reset — the Q2 2025 operating loss of $(3.2)B and gross-margin dip to 27.5% reflect restructuring/impairment charges, while Q1 2025's near-breakeven operating result shows the underlying trend.
3. **Portfolio rationalization** — divestitures (e.g., the sale of a majority stake in Altera to Silver Lake, IMS Nanofabrication) and the wind-down/cancellation of European fab projects, aimed at cutting the CapEx trajectory that produced the FY2022–2024 FCF burn.
4. **Foundry/18A transition** — the entire investment thesis hinges on external foundry customers adopting 18A and the process ramping with acceptable yields; gross margin is the scorecard (still 38% vs 55%+ historically).

---

## 7. Earnings Quality & Red Flags

1. **Non-operating earnings dominate the Q3 2025 profit.** Net income of $4,063M vs operating income of only $683M → **~$3.4B+ of pre-tax profit came from non-operating sources** (interest/other, gains on investments, potentially tax items). A trader should **not extrapolate the $0.90 EPS as a run-rate earnings power**; the operations contributed ~$0.15–0.20 of EPS at most.
2. **GAAP profitability is not yet self-sustaining.** 9M2025 operating income is **$(2,794)M** (still negative) even though 9M2025 net income is **+$324M**. The gap is entirely non-operating.
3. **YoY revenue growth is barely positive.** 9M2025 revenue of $39,179M vs 9M2024 of $38,841M = **+0.9%** — stabilization, not recovery.
4. **Persistent cash burn** (FY2024 FCF $(15.7)B; Q1 2025 FCF ≈ $(4.4)B) with CapEx >40% of revenue remains the largest balance-sheet risk, mitigated only by the 2025 equity raises.
5. **Dilution.** The strategic investments materially increased share count — per-share metrics will be diluted versus historical levels.
6. **Data caveat:** the quarterly income statement omits Q4 2024; Q4 figures here are derived and should be treated as estimates.

---

## 8. Actionable Insights for Traders

- **The balance sheet story has decisively improved, and that is a genuine, quantifiable de-risking:** cash to $11.1B, current ratio 1.60, equity +$8.5B QoQ, Liabilities/Equity down to ~0.9x. Any thesis premised on imminent liquidity stress should be discounted.
- **But the operating story is only at "less bad," not "good."** Gross margin 38% and operating margin 5% in Q3 2025 remain far below the 55%+/25%+ levels of the 2019–2021 era. **Watch the trajectory of gross margin and operating income, not headline EPS.**
- **Do not chase the $0.90 Q3 EPS as if it were recurring** — it is non-operationally inflated (~$3.4B of below-the-line gains). A clean operating run-rate is closer to break-even.
- **The pivotal forward variable is CapEx discipline and 18A customer traction.** A credible path to FCF break-even (CapEx converging toward operating cash flow) would be the single most bullish fundamental catalyst. Conversely, another year of $(14–16)B FCF burn would re-open solvency questions despite the new equity.
- **Revenue stabilization (~$13–13.7B/quarter) plus the 2025 capital injections argue against a bearish liquidity-driven outcome**, while the still-negative operating profitability argues against a bullish "turnaround confirmed" outcome. This is a **show-me, watch-the-margin, event-driven** situation (foundry customer wins, 18A ramp, further divestitures, CapEx guidance).
- **Valuation is un-assessable from this vintage** (market data withheld). Any valuation work must be layered on separately by an assistant with price-data access; use the reported book value anchor of ~**$106B equity (~$20–24/share)** as a fundamental floor reference.

### Bottom line
Fundamentally, INTC as of 2025-11-14 is a **stabilizing-but-still-unprofitable turnaround with a dramatically strengthened balance sheet**. The Q3 2025 GAAP profit is an artifact of non-operating gains; the operating business is only marginally above break-even and continues to consume cash on CapEx. **Net fundamental stance: cautiously constructive on solvency/optionality, neutral-to-cautious on earnings quality — a "confirm-the-turn" rather than "buy-the-turn" posture.**

---

## 9. Key Metrics Summary Table

| Category | Metric | Value | Direction / Note |
|---|---|---|---|
| **Latest Quarter (Q3 2025)** | Revenue | $13,653M | +6.2% QoQ, +2.8% YoY |
| | Gross Margin | 38.2% | Best since 2022 deterioration |
| | Operating Income | $683M (5.0%) | First positive op. income in ~2 yrs |
| | Net Income | $4,063M | **Non-operating inflated** |
| | Diluted EPS | $0.90 | Not a clean run-rate |
| **Trailing 9M 2025** | Revenue | $39,179M | +0.9% YoY |
| | Operating Income | $(2,794)M | Still negative |
| | Net Income | +$324M | Positive only via non-op. gains |
| **FY2024 (full year)** | Revenue | $53,101M | -32.8% vs FY2021 peak |
| | Net Income | $(18,756)M | Includes Q3'24 $(16.6)B impairment |
| | Diluted EPS | $(4.38) | — |
| | Free Cash Flow | $(15,656)M | CapEx 45% of revenue |
| **Balance Sheet (Q3 2025)** | Total Assets | $204,514M | +$12.0B QoQ |
| | Stockholders' Equity | $106,376M | +$8.5B QoQ (equity infusions) |
| | Cash & Equivalents | $11,141M | Rising |
| | Current Ratio | 1.60 | Sharp improvement |
| | Liabilities / Equity | ~0.92x | Deleveraging |
| | Book Value / Share (approx.) | ~$20–24 | Post-issuance |
| **Cash Flow Risk** | FY2022–24 cumulative FCF | ~$(39.3)B | Core risk |
| | CapEx / Revenue | 39–48% | Fab buildout |
| **Strategic** | 2025 equity raised | ~$15–16B | US gov, SoftBank, NVIDIA |
| | Leadership | CEO Lip-Bu Tan (Mar 2025) | Portfolio/cost reset |
| **Data Limitations** | Market multiples / market cap | **Unavailable** | Vendor withholds present-day profile |
| | Total Liabilities | **Untagged** | Derived only |
| | Q4 2024 income statement | **Missing** | Derived from FY − 9M |