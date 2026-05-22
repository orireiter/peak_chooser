# peak-chooser

A small utility to detect peaks in a two-column CSV (time, value).

## Installation

- Requirements: Python >= 3.13 (see `pyproject.toml`).


After cloning and cd-ing into the repository's root:
```
pip install .
```

## Example Usage

```
choose_peaks sample_1.csv -d "," --plot --prominence 0.5 --distance 10 -o csv > peaks.csv
```

## CLI options

- `csv_path` : Path to the input CSV file (required).
- `-d`, `--delimiter` : Delimiter used in the CSV file (defaults to tab `\t` due to Excel).
- `--prominence` : Minimum prominence of peaks.
- `--distance` : Minimum distance between peaks (in data points).
- `--plot` : Show visualization plots.
- `-o`, `--output` : Output format, either `echo` (default) or `csv`.

For more details, see the code in [main.py](main.py).
