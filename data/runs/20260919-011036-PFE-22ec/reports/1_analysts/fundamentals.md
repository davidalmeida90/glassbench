# Fundamental Analysis Report — Pfizer Inc. (`PFE`)

**Analysis date:** 2026-02-13 | **Exchange:** NYQ | **Sector:** Healthcare — Drug Manufacturers–General
**Data source:** SEC EDGAR facts filed on or before 2026-02-13 (point-in-time). Latest reported period available: **Q3 FY2025 (quarter ended 2025-09-28)**.

---

## 1. Important Data-Availability Caveat

The comprehensive `get_fundamentals` profile endpoint **withheld all present-day profile and market data** for this date (market cap, P/E, P/B, EV/EBITDA, 52-week range, TTM quote-linked metrics). The vendor only serves a *present-day (2026-09-19)* snapshot, and serving it into a 2026-02-13 analysis would inject look-ahead/quote bias. **Therefore all valuation multiples below are either unavailable or derived from the statements themselves.** Everything that follows is built from the point-in-time balance sheet, income statement, and cash flow data filed on or before 2026-02-13. There is no week-specific news/event feed in these tools, so "the past week" for fundamentals reduces to the most recent filings already on record (latest = Q3 2025, filed Nov 2025).

---

## 2. Company Profile & Business Context

- **Identity confirmed by tool output:** Pfizer Inc., Healthcare / Drug Manufacturers – General, listed on NYQ (`PFE`). No tool result contradicted the resolved identity.
- **Business model:** Large-cap, diversified global pharmaceutical manufacturer — innovative biopharma (oncology, vaccines, internal medicine, immunology, rare disease) plus a legacy consumer/off-patent footprint. Reporting has been reshaped in recent years by the **COVID-19 franchise (Comirnaty vaccine + Paxlovid antiviral)** and by the **~$43B Seagen acquisition (closed Dec 2023)**, which added oncology.
- **Diluted share count (derived):** ~5,700M shares (Net income ÷ Diluted EPS across Q1–Q3 2025 is consistently ~5,706–5,711M).

---

## 3. Revenue & Earnings — Annual Trend (FY)

| FY (Dec 31) | Revenue ($M) | YoY | Net Income ($M) | Diluted EPS | Net Margin |
|---|---:|---:|---:|---:|---:|
| 2021 | 73,636 | +76.8% | 21,979 | 3.85 | 29.8% |
| 2022 | 91,793 | +24.7% | 31,372 | 5.47 | 34.2% |
| 2023 | 50,914 | **-44.5%** | 2,119 | 0.37 | 4.2% |
| 2024 | 63,627 | **+25.0%** | 8,031 | 1.41 | 12.6% |

**Read-through:** PFE is a textbook COVID-boom-bust-recovery story. FY2022 ($91.8B revenue, $31.4B NI) was the COVID peak. FY2023 was the air-pocket: revenue fell 44.5% and net income collapsed 93% to $2.1B as COVID revenue evaporated *and* large charges/inventory write-downs landed. **FY2024 marks the recovery** — revenue +25% to $63.6B and net income ~3.8× to $8.0B, aided by Seagen/oncology plus a stabilizing non-COVID base. FY2024 is still well below the 2021–2022 peak in absolute dollars.

---

## 4. Recent Quarterly Trend & Trailing-Twelve-Month (TTM)

Quarterly income statement (most recent five reported quarters; Q4’24 **not separately tagged** — derived from FY2024 minus 9M):

| Period | Revenue ($M) | Net Income ($M) | Diluted EPS |
|---|---:|---:|---:|
| Q4 2024 (derived) | ~17,763 | ~410 | ~0.07 |
| Q1 2025 (2025-03-30) | 13,715 | 2,967 | 0.52 |
| Q2 2025 (2025-06-29) | 14,653 | 2,910 | 0.51 |
| Q3 2025 (2025-09-28) | **16,654** | **3,541** | **0.62** |
| **TTM (Q4’24+Q1–Q3’25)** | **~62,785** | **~9,828** | **~1.72** |

**Read-through:** The last three quarters show a **clear improving, sequential earnings ramp** — EPS $0.52 → $0.51 → $0.62, with Q3 the strongest of 2025 (revenue $16.65B, net income $3.54B). TTM EPS of ~$1.72 is running ahead of FY2024's $1.41, consistent with continued earnings normalization. Note Q4 is seasonally soft (Q4'24 EPS only ~$0.07 on charges), so TTM comparisons flatter the trailing run-rate.

---

## 5. Margin Analysis

| Metric | FY2023 | FY2024 | TTM | Q3 2025 |
|---|---:|---:|---:|---:|
| Gross margin | 51.0% | 71.9% | 73.4% | 74.9% |
| Net margin | 4.2% | 12.6% | 15.7% | 21.3% (3,541/16,654) |

**Read-through:** The **gross-margin jump from 51% → 72%+** is the single most important fundamental development. It reflects (a) the runoff of low-/negative-margin COVID inventory write-downs and profit-share mechanics that crushed FY2023, and (b) a more favorable mix post-Seagen. Net margin has recovered in tandem. This operating-leverage inflection is the core of the bull case in the data.

---

## 6. Balance Sheet, Liquidity & Leverage (as of 2025-09-28)

| Item | Value ($M) | Comment |
|---|---:|---|
| Total assets | 208,731 | Down from ~$226.5B (Q4’23 peak balance sheet) |
| Total liabilities | 115,635 | ~55.4% of assets |
| Stockholders' equity | 92,801 | Recovered from $88,203 (Q4’24) |
| Current assets | 46,924 | |
| Current liabilities | 36,596 | |
| Cash & equivalents | **1,343** | Very low on the *narrow* line — see note |
| Working capital | 10,328 | |
| Current ratio | ~1.28 | Adequate, not strong |

**Read-through / caveats:**
- **Leverage is elevated:** total liabilities of $115.6B against equity of $92.8B = **debt-to-equity proxy of ~1.25×**, a legacy of the Seagen financing. The vendor did **not** tag discrete short-term/long-term debt lines, so true net-debt cannot be isolated from these tools.
- **Cash of only ~$1.34B** on the reported "Cash & Equivalents" line looks alarmingly thin for a company this size, **but this is a tagging artifact** — PFE holds substantial balances in short-term investments (not captured by this vendor's single cash line). Traders should not read $1.3B as total liquidity. The consistency of these low figures across 2022–2025 (mostly $1–3B) confirms it is a reporting-definition issue, not a liquidity crisis.
- **Equity peaked ~$101.0B (Q1 2023)** and has since drifted to ~$92.8B via buybacks, dividends, impairments, and FX — a slow erosion worth monitoring alongside leverage.

---

## 7. Cash Flow Analysis

**Annual ($M):**

| FY | Operating CF | CapEx | Free Cash Flow | Investing CF | Financing CF |
|---|---:|---:|---:|---:|---:|
| 2021 | 32,580 | 2,711 | 29,869 | -22,546 | -9,816 |
| 2022 | 29,267 | 3,236 | 26,031 | -15,783 | -14,834 |
| 2023 | 8,700 | 3,907 | 4,793 | **-32,278** | **+26,066** |
| 2024 | 12,744 | 2,909 | **9,835** | +2,652 | -17,140 |

**Quarterly (Q1 files only):** Q1 2025 (2025-03-30): Operating CF 2,335; CapEx 564; **FCF ~1,771**.

**Read-through:** FCF is the recovery story in numbers — from **$4.8B (2023) to $9.8B (2024)**, roughly doubling. FY2023's investing outflow of $32.3B (Seagen) was funded by a **+$26.1B financing inflow** (debt), and FY2024's **-$17.1B financing outflow** shows the deleveraging/dividend/buyback paydown already underway. Q1'25 FCF of ~$1.77B is a solid start but front-loaded by Q1 seasonality caveats. Capital intensity is modest (CapEx ~4.6% of revenue in FY2024) — typical pharma asset-light profile.

---

## 8. Actionable Insights for Traders

1. **The turnaround is real and measurable, but priced off a depressed base.** Revenue +25% and net income ~3.8× in FY2024, plus three consecutive quarters of accelerating EPS ($0.52→$0.62), argue the worst of the COVID unwind is behind PFE. The **gross-margin expansion (51%→75%)** is the cleanest signal.
2. **TTM earnings power (~$1.72 EPS) is already above FY2024's $1.41.** If Q4'25 follows the improving trend, full-year 2025 EPS could exceed the prior year comfortably — a potential positive catalyst when Q4 is reported.
3. **Balance sheet remains the key overhang.** Elevated leverage (~1.25× liabilities/equity) and thin narrow-line cash mean FCF allocation (debt paydown vs. dividends vs. buybacks) will drive sentiment. Watch financing-cash outflows as the deleveraging gauge.
4. **Watch the composition, not just the total, of revenue.** The durability of the recovery depends on non-COVID growth (oncology/Seagen, vaccines, internal medicine) offsetting the ongoing COVID-franchise decay. The statements alone don't break out product-level mix — a limitation to flag.
5. **Valuation cannot be assessed from these tools** (no market cap/multiples available point-in-time). Any P/E or FCF-yield judgment must be sourced separately; do not infer it from this report.
6. **Do not over-interpret the $1.3B cash line** — it excludes short-term investments; treat it as a reporting artifact rather than a liquidity red flag.

---

## 9. Key Risks

- **COVID-franchise decay** continues to drag on reported top-line (Comirnaty/Paxlovid).
- **Patent cliff / LOE exposure** on legacy blockbusters is not quantified in the statement data but remains the industry-standard risk.
- **Elevated leverage** from the Seagen deal limits financial flexibility if FCF disappoints.
- **Charge/populated-quarter volatility** — PFE has repeatedly taken large write-downs (FY2023, Q4'24), so single-quarter earnings can swing sharply (e.g., Q4'24 EPS ~$0.07).
- **Data coverage gaps** (no Q4 in quarterly series; no discrete debt or product-mix lines; no market data) constrain precision.

---

## 10. Summary Table — PFE Fundamentals (point-in-time 2026-02-13)

| Category | Metric | Value / Result | Insight |
|---|---|---|---|
| **Identity** | Company / Ticker / Exchange | Pfizer Inc. / PFE / NYQ | Healthcare – Drug Manufacturers (General) |
| **Latest period** | Reported quarter | Q3 FY2025 (2025-09-28) | Latest filed on/before 2026-02-13 |
| **Revenue (FY)** | 2022 / 2023 / 2024 | $91.8B / $50.9B / $63.6B | COVID peak → bust (-44.5%) → recovery (+25%) |
| **Revenue (TTM)** | Q4’24+Q1–Q3’25 | ~$62.8B | Below COVID peak; stable base |
| **Q3’25 quarter** | Revenue / Net Income / EPS | $16.65B / $3.54B / $0.62 | Strongest quarter of 2025 |
| **Earnings (FY)** | NI 2023 / 2024 | $2.12B / $8.03B | ~3.8× recovery |
| **Earnings (TTM)** | Net Income / EPS | ~$9.83B / ~$1.72 | Above FY2024 EPS of $1.41 |
| **EPS (FY)** | 2022 / 2023 / 2024 | $5.47 / $0.37 / $1.41 | Extreme COVID-cycle volatility |
| **Gross margin** | FY23 → FY24 → TTM | 51.0% → 71.9% → 73.4% | Major margin inflection = core bull signal |
| **Net margin** | FY23 → FY24 → TTM | 4.2% → 12.6% → 15.7% | Operating leverage returning |
| **Balance sheet** | Assets / Liabilities / Equity | $208.7B / $115.6B / $92.8B | Leverage proxy ~1.25× |
| **Liquidity** | Curr. assets / curr. liab. | $46.9B / $36.6B (ratio 1.28) | Adequate; working capital $10.3B |
| **Cash (narrow line)** | Q3’25 | $1.34B | Tagging artifact — excludes ST investments |
| **Cash flow (FY24)** | OCF / CapEx / FCF | $12.7B / $2.9B / $9.8B | FCF roughly doubled vs 2023 ($4.8B) |
| **Cash flow (Q1’25)** | OCF / CapEx / FCF | $2.34B / $0.56B / ~$1.77B | Solid start to 2025 |
| **Capital allocation** | FY23 financing / FY24 financing | +$26.1B / -$17.1B | Debt-funded Seagen → deleveraging |
| **Shares (derived)** | Diluted | ~5,700M | From NI ÷ EPS |
| **Valuation** | P/E, P/B, market cap, 52-wk range | **NOT AVAILABLE** | Profile endpoint withheld to avoid look-ahead |
| **Key catalyst** | Q4/FY2025 results | Pending | May confirm EPS > $1.41 |

**Bottom line for traders:** The point-in-time fundamentals show a company past the trough of its COVID unwind, with **recovering revenue, doubling free cash flow, and a dramatic gross-margin inflection (51%→~74%)**, but still carrying **elevated balance-sheet leverage and a slow equity erosion**. The next hard datapoint is Q4/FY2025 earnings, which this data set does not yet contain. Valuation is not assessable from the provided tools and must be sourced independently.