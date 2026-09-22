# Does serving valuation data change what the agents write? A matched pair

Measured 2026-09-19 on TradingAgents 0.5.0 plus one change (a `sec_edgar.get_fundamentals` vendor that serves market cap, P/E, P/S and P/B as of the run date, proposed upstream as issue #1374). Everything below is in the shipped database: backtests `bt-20260919-003638-8bbd` (control) and `bt-20260919-003638-aab3` (treatment).

## Design

- **Question.** The paper's engine asks the fundamentals analyst for valuation, but on a past date nothing serves it, so the agents write "valuation data not provided" and reason around it. If a point-in-time valuation is served instead, do they use it, and is what they cite correct?
- **Cells.** AAPL, NVDA, INTC and PFE on 2025-11-14, 2026-02-13 and 2026-05-15: 12 cells, one run per cell per arm, 24 runs.
- **Arms.** Control, variant `edgar_statements`: the three financial statements as filed with the SEC, nothing else. Treatment, variant `edgar_valuation`: the same statements plus the valuation multiples as of the run date. Same models (DeepSeek V4 Flash quick, V4 Pro deep), Market and Fundamentals analysts, memory off, one debate round.
- **What is counted.** Not ratings. Statements that valuation is missing, multiples cited with a number, and how many of those match the true figure on the run date (within 5%), read from what every agent wrote (`deskapp/paired.py`).

## Result

| Measure, 12 runs per arm | Statements only | Statements plus valuation |
|---|---:|---:|
| Statements that valuation is missing | 55 | 1 |
| Multiples cited with a number | 35 | 447 |
| of which match the run date's true figure | 25 | 397 |
| Cited by the research or portfolio manager | 5, in 2 runs | 53, in 9 runs |
| LLM cost | $0.548 | $0.523 |
| Tokens | 2,256,268 | 2,165,464 |
| Run time, mean per run | 6.2 min | 5.6 min |

Fewer missing-valuation statements with valuation served in 12 of 12 cells, more in none, equal in none. Exact sign test p = 0.0005. Same cost.

### By agent

| Agent | Missing, control | Missing, treatment | Cited, control | Cited, treatment | Matched, control | Matched, treatment |
|---|---:|---:|---:|---:|---:|---:|
| Fundamentals analyst | 32 | 1 | 2 | 185 | 1 | 172 |
| Bull | 4 | 0 | 4 | 52 | 2 | 46 |
| Bear | 7 | 0 | 14 | 91 | 10 | 75 |
| Research manager | 2 | 0 | 3 | 26 | 3 | 22 |
| Trader | 1 | 0 | 1 | 8 | 1 | 8 |
| Risk, aggressive | 2 | 0 | 3 | 21 | 2 | 21 |
| Risk, conservative | 3 | 0 | 5 | 26 | 4 | 24 |
| Risk, neutral | 1 | 0 | 1 | 11 | 0 | 8 |
| Portfolio manager | 3 | 0 | 2 | 27 | 2 | 21 |

### By cell

| Ticker | Date | True P/E | Rating, control | Rating, treatment | Missing C | Missing T | Cited C | Cited T | Matched C | Matched T |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| AAPL | 2025-11-14 | 35.9x | Underweight | Underweight | 3 | 0 | 2 | 45 | 2 | 45 |
| AAPL | 2026-02-13 | 31.9x | Overweight | Overweight | 8 | 0 | 10 | 35 | 10 | 32 |
| AAPL | 2026-05-15 | 36.0x | Overweight | Overweight | 4 | 0 | 4 | 48 | 3 | 42 |
| INTC | 2025-11-14 | 855.7x | Underweight | Underweight | 2 | 0 | 2 | 27 | 0 | 25 |
| INTC | 2026-02-13 | n/m | Underweight | Underweight | 3 | 0 | 0 | 33 | 0 | 31 |
| INTC | 2026-05-15 | n/m | Underweight | Sell | 3 | 0 | 0 | 48 | 0 | 33 |
| NVDA | 2025-11-14 | 53.4x | Hold | Underweight | 8 | 0 | 1 | 55 | 1 | 55 |
| NVDA | 2026-02-13 | 44.8x | Overweight | Overweight | 5 | 0 | 3 | 33 | 3 | 30 |
| NVDA | 2026-05-15 | 45.6x | Underweight | Underweight | 10 | 0 | 0 | 27 | 0 | 26 |
| PFE | 2025-11-14 | 12.1x | Overweight | Overweight | 1 | 0 | 4 | 25 | 3 | 21 |
| PFE | 2026-02-13 | 11.6x | Overweight | Overweight | 3 | 1 | 5 | 30 | 2 | 28 |
| PFE | 2026-05-15 | 11.9x | Underweight | Underweight | 5 | 0 | 4 | 41 | 4 | 29 |

## What is claimed, and what is not

- Claimed: with valuation served, the agents stop saying it is missing and cite multiples that are correct for the date, at no extra cost. Both managers, who write the plan and the final rating, cite them in 9 of 12 runs instead of 2.
- Not claimed: anything about ratings. Four cells changed rating, but one run per cell cannot separate the data's effect from run-to-run noise (the same engine gives different ratings on identical inputs, see the twin runs in the database).
- Checked and rejected: the idea that the control was quoting memorised multiples. All 36 unmatched citations in the control were read by hand; they were counter noise, homemade forward P/Es and hand arithmetic, not recalled figures.
- Found along the way: the engine keeps one process-wide data configuration and merges into it, so with two runs in flight the control was served the treatment's vendor. That batch was cancelled at $0.055 and the run configuration now lives in a context variable per run (`deskapp/runconfig.py`, test `tests/test_runconfig.py`). Reported upstream as issue #1369.
- Also seen: the market tools serve dividend-adjusted closes, so a "verified close" for a past date drifts as later dividends land (PFE 24.89 served against 25.33 traded on 2026-05-15).

## Reproduce

Run both variants on the same cells from the Backtests page (or `POST /api/backtests` twice with `variant` set to `edgar_statements` and `edgar_valuation`), then:

```powershell
cd backend
python -m deskapp.paired bt-<control> bt-<treatment>
```

The treatment variant needs an engine that serves valuation from EDGAR; the released 0.5.0 serves statements only, so `variants.ensure_available` refuses it on a stock engine until the upstream issue lands.
