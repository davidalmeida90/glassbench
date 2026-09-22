# Intel Corporation (INTC) — Fundamental Analysis Report
**Analysis date:** 2026-05-15 | **Exchange:** NMS (NASDAQ) | **Sector:** Technology / Semiconductors

---

## 1. Data Scope & Caveats

- **Source:** SEC EDGAR facts (as filed on or before 2026-05-15), covering the income statement, balance sheet, and cash flow statement.
- **Profile/valuation data withheld:** The vendor's `get_fundamentals` snapshot explicitly withholds profile, market cap, valuation multiples, and 52-week range for this point-in-time because those fields are only served as present-day (2026-09-19) values, which would inject look-ahead bias. **No P/E, P/S, EV/EBITDA, or market cap can be cited.** All analysis below is built strictly from the point-in-time financial statements.
- **Quarterly income-statement gap:** The vendor's quarterly income statement omits all **December (Q4/fiscal year-end) quarters** consistently across history (e.g., 2023-12-30, 2024-12-28, 2025-12-27 absent). Q4 revenue must be inferred from the annual figures. The **latest reported quarter is Q1 FY2026, ended 2026-03-28.**
- Intel operates on a 52/53-week fiscal year ending the last Saturday of December.

---

## 2. Business Context

Intel Corporation is a US-based semiconductor designer and manufacturer (IDM), spanning Client Computing (PC CPUs), Data Center & AI, Network & Edge, and the fledgling **Intel Foundry** contract-manufacturing business. The core fundamental story captured in this data is a **multi-year turnaround**: the company absorbed enormous losses, impairments and restructuring in FY2023–FY2024, showed a sharp loss-narrowing recovery through FY2025, but the **most recent quarter (Q1 FY2026) shows renewed bottom-line pressure** even as revenue and gross margin improved.

---

## 3. Income Statement Analysis

### 3.1 Annual trend (FY2021–FY2025, USD millions)

| Metric | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Revenue | 79,024 | 63,054 | 54,228 | 53,101 | 52,853 |
| Cost of Revenue | 35,209 | 36,188 | 32,517 | 35,756 | 34,478 |
| Gross Profit | 43,815 | 26,866 | 21,711 | 17,345 | 18,375 |
| Gross Margin | 55.4% | 42.6% | 40.0% | 32.7% | 34.8% |
| Operating Income | 19,456 | 2,334 | 93 | (11,678) | (2,214) |
| Net Income | 19,868 | 8,014 | 1,689 | (18,756) | (267) |
| Diluted EPS | 4.86 | 1.94 | 0.40 | (4.38) | (0.06) |

**Key takeaways:**
- **Revenue has stabilized.** After collapsing from $79.0B (FY2021) to $54.2B (FY2023), revenue has flattened at ~$53B for two straight years (−0.5% in FY2025). The steep share-loss phase appears to be bottoming.
- **Gross margin is recovering:** 32.7% (FY2024) → **34.8% (FY2025)**, first YoY improvement since FY2021.
- **Massive loss narrowing:** Net loss fell from **−$18,756M (FY2024) to −$267M (FY2025)** — a ~$18.5B improvement — largely on the absence of FY2024's huge impairments/restructuring and a swing in operating income from −$11.7B to −$2.2B.
- **Still not profitable:** FY2025 EPS of −$0.06 means the company remains barely below break-even on the bottom line.

### 3.2 Recent quarterly trend (USD millions)

| Metric | Q1 FY24 (03/30/24) | Q3 FY24 (09/28/24) | Q1 FY25 (03/29/25) | Q2 FY25 (06/28/25) | Q3 FY25 (09/27/25) | **Q1 FY26 (03/28/26)** |
|---|---|---|---|---|---|---|
| Revenue | 12,724 | 13,284 | 12,667 | 12,859 | 13,653 | **13,577** |
| Gross Profit | 5,217 | 1,997 | 4,672 | 3,542 | 5,218 | **5,347** |
| Gross Margin | 41.0% | 15.0% | 36.9% | 27.5% | 38.2% | **39.4%** |
| Operating Income | (1,069) | (9,057) | (301) | (3,176) | 683 | **(3,136)** |
| Net Income | (381) | (16,639) | (821) | (2,918) | 4,063 | **(3,728)** |
| Diluted EPS | (0.09) | (3.88) | (0.19) | (0.67) | 0.90 | **(0.73)** |

**Key takeaways:**
- **Q1 FY2026 revenue of $13,577M is up ~7.2% YoY** vs Q1 FY2025 ($12,667M) — the strongest YoY growth read in the visible window.
- **Gross margin of 39.4% is the highest of the visible quarters**, continuing the structural margin recovery.
- **But operating and net losses re-widened sharply:** Operating income of −$3,136M and net loss of −$3,728M (EPS −$0.73). Implied operating expenses (gross profit − operating income) ≈ $8.5B, pointing to elevated R&D plus restructuring/impairment charges tied to the foundry build-out.
- **Q3 FY2025 net income of $4,063M was an outlier**, inflated by large non-operating/investment gains (operating income was only $683M). Traders should treat that quarter's bottom line as non-recurring.
- Gross margin is volatile quarter to quarter (27.5% in Q2 FY25 to 38.2% in Q3 FY25), reflecting foundry start-up costs and product mix.

---

## 4. Balance Sheet Analysis (USD millions)

| Metric | 12/28/24 | 03/29/25 | 06/28/25 | 09/27/25 | 12/27/25 | **03/28/26** |
|---|---|---|---|---|---|---|
| Total Assets | 196,485 | 192,242 | 192,520 | 204,514 | 211,429 | **205,332** |
| Current Assets | 43,269 | 42,134 | 43,375 | 51,731 | 63,688 | **62,157** |
| Cash & Equivalents | ~7,870 | ~8,249 | 9,643 | 11,141 | 14,265 | **17,247** |
| Current Liabilities | 35,159 | 32,174 | 34,966 | 32,297 | 31,575 | **26,885** |
| Stockholders' Equity | 99,270 | 99,756 | 97,883 | 106,376 | 114,281 | **111,394** |

**Key takeaways:**
- **Liquidity has strengthened materially.** Cash & equivalents nearly **doubled from ~$8.2B (Q1 FY25) to $17.2B (Q1 FY26)**.
- **Equity expanded from ~$97.9B (Q2 FY25) to ~$111.4B**, consistent with the 2025 capital injections (strategic/sovereign equity investments widely associated with the US government, NVIDIA, and SoftBank), which also lifted total assets above $200B.
- **Current ratio ≈ 2.3x** ($62.2B current assets / $26.9B current liabilities) — a comfortable liquidity cushion.
- **Implied leverage:** Total assets ($205.3B) − equity ($111.4B) ≈ **$94B of total liabilities** (exact total-liability figure is not tagged by this filer). The balance sheet remains highly leveraged relative to peers, a standing risk given persistent negative free cash flow.
- Total assets dipped slightly QoQ (211,429 → 205,332) and equity fell modestly (114,281 → 111,394) in Q1 FY2026 — consistent with the quarter's net loss.

---

## 5. Cash Flow Analysis (USD millions)

### 5.1 Annual

| Metric | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Operating Cash Flow | 29,456 | 15,433 | 11,471 | 8,288 | 9,697 |
| Capital Expenditure | 18,733 | 24,844 | 25,750 | 23,944 | 14,646 |
| **Free Cash Flow** | **10,723** | **(9,411)** | **(14,279)** | **(15,656)** | **(4,949)** |
| Investing CF | (24,283) | (10,231) | (24,041) | (18,256) | (14,821) |
| Financing CF | (6,211) | 1,115 | 8,505 | 11,138 | 11,587 |

### 5.2 Quarterly (Q1 of each year)

| Metric | Q1 FY24 | Q1 FY25 | **Q1 FY26** |
|---|---|---|---|
| Operating Cash Flow | (1,223) | 813 | **1,096** |
| Capital Expenditure | 5,970 | 5,183 | **3,636** |
| Investing CF | (2,563) | 81 | **3,093** |
| Financing CF | 3,630 | (196) | **(1,206)** |

**Key takeaways:**
- **OCF is recovering:** FY2025 OCF of $9,697M up from $8,288M in FY2024; Q1 FY2026 OCF of $1,096M up YoY from $813M.
- **Capex discipline is the headline story:** Capex fell from a peak of **$25,750M (FY2023) → $23,944M (FY2024) → $14,646M (FY2025)**, a ~43% cut. Q1 FY2026 capex of $3,636M is well below Q1 FY2025's $5,183M.
- **FCF remains negative but sharply improving:** −$15,656M (FY2024) → **−$4,949M (FY2025)**, the best FCF read since FY2021. Q1 FY2026 FCF ≈ −$2,540M vs ≈ −$4,370M in Q1 FY2025.
- **Heavy reliance on external financing:** FY2024 and FY2025 financing inflows of $11.1B and $11.6B (capital raises, and in earlier years debt), while investing outflows remained large. This confirms the turnaround is being funded externally, not yet self-funding.
- **Positive investing CF in Q1 FY2026 (+$3,093M)** alongside capex of $3,636M implies sizable asset/investment sales or proceeds during the quarter — a point to watch for recurrence.

---

## 6. Key Ratios & Trend Summary

| Metric | FY2023 | FY2024 | FY2025 | Q1 FY2026 |
|---|---|---|---|---|
| Revenue growth (YoY) | −14.0% | −2.1% | −0.5% | +7.2%¹ |
| Gross margin | 40.0% | 32.7% | 34.8% | 39.4% |
| Operating margin | 0.2% | −22.0% | −4.2% | −23.1% |
| Net margin | 3.1% | −35.3% | −0.5% | −27.5% |
| Diluted EPS | 0.40 | (4.38) | (0.06) | (0.73) |
| Current ratio | — | ~1.2x | ~2.0x | ~2.3x |
| FCF (annual) | (14,279) | (15,656) | (4,949) | (2,540)² |

¹Q1 FY2026 vs Q1 FY2025. ²Q1 FY2026 quarterly FCF (OCF − Capex).

---

## 7. Actionable Insights for Traders

1. **Turnaround is real but incomplete and bumpy.** FY2025 delivered dramatic improvement (net loss −$267M vs −$18,756M), but **Q1 FY2026 reverted to a −$3,728M net loss / −$0.73 EPS.** Do not extrapolate the Q3 FY2025 profit ($0.90 EPS) — it was driven by non-operating gains. Expect headline loss volatility to persist.

2. **Watch the gross-margin trajectory as the primary signal.** Gross margin improved to **39.4% in Q1 FY2026** — the best visible quarter — even as the bottom line worsened. If margin expansion holds while cost discipline persists, it supports a bullish recovery thesis; a reversal below ~35% would be a red flag.

3. **Capex is the swing factor for FCF.** The reduction from $25.8B (FY2023) to $14.6B (FY2025) and Q1 FY2026's lean $3.6B are the biggest driver of FCF improvement. **Any guidance implying re-acceleration of foundry capex threatens the FCF recovery** and likely pressures shares.

4. **Balance-sheet strength is a buffer.** Cash of **$17.2B**, equity of **$111.4B**, and a ~2.3x current ratio reduce near-term solvency risk despite ~$94B in total liabilities and negative FCF. This buys the company time but equity holders remain behind a large liability stack.

5. **External financing dependence is a risk.** Two consecutive years of >$11B financing inflows mean the story relies on continued capital access. Positive investing CF (+$3,093M) in Q1 FY2026 warrants scrutiny — if driven by asset sales rather than operations, quality of the liquidity improvement is lower.

6. **Revenue stabilization + 7% YoY growth is the bull case.** After two flat years, Q1 FY2026's +7.2% YoY revenue growth is the first genuine top-line inflection in the visible window — a potentially constructive leading indicator if sustained.

7. **No valuation anchor available.** Because profile/multiple data is withheld point-in-time, position sizing must rely on the above fundamental trajectory rather than a P/E or P/S framework; traders should overlay their own current multiple inputs externally.

**Net assessment:** Fundamentally a **high-risk, deep-value turnaround**. Improving revenue trend and margins, sharply reduced cash burn, a fortress liquidity position, and dramatically narrowed losses support a constructive medium-term view — but recurring quarterly losses, ~$94B of liabilities, persistent negative FCF, and dependence on external capital keep downside risk elevated. The next data point to watch is whether Q2 FY2026 sustains ~39% gross margin while further reducing the operating loss.

---

## 8. Key Points Summary Table

| Category | Metric | Value | Trend / Signal |
|---|---|---|---|
| Identity | Ticker / Exchange | INTC / NMS | Technology – Semiconductors |
| Revenue | FY2025 | $52,853M | Flat (−0.5% YoY); stabilizing |
| Revenue | Q1 FY2026 (03/28/26) | $13,577M | +7.2% YoY — first real inflection |
| Profitability | FY2025 Net Income | −$267M | Massive improvement from −$18,756M |
| Profitability | Q1 FY2026 Net Income | −$3,728M | Loss re-widened (EPS −$0.73) |
| Margins | FY2025 Gross Margin | 34.8% | Up from 32.7% FY2024 |
| Margins | Q1 FY2026 Gross Margin | 39.4% | Best visible quarter |
| Margins | FY2025 Operating Margin | −4.2% | Up from −22.0% FY2024 |
| Cash Flow | FY2025 Operating CF | $9,697M | Recovering |
| Cash Flow | FY2025 Capex | $14,646M | −43% from FY2023 peak |
| Cash Flow | FY2025 Free Cash Flow | −$4,949M | Best since FY2021; still negative |
| Balance Sheet | Total Assets (Q1 FY26) | $205,332M | >$200B |
| Balance Sheet | Cash (Q1 FY26) | $17,247M | Doubled from ~$8.2B a year earlier |
| Balance Sheet | Stockholders' Equity (Q1 FY26) | $111,394M | Rising on capital injections |
| Liquidity | Current Ratio (Q1 FY26) | ~2.3x | Comfortable cushion |
| Leverage | Implied Total Liabilities | ~$94B | High — key risk |
| Financing | FY2025 Financing CF | +$11,587M | Heavy external capital reliance |
| Overall | Assessment | High-risk turnaround | Improving fundamentals; loss volatility + leverage risk |

*Note: Profile, market-cap, and valuation multiples were unavailable for the 2026-05-15 point-in-time (vendor withholds present-day-only fields to avoid look-ahead bias).*