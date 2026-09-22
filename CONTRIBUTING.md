# Contributing

Thanks for looking at Glassbench. Issues and pull requests are welcome; the notes below keep them easy to review.

## Where things live

- **The engine stays untouched.** Everything Glassbench needs from TradingAgents goes through `backend/deskapp/adapter.py` (node names, state keys, parsers). If an engine update breaks something, the adapter tests say what changed; fix it there.
- **Changing how agents think is a variant.** Prompt wording, data vendors and similar go in `backend/deskapp/variants.py` and are applied per run through `runconfig.py`. A variant has a name, a description and a check that it still applies to the engine version in use.
- **Events are the record.** `capture.py` turns LangChain callbacks into numbered events, `store.py` keeps them in SQLite, `api.py` replays them. A new feature usually starts as a new event type or a new field on an existing one.
- **The frontend** is React with TypeScript under `frontend/src`, one page per route under `pages/`, shared pieces under `components/`.

## Running the checks

```powershell
cd backend
python -m unittest discover tests      # adapter, backtest, simulator, variants, run config, path containment
cd ../frontend
npm run typecheck && npm run build
```

Set `GLASSBENCH_ENGINE_DIR` if the engine clone is not at `./TradingAgents`.

## Pull requests

- One change per pull request, with the reason in the description and, when it touches a run, before and after numbers from a real run.
- Keep the tests green and add one when you fix a bug.
- No API keys, no run databases and no screenshots with keys in a pull request. The `.env` file is ignored on purpose.

## A second framework

The most useful contribution is an adapter for another open-source framework (AI Hedge Fund is first on the list). An adapter maps the framework's stages and agents onto Glassbench's event stream so that runs land in the same table as TradingAgents runs, with the framework name and version as the label. Open an issue first with the framework and the mapping you have in mind.
