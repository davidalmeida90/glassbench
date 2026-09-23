# Backtest method

How Glassbench turns saved agent runs into a fair comparison against holding the stock, and what the first pilot found. The results page is `/backtests/<id>`; the code is `backend/deskapp/backtest.py` (the grid of runs) and `backend/deskapp/simulate.py` (the replay), with tests in `backend/tests/`.

## Question

Over a year of weekly decisions, did the agents' ratings add anything over simply holding the stock, and over chance?

## Grid

- **Dates.** Every Friday close (or the last trading day of the week), taken from SPY's trading calendar, sampled evenly when a stage uses fewer dates. Weekly rather than daily: consecutive daily decisions are highly correlated, so daily runs add cost faster than information.
- **Analysts.** Market and Fundamentals only on past dates. Yahoo keeps only recent news, and StockTwits, Reddit and prediction markets return present-day data, which would leak the future into a past decision.
- **Memory.** Off: each backtest writes to its own empty memory log that is never read or scored, so no lesson from another date reaches a decision and the live memory log stays untouched.
- **Point in time.** Prices stop on the decision date, statements stop at the last period known then, the company profile is withheld.
- **Cost safety.** A hard budget cap per backtest, identical finished runs reused instead of rerun, one retry on failure, pause and cancel. Every finished run stays in the database, tagged with its backtest id.

| Stage | Runs | Gives | Cost on DeepSeek |
|---|---|---|---|
| Pilot | 2 stocks, 4 dates, 8 runs | proves the pipeline, measures real cost and time | about $0.30 |
| Demo | 2 stocks, 52 weeks, 104 runs | full equity curves, every trade linked to its run | about $4 |
| Noise estimate | 2 more reruns per date, 312 runs | confidence bands, rating agreement across reruns | about $10 |

A hit rate measured on 104 decisions has a 95% margin of about ten percentage points: enough to see behaviour and obvious failures, too small to prove skill.

## Replay

Two ways to read a decision, both replayed at zero LLM cost from the saved runs:

- **Rating only.** Buy 100% long, Overweight 50%, Hold keeps the current position, Underweight and Sell flat. Failed or unparseable runs keep the position and are flagged, never counted as a Hold.
- **Trader levels.** The trader's entry, stop and target as orders: an entry below the close is a pullback limit, above it a confirmation stop, a stop exits everything, no same-bar stop.

Fills at the next session's open, a selectable cost in basis points on every change of position, long only, no leverage, positions held until the next weekly decision.

## Baselines

1. Buy-and-hold of the same stock.
2. A 50/200-day moving-average crossover on the same weekly schedule.
3. A shuffled-rating placebo: 1,000 simulations with the same rating mix and number of position changes, shown as the 5th to 95th percentile band.
4. SPY for context.

Metrics: total and annualised return, volatility, Sharpe, maximum drawdown, position changes, cost drag, time in market, hit rate by rating, average next-week return by rating, and the strategy's percentile inside the placebo band. With reruns: rating agreement across reruns and return mean with its standard error.

## Pilot result

Backtest `bt-20260913-230450-9dec` (in the shipped database): AAPL and NVDA on 2025-09-12, 2026-01-09, 2026-05-15 and 2026-09-11, Market and Fundamentals, memory off, TradingAgents 0.4.0.

| Check | Result |
|---|---|
| Runs | 8 of 8 finished |
| Cost | $0.30 in total, $0.033 to $0.044 per run |
| Time | 3.7 to 5.5 minutes per run, two in parallel |
| Ratings | 8 of 8 Hold, the research manager and the trader also Hold on every date |

Replayed on 23 September 2026 over 256 trading days from 2025-09-12, at 10 bps (the same numbers the results page shows at that cost setting):

| Strategy | AAPL | NVDA | Equal weight |
|---|---:|---:|---:|
| Agents, trader levels | -6.0% (5 trades) | -7.4% (7 trades) | -6.7% |
| Agents, rating only | 0.0% (no trades) | 0.0% | 0.0% |
| Buy and hold | +43.5% | +29.6% | +36.6% |
| 50/200-day MA rule | +31.0% | +29.6% | +30.3% |

Prices are dividend adjusted and refreshed daily, so a later replay can move these figures by a point or two; a replay on 14 September 2026 over 250 days gave -2.8% and -7.8% for the agents against +40.6% and +24.5% for buy and hold. Every level-based entry was stopped out, mostly within days or weeks. Four decisions per stock is a method check, not evidence.

## What the pilot taught

- Hold bias came from the prompt, not from missing data. Two variants on the same eight decisions: restoring the earlier, more decisive manager wording gave 4 Overweight, 2 Underweight and 2 Hold; adding SEC EDGAR statements gave 8 Hold. Upstream later dropped the over-cautious condition from the Hold rule (commit `62d3479`, 2026-09-14), and on 0.5.0 the same AAPL and NVDA dates come out Overweight.
- Two runs on the same ticker and date can differ. Any claim about ratings needs reruns, which is what the noise-estimate stage is for.
- The most careful public evaluation of this class of systems is FINSABER (arXiv 2505.07078); see [backtest-research.md](backtest-research.md) for what other projects did and what to avoid.
