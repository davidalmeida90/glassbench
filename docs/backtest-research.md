# Backtest research: how others tested TradingAgents

Collected 2026-09-13 from the actual code of existing projects (read through the GitHub API, nothing run), TradingAgents issues and commits, and two evaluation papers. Input for planning the Glassbench backtest (since built, see backtest.py and simulate.py).

## Headline findings

- **No trustworthy TradingAgents backtest exists publicly.** Tauric never released the paper's evaluation code (issues #119, #137 still open).
- **Leakage-aware tests find the agents lose to buy-and-hold.** trading-agents-lab (anonymised, 10 bps costs, AAPL Mar-Jun 2026): agents -0.9% vs buy-and-hold +15.7%, Sharpe -1.21 vs 2.66.
- **One signal-quality study found the ratings anti-predictive.** quanticsoul4772 fork: rank IC -0.073 at 5 days, -0.254 at 90 days (n=153, 10 tickers, 33 dates; window unverified).
- **Run-to-run noise is large.** ICAIF 2026 reproducibility paper (GOOG, May-Jul 2025): 15.8% ± 4.2% (GPT-4o) and 18.1% ± 2.8% (Qwen3) vs buy-and-hold 19.1%; a single seeded run showed 28.2%, which the authors call cherry-picking.
- **Model choice swings results wildly.** Agent Market Arena (live Aug-Sep 2025): TradingAgents-based agent on TSLA ranged -38.7% to +21.9% by model, vs buy-and-hold +46.9%.
- **Upstream fixed key look-ahead bugs:** `e111388` (#175, #203 data date filtering), `0c1231a` (#1007 future news), `8db41f6` (#1251 date-safe memory lessons). Any backtest must run on a version after these. The v0.4.2 clone used at the time included them; v0.5.0 does too.

## Project comparison

| Project | Past-date decisions | Look-ahead handling | Rating to position | Fills and costs | Metrics | Reruns | Result |
|---|---|---|---|---|---|---|---|
| AlpacaTradingAgent (264★) | replays recorded signals | replay clean; memory teaching unclear | BUY 95%, SELL flat, HOLD keep | backtrader next open, 10 bps + vol slippage | return, Sharpe, max DD, win rate; no benchmark | none | none |
| TradingAgents-AShare (824★) | live `propagate()` every N days | vendor filters only | BUY long, SELL scored as short (A-shares can't short), HOLD ignored | decision-day close; no costs | win rate, avg return | none | none |
| trading-agents-lab (0★, 62 tests) | own reimplementation, every 5 days, cached | anonymised tickers/dates/prices + memorisation probe | exposure in [-1, 1], HOLD carries | next close, 10 bps turnover | B&H, paper baselines, LightGBM | frozen cache | -0.9% vs +15.7% |
| AgenticTrading (722★) | runs TradingAgents, saves hashed artifact, replays | first hourly bar after analysis | Buy/Overweight BUY 25%, Hold, Underweight/Sell SELL all | hourly env; fees unverified | return, fills, rejections | 1 retry; errors kept apart from Holds | none |
| Mai0313 fork (3★) | live weekly/daily, USD budget cap, stub dry run | **leak:** daily mode feeds t+5 outcome into t+1 memory | signal × LLM size ≤ 0.2, SELL short | decision close, no costs | Sharpe on overlapping trades (wrong), hit rate | none | none |
| quanticsoul4772 fork (0★) | resumable weekly grid | upstream filters | 5-tier rating → score -2..+2 | close-based alpha vs SPY 5/10/21/90d | pooled and within-ticker Spearman IC | none | IC negative |
| TraderHarness (37★) | own A-share env, committee config | tool date filters, D+0 dates, pseudonyms, masked vs unmasked A/B | single executor | 5-min bars, minute matching | CSI 300, Sharpe, DD | recordings, seed 42 | claimed +1.45% to -2.69% vs index -9.12% (21 days) |
| quanterback, skopaqtrader, lucas replication | not agent-signal backtests (rule backtests or fallbacks) | varies; lucas uses `bfill` (leak) | long-only rules | same-close fills, one exits on the entry bar | varies | none | not meaningful |
| TradingAgents-CN (31.8k★) | **no backtest module** | | | | | | |
| BA2TradePlatform (11★) | excludes TradingAgents from backtests ("not replayable") | plans `as_of` data contract | | plans next-bar + fees | plans drop-best-K, shift weekday | | |

## Worth copying

1. Separate **generation** from **replay**: immutable decision artifacts (model, version, config hash, raw text, SHA-256), replayed for free.
2. **Next-open fills**; signals on non-trading days roll forward; superseded signals marked.
3. **Costs on by default**, slippage scaled to the prior bar's range.
4. **Errors are not Holds**: label, retry once, refuse to report if all dates failed.
5. **Anonymised mode** (rebased prices, masked tickers and dates) plus a memorisation probe.
6. **Perturbation test**: change future rows, assert past decisions identical.
7. **Within-ticker IC** next to pooled IC.
8. **Budget cap and stub-LLM dry run** before spending.
9. Upstream `as_of` memory filter; report by window (quarter), not one number.
10. Rerun spread as **mean ± standard error**.
11. Robustness: **drop the K best trades**, **shift the decision weekday**.

## Mistakes to avoid

1. Same-close fills; exiting on the entry bar's own high/low.
2. `bfill` on prices; silent `except:`; README numbers that differ from code.
3. Treating overlapping 5-day trades as independent; wrong annualisation; errors counted as zero-return Holds.
4. Scoring only BUY/SELL; shorting where shorting is impossible.
5. Feeding realised outcomes into memory before they would be known.
6. Fake walk-forward (nothing refit) and Monte Carlo that shuffles additive PnL (every path ends the same).
7. Freezing one seed or cache and calling it deterministic.
8. Position caps that block buys, making a flat curve look cautious.
9. One ticker, one quarter.
10. Pre-fix engine versions.

## What nobody has done (the opportunity)

1. **Reruns per (ticker, date)** with confidence intervals at portfolio level.
2. **Named vs anonymised A/B** and **pre- vs post-cutoff windows** per model on real TradingAgents: measure memorisation directly.
3. **Cross-sectional test**: many tickers per date, 5-tier rating IC and long-short spread (everyone else collapses to 3 actions).
4. **Random-signal placebo** with equal turnover, plus block bootstrap / deflated Sharpe.
5. **Ablations at equal LLM cost**: each analyst off, debate rounds, memory on/off, single-LLM baseline.
6. **Hold-semantics sensitivity** (keep / flatten / half) and decision-weekday sensitivity.
7. **Date-safe fundamentals** check (yfinance fundamentals may be current snapshots).

## Sources

- Repos: [AlpacaTradingAgent](https://github.com/huygiatrng/AlpacaTradingAgent), [TradingAgents-AShare](https://github.com/KylinMountain/TradingAgents-AShare), [trading-agents-lab](https://github.com/Kantamaniprakash/trading-agents-lab), [AgenticTrading](https://github.com/Open-Finance-Lab/AgenticTrading), [Mai0313/TradingAgents](https://github.com/Mai0313/TradingAgents), [quanticsoul4772/TradingAgents](https://github.com/quanticsoul4772/TradingAgents), [TraderHarness](https://github.com/HephaestLab/TraderHarness), [quanterback](https://github.com/Kiyo5hi/quanterback), [skopaqtrader](https://github.com/Skopaq-AI/skopaqtrader), [tradingagents_replicated](https://github.com/lucas020695/tradingagents_replicated), [BA2TradePlatform](https://github.com/bmigette/BA2TradePlatform), [TradingAgents-CN](https://github.com/hsliuping/TradingAgents-CN)
- TradingAgents issues: [#119](https://github.com/TauricResearch/TradingAgents/issues/119), [#137](https://github.com/TauricResearch/TradingAgents/issues/137), [#175](https://github.com/TauricResearch/TradingAgents/issues/175), [#203](https://github.com/TauricResearch/TradingAgents/issues/203), [#1007](https://github.com/TauricResearch/TradingAgents/issues/1007), [#1251](https://github.com/TauricResearch/TradingAgents/issues/1251)
- Papers: [Reproducibility in the TradingAgents Framework (ICAIF 2026)](https://dl.acm.org/doi/10.1145/3800973.3801029) (numbers from snippets, unverified), [Agent Market Arena](https://arxiv.org/html/2510.11695v2)
