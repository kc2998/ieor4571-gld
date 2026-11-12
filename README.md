# Trading Gold: IEOR 4571 Project

Research and backtesting of systematic trading strategies on gold (GLD and gold futures),
for IEOR 4571 at Columbia University.

The scope is open. Technical analysis, macro and market drivers, positioning data and ML
models all feed the same backtest and validation code, so any idea can be tested and
compared on equal terms.

## Quick start

Requirements: [uv](https://docs.astral.sh/uv/) and [Quarto](https://quarto.org/).
Python 3.11 is pinned in `.python-version`; uv installs it if needed.

```shell
git clone https://github.com/kc2998/ieor4571-gld.git
cd ieor4571-gld
uv sync
uv run python -c "import gold; print('ok')"
```

`uv sync` installs the exact versions in `uv.lock`, including the `dev` group (pytest, ruff),
and installs `src/gold` in editable mode so `import gold` works from any notebook or script.
For the ML packages (scikit-learn, statsmodels), run `uv sync --group ml`.

Register the Jupyter kernel that the notebooks and Quarto files use:

```shell
uv run python -m ipykernel install --user --name ieor4571-project --display-name "Python (IEOR4571 Project)"
```

Common commands:

| Task | Command |
|---|---|
| Open notebooks | `uv run jupyter lab` |
| Render a Quarto file | `quarto render 02_eda/market/01_example.qmd` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Add a package | `uv add <name>` or `uv add --group ml <name>` |

Always add packages with `uv add` so `pyproject.toml` and `uv.lock` stay in step, and commit
both files together.

## Repository structure

Numbered folders hold exploration (notebooks, `.qmd` files, findings) in research order.
Reusable code lives in `src/gold/`, which uses plain names because Python cannot import a
module whose name starts with a digit.

```text
.
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

## Naming conventions

| Item | Pattern | Example |
|---|---|---|
| Notebook or Quarto file | `NN_topic.ipynb` / `.qmd` inside its stage folder | `02_eda/market/02_real_yields_vs_gold.qmd` |
| Module in `src/gold/` | lowercase, one topic per file | `features/technical.py` |
| Experiment config | `configs/experiments/<short_name>.yaml` | `ma_crossover_50_200.yaml` |
| Run output | `results/<YYYYMMDD>_<short_name>/` | `results/20261115_ma_crossover_50_200/` |
| Branch | `<area>/<short_description>` | `eda/real_yields`, `model/breakout` |

Move a function into `src/gold/` once it is used in a second notebook.

## Workflow

1. Pull the latest `main`: `git switch main && git pull`.
2. Create a branch: `git switch -c eda/real_yields`.
3. Commit as you go, then push: `git push -u origin eda/real_yields`.
4. Open a pull request into `main` and ask a teammate to review.

Do not push directly to `main`. Clear notebook outputs before committing if they are large.

## Good to know

- **API keys** (for example FRED) go in a `.env` file at the repo root, which git ignores.
  Never put keys in code or notebooks.
- **Personal files** (papers, scratch notebooks) go in `local/`, which git ignores.
