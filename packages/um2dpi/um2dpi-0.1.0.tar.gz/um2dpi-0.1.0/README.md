# um2dpi

Python package to convert drop-spacing in micrometres to dots per inch (DPI).

## Index

- [um2dpi](#um2dpi)
  - [Index](#index)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Development](#development)
    - [Clone and setup](#clone-and-setup)
    - [Run tests](#run-tests)

## Installation

Install the package from PyPI:

```bash
pip install um2dpi
```

Or install the package from source:

```bash
gh repo clone fabio-terranova/um2dpi
cd um2dpi
pip install .
```

## Usage

```bash
um2dpi <ds> [<ds> ...]
```

Where `<ds>` is the drop-spacing in micrometres. For example:

```bash
um2dpi 10 20 30
```

Will output:

```bash
10.0 μm: 2540.00 dpi
20.0 μm: 1270.00 dpi
30.0 μm: 846.67 dpi
```

## Development

### Clone and setup

```bash
gh repo clone fabio-terranova/um2dpi
cd um2dpi
pipenv install --dev
pipenv run pre-commit install
```

### Run tests

```bash
pipenv run pytest
```
