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
from glbuild import GitlabBuild

glb = GitLabBuild(host="https://gitlab.com", token="***")

glb.get(project=[14, 31], path="./data/")
```

Use in a Bash command line as follows:

```bash
glbuild init --host=https://gitlab.com --token=***
```

```bash
glbuild get --project=14,31 --path=./data/
```
