# MentorMate Python CLI
A CLI tool for generating Django and FastAPI projects.

![Tests](https://github.com/MentorMate/python-project-cli/actions/workflows/tests.yaml/badge.svg)

![Deploy](https://github.com/MentorMate/python-project-cli/actions/workflows/main_release.yaml/badge.svg)

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



## License

PYTHON-PROJECT-CLI is unlicensed, as found in the
[LICENSE](https://github.com/MentorMate/python-project-cli/blob/development/LICENSE) file.
