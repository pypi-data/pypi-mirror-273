# glbuild

A tool to collect the entire history of build data and logs (at once) from GitLab projects.

## Requirements

- Python 3.10
- [Poetry](https://python-poetry.org/)

## Get started

Install dependencies

```bash
poetry install
```

Access virtual environment

```bash
poetry shell
```

Install pre-commit hook for static code analysis

```bash
pre-commit install
```

## Usage

Install the Python package using Pip

>```bash
>pip install glbuild
>```

Use in a Python script as follows:

```python
import glbuild

glb = glbuild.GitLabBuild(base_url="https://gitlab.com", token="******", projects=[1538, 5427])

glb.get(datapath="./data")
```

Use in a Bash command line as follows:

```bash
glbuild init --base_url=https://gitlab.com --token=****** --projects=1538,5427
```

```bash
glbuild get --datapath=./data
```
