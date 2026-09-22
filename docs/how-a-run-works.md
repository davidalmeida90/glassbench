# TradingAgents: how a run works

Reference notes from the first run, SPY on 2026-09-13, with all 4 analysts selected and DeepSeek as the provider (`deepseek-v4-flash` quick, `deepseek-v4-pro` deep). Repo: TauricResearch/TradingAgents, commit `be952b8` (v0.4.2).

---

## 1. 12 agents in two groups

```
 ┌─ OPTIONAL: pick 1 to 4 in the CLI ────────────────────────────────┐
 │  DATA ANALYSTS: fetch data with tools, write reports              │
 │  Market · Sentiment · News · Fundamentals                         │
 └───────────────────────────────────────────────────────────────────┘
                              │ reports
                              ▼
 ┌─ ALWAYS ON: 8 roles ──────────────────────────────────────────────┐
 │  REASONERS: no tools, read reports and each other's text          │
 │  Bull · Bear · Research Manager                                   │
 │  Trader                                                           │
 │  Aggressive · Conservative · Neutral · Portfolio Manager          │
 └───────────────────────────────────────────────────────────────────┘
```

- "Agents: X/12" in the CLI = 4 selected analysts + 8 fixed roles. With 2 analysts it shows /10.
- All 12 use the LLM. Reasoners make one call each and have no tools.
- Roles are hardcoded prompts in Python files. Bull always argues for buying and Bear always argues against, whatever the data says.
- Speaking order is fixed in `graph/setup.py`; debate length is a Python counter in `graph/conditional_logic.py`.
- Deselecting an analyst removes only that report. All 8 reasoners still run, with that report empty.
- Naming trap: Aggressive, Conservative and Neutral are called "Analyst" in the code but are debaters with no data access.

---

## 2. Data analysts

| # | Agent | What it does | Reads | Tool calls (examples from the SPY run) | LLM usage | Output |
|---|---|---|---|---|---|---|
| 1 | **Market Analyst** | Technical analysis: trend, momentum, volatility, key price levels | its own tool data only | `get_stock_data(SPY, 2026-03-01→09-13)`, `get_verified_market_snapshot(SPY)`, `get_indicators(rsi)`, `get_indicators(macd)`, `get_indicators(close_200_sma)`, 5 more indicators | **flash**, tool loop. **3 calls**: ask for data, ask for indicators, write report. 10 tools in 2 parallel batches | `market_report` (free text, ends with a BUY/HOLD/SELL line) |
| 2 | **Sentiment Analyst** | Crowd mood from news headlines, StockTwits and Reddit | data Python fetched **before** the LLM call | none: Python pre-fetches Yahoo news (7 days), 30 StockTwits posts, Reddit r/wallstreetbets, r/stocks, r/investing | **flash**, **1 call**, structured output (`SentimentReport`: score 0-10, band, confidence, narrative) | `sentiment_report`: "Mixed, 4.8/10, medium" |
| 3 | **News Analyst** | Macro and news: Fed, rates, inflation, events, prediction markets | its own tool data only | `get_news(SPY)`, `get_global_news(limit=25)`, `get_macro_indicators(cpi)`, `(10y_treasury)`, `(vix)`, `get_prediction_markets("Fed rate hike September")`, `("recession 2026")` | **flash**, tool loop. **3 calls**. 19 tools in 2 batches; went back for 8 more on its own | `news_report`: "78% Fed hike odds, 10Y at 4.95%, cautious" |
| 4 | **Fundamentals Analyst** | Company financials: valuation, balance sheet, income, cash flow | its own tool data only | `get_fundamentals(SPY)`, `get_balance_sheet`, `get_income_statement`, `get_cashflow` (last 3 returned `NO_DATA`, SPY is an ETF) | **flash**, tool loop. **2 calls**. 4 tools in 1 batch | `fundamentals_report`: "P/E 24.7, uptrend, expensive" |

`get_insider_transactions` is registered in the news tool node but not in the tool list handed to the LLM, so it never gets called.

## 3. Reasoners

| # | Agent | What it does | Reads | Tool calls | LLM usage | Output |
|---|---|---|---|---|---|---|
| 5 | **Bull Researcher** | Argues **for** buying, rebuts the Bear | 4 reports + debate history + Bear's last argument | none | **flash**, **1 call** per turn, free text | adds its argument to `investment_debate_state` |
| 6 | **Bear Researcher** | Argues **against**, rebuts the Bull | 4 reports + debate history + Bull's last argument | none | **flash**, **1 call** per turn, free text | adds its argument to `investment_debate_state` |
| 7 | **Research Manager** | Judges the debate, picks rating and plan | **Bull/Bear debate only**, no reports | none | **PRO**, **1 call**, structured (`ResearchPlan`: recommendation, rationale, strategic_actions) | `investment_plan`: "Hold; add above 766.88, exit below 758" |
| 8 | **Trader** | Turns the plan into a concrete trade | plan + market report only | none | **flash**, **1 call**, structured (`TraderProposal`: action, entry, stop, sizing) | `trader_investment_plan`: Hold, entry 766.88, stop 757.5 |
| 9 | **Aggressive Analyst** | Debates for more risk and upside | 4 reports + Trader plan + risk debate | none | **flash**, **1 call** per turn, free text | "Coiled-spring hold, 2:1 reward" |
| 10 | **Conservative Analyst** | Debates for protecting capital | 4 reports + Trader plan + risk debate | none | **flash**, **1 call** per turn, free text | "Fed binary risk, gap risk through the stop" |
| 11 | **Neutral Analyst** | Balances the two | 4 reports + Trader plan + risk debate | none | **flash**, **1 call** per turn, free text | "Keep neutral size, wait for triggers" |
| 12 | **Portfolio Manager** | Final decision | Research plan + Trader plan + risk debate + past lessons (API path only) | none | **PRO**, **1 call**, structured (`PortfolioDecision`: rating, summary, thesis, target, horizon) | `final_trade_decision`: **Hold, 1-3 months** |

### Run totals (SPY, 2026-09-13)

| | LLM calls | Model | Tool calls |
|---|---|---|---|
| 4 data analysts | 9 | flash | 33 |
| 6 debaters + Trader | 7 | flash | 0 |
| 2 managers | 2 | **pro** | 0 |
| **Total** | **17** | 15 flash, 2 pro | **33** |

Wall time 7m28s. Analysts: Market 32s, Sentiment 94s (Reddit rate limit), News 32s, Fundamentals 14s.

---

## 4. Sequence: what runs in order and what runs in parallel

`═══` = runs in parallel. Everything else is one step at a time.

```
 TIME      STEP                                          MODE
 ────────  ────────────────────────────────────────────  ─────────────────────
 18:30:28  START  SPY · 2026-09-13
              │
           ┌──┴─ MARKET ANALYST ───────────────────────┐
 18:30:30  │ ① LLM call (flash) → asks for 2 tools     │  sequential
           │   ╔═ get_stock_data                       │
           │   ╚═ get_verified_market_snapshot         │  PARALLEL (2)
 18:30:35  │ ② LLM call (flash) → asks for 8 tools     │  sequential
           │   ╔═ EMA10 ═ SMA50 ═ SMA200 ═ MACD        │
           │   ╚═ RSI ═ Boll ═ ATR ═ VWMA              │  PARALLEL (8)
 18:31:00  │ ③ LLM call (flash) → writes report        │  sequential
           └──┬─ wipe messages ────────────────────────┘
              │
           ┌──┴─ SENTIMENT ANALYST ────────────────────┐
           │   Yahoo news → StockTwits → Reddit        │  sequential fetches
           │   (Reddit 429 → waits ~70s → retries)     │  ← the 94s bottleneck
 18:32:33  │ ① LLM call (flash) → writes report        │  sequential
           └──┬─ wipe messages ────────────────────────┘
              │
           ┌──┴─ NEWS ANALYST ─────────────────────────┐
 18:32:36  │ ① LLM call (flash) → asks for 11 tools    │  sequential
           │   ╔═ news ═ global news ═ 7 FRED series   │
           │   ╚═ 2 Polymarket searches                │  PARALLEL (11)
 18:32:42  │ ② LLM call (flash) → asks for 8 more      │  sequential
           │   ╔═ 3 FRED ═ 4 Polymarket                │
           │   ╚═ global news                          │  PARALLEL (8)
 18:33:05  │ ③ LLM call (flash) → writes report        │  sequential
           └──┬─ wipe messages ────────────────────────┘
              │
           ┌──┴─ FUNDAMENTALS ANALYST ─────────────────┐
 18:33:07  │ ① LLM call (flash) → asks for 4 tools     │  sequential
           │   ╔═ fundamentals ═ balance sheet         │
           │   ╚═ income stmt ═ cash flow              │  PARALLEL (4)
 18:33:19  │ ② LLM call (flash) → writes report        │  sequential
           └──┬─ wipe messages ────────────────────────┘
              │
              ├─ Bull            LLM call (flash)           sequential
              ├─ Bear            LLM call (flash)           sequential
              ├─ Research Mgr    LLM call (PRO)  → HOLD     sequential
 18:35:24     ├─ Trader          LLM call (flash) → HOLD    sequential
              ├─ Aggressive      LLM call (flash)           sequential
              ├─ Conservative    LLM call (flash)           sequential
              ├─ Neutral         LLM call (flash)           sequential
              ├─ Portfolio Mgr   LLM call (PRO)  → rating   sequential
              │
              ├─ regex extracts "Hold"   (no LLM)           sequential
 18:37:56  END ─ reports written
```

| What | Parallel? | Why |
|---|---|---|
| LLM calls (all 17) | ❌ never | One straight chain of nodes; a node starts only after the previous one returns |
| Tool calls within one round (33 in 6 batches) | ✅ yes | LangGraph `ToolNode` runs them in a thread pool; all 8 indicators share the 18:30:35 timestamp |
| Tool rounds within one analyst | ❌ | Round 2 needs the LLM to read round 1's results first |
| The 4 analysts | ❌ | Run one after another although none needs another's output |
| Sentiment fetches | ❌ | Plain Python, three functions in order; one Reddit backoff stalls the run |
| Debaters | ❌ | Each speaker reads the previous argument first |

Speed-up available: the 4 analysts are independent, so running them in parallel would cut the analyst phase from 2m51s to roughly the slowest one (~1m34s).

---

## 5. Hand-off: what each reasoner receives

```
 ① Market ─┐
 ② Sentiment ─┤  4 reports filed in the shared state
 ③ News ────┤
 ④ Fundamentals ─┘
        │
        ▼
 ⑤ BULL (opens)
    gets: 4 reports
        + marker saying the bear has not spoken yet, open with your own case
    writes: Bull argument #1
        │
        ▼
 ⑥ BEAR
    gets: 4 reports + Bull argument #1
    writes: Bear argument #1 (rebuttal)
        │
        ▼   counter = 2 → debate over (1 round)
 ⑦ RESEARCH MANAGER (PRO)
    gets: Bull + Bear arguments ONLY            ✗ no reports
    writes: investment_plan → "Hold"
        │
        ▼
 ⑧ TRADER
    gets: investment_plan + market report ONLY  ✗ no sentiment/news/fundamentals
    writes: trader plan → Hold, entry 766.88, stop 757.5
        │
        ▼
 ⑨ AGGRESSIVE (opens)
    gets: 4 reports + trader plan
    writes: Aggressive argument
        │
        ▼
 ⑩ CONSERVATIVE
    gets: 4 reports + trader plan + Aggressive argument
    writes: Conservative argument
        │
        ▼
 ⑪ NEUTRAL
    gets: 4 reports + trader plan + Aggressive + Conservative
    writes: Neutral argument
        │
        ▼   counter = 3 → debate over (1 round)
 ⑫ PORTFOLIO MANAGER (PRO)
    gets: investment_plan + trader plan + all 3 risk arguments ONLY   ✗ no reports
    writes: final decision → "Hold, 1-3 months"
```

| Step | Agent | Gets the 4 reports directly? |
|---|---|---|
| ⑤ ⑥ | Bull, Bear | ✅ yes |
| ⑦ | Research Manager | ❌ only the debate |
| ⑧ | Trader | ⚠️ only the market report |
| ⑨ ⑩ ⑪ | Aggressive, Conservative, Neutral | ✅ yes, plus the trader plan |
| ⑫ | Portfolio Manager | ❌ only plans and the risk debate |

Reports enter twice: into the research debate (⑤ ⑥) and into the risk debate (⑨ ⑩ ⑪). Both managers decide from what the debaters said. Once ⑦ said Hold, every later agent reacted to that plan, which is why the whole SPY run converged on Hold.

---

## 6. Inside an analyst: 3 nodes in one graph

One single LangGraph `StateGraph` holds all 20 nodes. Each analyst is 3 of them plus one conditional edge:

```
                    ┌─────────────────────────────┐
                    ▼                             │
          ┌───────────────────┐   tool calls?   ┌─┴───────────────┐
 ───────► │  Market Analyst   │ ───── YES ────► │  tools_market   │
          │  (LLM node)       │                 │  (ToolNode:     │
          └───────────────────┘                 │  runs Python    │
                    │                           │  functions)     │
                    │ NO                        └─────────────────┘
                    ▼
          ┌───────────────────┐
          │ Msg Clear Market  │  (wipe node, no LLM)
          └───────────────────┘
                    │
                    ▼  next analyst's LLM node
```

Sentiment has the same wiring, but its LLM gets no tools, so its tool node never runs.

### The wipe

```
                   ┌──────────────────────── AgentState ────────────────────────┐
                   │  messages  (scratchpad)          reports  (filing cabinet) │
                   │  tool requests                   market_report             │
                   │  raw tool data (CSV, FRED...)    sentiment_report          │
                   │  drafts, final report text       news_report               │
                   │                                  fundamentals_report       │
                   └────────────────────────────────────────────────────────────┘
```

- An analyst's prompt = its own instructions + `messages`. No analyst reads another analyst's report.
- After each analyst, `Msg Clear` deletes every message and leaves one placeholder ("Proceed with your assigned analysis... SPY... 2026-09-13"). Those are the `[User] Proceed with...` lines in `message_tool.log`.
- Reasons: keeps context small, keeps analysts independent, avoids provider confusion from another agent's tool calls.
- Side effect: sentiment and news both read the same Yahoo articles about AI concentration, so one source reached the debate looking like two confirmations.

---

## 7. Practical notes

- **CLI skips memory.** `cli/main.py` streams the graph directly instead of calling `propagate()`, so a CLI run never writes `trading_memory.md`, never scores past decisions, never injects lessons, and never writes `full_states_log_*.json`. Use `run_one.py` for runs that should feed memory.
- **Memory scoring** measures a 5-trading-day return vs the benchmark, whatever the rating said. For SPY the benchmark is SPY, so alpha is always 0; use single stocks.
- **Use today's date.** Yahoo returns only the latest 10-20 articles, so a past date gets an empty news feed, and company profile fields are withheld for past dates.
- **Data sources.** yfinance for prices, indicators, fundamentals, news and insiders; FRED for macro; Polymarket; StockTwits; Reddit. No Finnhub (removed 2025-09-26).
- **Launch.** `.\ta.ps1` from `trading_agents/` in the VS Code terminal (loads only `DEEPSEEK_API_KEY` and `FRED_API_KEY`). Reports land in `results/<TICKER>/<date>/`.
