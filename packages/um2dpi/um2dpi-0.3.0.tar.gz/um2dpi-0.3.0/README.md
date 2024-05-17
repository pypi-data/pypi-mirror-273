# um2dpi

[![PyPI](https://img.shields.io/pypi/v/um2dpi)](https://pypi.org/project/um2dpi/)

Python package to convert drop-spacing in micrometres to dots per inch (DPI).

## Index

- [um2dpi](#um2dpi)
  - [Index](#index)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Examples](#examples)
  - [Development](#development)
    - [Clone](#clone)
    - [Run tests](#run-tests)
    - [Build](#build)
    - [Publish](#publish)

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
um2dpi [-r] <value> [value ...]
```

  Where:
    - `-r`  will convert from DPI to micrometres.

### Examples

```bash
um2dpi 10 20 30
```

Will output:

```bash
10.0 μm: 2540.00 dpi
20.0 μm: 1270.00 dpi
30.0 μm: 846.67 dpi
```

```bash
um2dpi -r 2540 1270 846.67
```

Will output:

```bash
2540.0 dpi: 10.00 μm
1270.0 dpi: 20.00 μm
846.67 dpi: 30.00 μm
```

## Development

Using [Hatch](https://hatch.pypa.io/latest/#hatch) and [pre-commit](https://pre-commit.com/) for
development.

### Clone

```bash
gh repo clone fabio-terranova/um2dpi
cd um2dpi
hatch run pre-commit install
```

### Run tests

```bash
hatch test --cover
```

### Build

```bash
hatch build
```

### Publish

```bash
hatch publish
```
