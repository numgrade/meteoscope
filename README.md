# meteoscope

meteoscope analyzes a CSV file of weather observations and produces a report: descriptive statistics, missing values, duplicates, outliers, and a chart.

## Installation

```bash
python -m pip install --index-url https://test.pypi.org/simple/ meteoscope
```
or with uv :
```bash
$ uv run --with meteoscope \
    --default-index https://pypi.org/simple/ \
    --index https://test.pypi.org/simple/ \
    --no-project \
    -- python -c "import meteoscope; print(meteoscope.__version__)"

```

## How to use meteoscope

```bash
uv run meteoscope data/stations.csv --sortie rapport.json --plot temperature_c
```

## Développement

```bash
uv run pytest            # tests + couverture
uv run ruff check .      # lint
uv run mkdocs serve      # documentation
uv run tox               # tout vérifier
```
