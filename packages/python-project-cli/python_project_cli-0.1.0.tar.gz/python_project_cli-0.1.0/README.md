# MentorMate Python CLI
A CLI tool for generating Django and FastAPI projects.

![Tests](https://github.com/MentorMate/python-project-cli/actions/workflows/tests.yaml/badge.svg)

![Deploy](https://github.com/MentorMate/python-project-cli/actions/workflows/release.yaml/badge.svg)

## Overview
This is a python-cli tool for interactive project setup, following best practices for **Django** and **FastAPI**.
In order to assure easier distribution, the project is deployed as **pypi** package.
For optimal maintenance the project utilizes the **tox** framework.

## Installation
We use `pip` for our package distribution, that's why we recomend that you use virtual environment for the package instalation (`venv` or `poetr`).
```bash
(env) pip install python-project-cli
```

## Commands
- `python-cli generate` - starts interactive project generation, that uses cookiecutter.
- `python-cli status` - shows the framework repo status. We aim to update the main templates frequently, in order to keep up with the everevolving "best" practices, that's why there's a chance for a repo downtime.
- `python-cli version` - project version.

### Frameworks
- Django
- FastAPI

## Package Maintenance
**Main points**
1. In order to automate the release versioning we use `python-semantic-release`, which utilizes the [Angular Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/). That means that we need to adopt it in our commit messages (example below).
2. Make sure you `git pull` after every release, because the `pyproject.toml` and `CHANGELOG.md` will be automatically updated by `semantic-release`.
3. Include new members in `CODEOWNERS`

### Development
- Prerequisites:

  Install `poetry`. **Make sure you have pip3/pipx installed**
  ```bash
  pipx install poetry
  poetry install
  ```

- pre-commit setup
  Install the `pre-commit` hooks
  ```bash
  poetry run pre-commit install
  ```

- git pre-push hook
  Configure a pre-push hook that runs `tox` before pushing to the repository
  ```bash
  echo -e '#!/bin/sh\n\npoetry run tox' >> .git/hooks/pre-push
  chmod ug+x .git/hooks/pre-push
  ```

### Automatic package update
As a brief overview of the main types for angular's conventional commits:
  - `BREAKING CHANGE:` **in the commit's footer** will bump to a new major version `1.0.0` -> `2.0.0`
  - `feat:` will bump to a new minor version `1.0.0` -> `1.1.0`
  - `fix:`, `perf:` will bump to a new patch version `1.0.0` -> `1.0.1`
  - `ci:`, `docs:`, `tests:` etc. won't result in a new release, therefore won't be published in `pypi`

Example on how to check if our commit will result in new release version, before we push:
```bash
$ git commit -m"feat: Create a new major feature"
$ poetry run semantic-release -vv version --print
...
           INFO     [semantic_release.version.algorithm] INFO algorithm.tags_and_versions: found 6 previous tags                                                               algorithm.py:58
No release will be made, 0.4.0 has already been released!
...
```

### Manual package update - not recommended!
Prerequisites:

- Install `build` and `twine` on root.
```bash
python3 -m pip install --upgrade build
python -m pip pinstall --upgrade twine
```

- Configure **pypi** token in `~/.pypirc`
```
[testpypi]
  username = __token__
  password = <TOKEN>
```
- Update project version in `pyproject.toml` -> `version`
```toml
[project]
name = "python_project_cli"
version = "1.0.0"  #<--- new version here
```

- Build new .whl and .tar.gz
```bash
python3 -m build
```

- Upload new version to pypi 
```bash
twine upload --repository testpypi dist/*
```

## License

PYTHON-PROJECT-CLI is unlicensed, as found in the
[LICENSE](https://github.com/MentorMate/python-project-cli/blob/development/LICENSE) file.
