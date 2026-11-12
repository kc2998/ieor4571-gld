# IEOR 4571 Project: Trading Gold

Research and backtesting of trading strategies on gold. The scope is open: technical
analysis, macro and market drivers, positioning data, and ML models all plug into the
same backtest and validation code.

## Layout

The numbered folders hold exploration (notebooks, `.qmd` files, findings) in research order.
Reusable code lives in `src/gold/`, which uses plain names because Python cannot import a
module whose name starts with a digit.

```text
ieor4571-project/
├── configs/              # data settings and one yaml per experiment
├── 01_data/              # download and check data; raw/ and processed/ are gitignored
├── 02_eda/
│   ├── technical/        # price behavior, trends, volatility regimes
│   └── market/           # real yields, USD, positioning, ETF flows
├── 03_features/          # trying feature ideas before moving them into src/
├── 04_models/
│   ├── rule_based/       # moving average crossover, breakout, mean reversion
│   └── ml/               # logistic regression, gradient boosting, etc.
├── 05_backtest/          # running strategies and comparing equity curves
├── 06_evaluation/        # robustness, regime splits, parameter sensitivity
├── 07_report/            # final writeup, figures, slides
├── src/gold/
│   ├── data/             # sources (Yahoo, FRED, CFTC) and the aligned loader
│   ├── features/         # technical and market features
│   ├── models/           # strategies sharing one base class
│   ├── backtest/         # engine, transaction costs, sizing
│   └── validation/       # walk forward splits and metrics
├── scripts/              # entry points, e.g. run one experiment from a config
├── results/              # one folder per run (gitignored)
├── tests/
└── local/                # personal scratch, papers, notes (gitignored)
```

## Conventions

- **One strategy interface.** Every strategy in `src/gold/models/` returns a position series
  indexed by date with values in [-1, 1] (short to long). The backtester and validation code
  never need to know what kind of model produced it.
- **No look ahead.** Features on day t use data through day t only, and the position is
  applied to the return on day t+1.
- **Walk forward validation** instead of random splits, and transaction costs on by default.
- **Notebook names** carry their stage number and a short topic, for example
  `02_eda/market/02_real_yields_vs_gold.qmd`.
- **Move code into `src/gold/`** once the same function shows up in a second notebook.
- **Data is never committed.** Anything in `01_data/` must be rebuildable from the code there.
- **Run outputs** go to `results/<YYYYMMDD>_<short_name>/` with a copy of the config used.

## Setup

Requirements: [uv](https://docs.astral.sh/uv/) and [Quarto](https://quarto.org/).
Python 3.11 is pinned in `.python-version`; uv installs it if needed.

This folder is under `Documents`, which iCloud syncs. Keep the environment out of iCloud by
pointing `.venv` at a `.nosync` folder before the first sync:

```shell
cd ieor4571-project
mkdir .venv.nosync && ln -s .venv.nosync .venv
uv sync                 # core packages plus the dev group (pytest, ruff)
uv sync --group ml      # add scikit-learn and statsmodels when needed
```

`uv sync` also installs `src/gold` in editable mode, so `import gold` works everywhere.

Register the kernel that Quarto and Jupyter use:

```shell
uv run python -m ipykernel install --user --name ieor4571-project --display-name "Python (IEOR4571 Project)"
```

Then:

```shell
uv run jupyter lab                         # notebooks
quarto render 02_eda/market/01_example.qmd # render one .qmd
uv run pytest                              # tests
uv run ruff check .                        # lint
```

Add a package with `uv add <name>` (or `uv add --group ml <name>`) so `pyproject.toml` and
`uv.lock` stay in step.
