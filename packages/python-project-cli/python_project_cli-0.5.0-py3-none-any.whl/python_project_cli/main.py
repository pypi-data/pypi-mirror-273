from enum import StrEnum
from subprocess import run
from rich.console import Console
from rich.table import Table
from rich import print
import typer
from typing_extensions import Annotated

__version__ = '0.5.0'

app = typer.Typer(add_completion=False)
console = Console()


class Frameworks(StrEnum):
    django = 'Django'
    fast_api = 'FastAPI'


REPO_URLS = {
    Frameworks.django: 'https://github.com/MentorMate/mentormate-django-cookiecutter-template',
    Frameworks.fast_api: 'https://github.com/gp-mentormate/fastapi-cookiecutter-template',
}


def generate_framework(framework_name: Frameworks) -> None:
    match framework_name:
        case Frameworks.django:
            repo_url = REPO_URLS[Frameworks.django]
        case Frameworks.fast_api:
            repo_url = REPO_URLS[Frameworks.fast_api]
    print(f'[bold]Generating {framework_name} framework...[bold]')
    run(['cookiecutter', repo_url])


@app.command(
    help=f"""
        Interactive CLI for creating a project for the following frameworks:
        [{Frameworks.django}, {Frameworks.fast_api}]"""
)
def generate(
    choice: Annotated[
        Frameworks,
        typer.Option(
            prompt='Please select a framework',
            case_sensitive=True,
        ),
    ],
) -> None:
    generate_framework(choice)


@app.command(help='Framework repo status.')
def status() -> None:
    table = Table('Framework', 'Repo URL', 'Status')
    table.add_row(
        f'[bold]{Frameworks.django}[bold]',
        f'[blue]{REPO_URLS[Frameworks.django]}[blue]',
        ':white_check_mark:',
    )
    table.add_row(
        f'[bold]{Frameworks.fast_api}[bold]',
        f'[blue]{REPO_URLS[Frameworks.fast_api]}[blue]',
        ':x:',
    )
    console.print(table)


@app.command(help='CLI version.')
def version() -> None:
    print(f'[bold]CLI Version:[bold] {__version__}')
