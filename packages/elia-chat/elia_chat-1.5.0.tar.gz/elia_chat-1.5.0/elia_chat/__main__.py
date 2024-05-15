"""
Elia CLI
"""

import asyncio
import pathlib
from textwrap import dedent
import tomllib
from typing import Any, Tuple

import click
from click_default_group import DefaultGroup

from rich.console import Console

from elia_chat.app import Elia
from elia_chat.config import LaunchConfig
from elia_chat.database.import_chatgpt import import_chatgpt_data
from elia_chat.database.database import create_database, sqlite_file_name
from elia_chat.launch_args import QuickLaunchArgs
from elia_chat.locations import config_file

console = Console()


def create_db_if_not_exists() -> None:
    if not sqlite_file_name.exists():
        click.echo(f"Creating database at {sqlite_file_name!r}")
        asyncio.run(create_database())


def load_or_create_config_file() -> dict[str, Any]:
    config = config_file()

    try:
        file_config = tomllib.loads(config.read_text())
    except FileNotFoundError:
        file_config = {}
        try:
            config.touch()
        except OSError:
            pass

    return file_config


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli() -> None:
    """Interact with large language models using your terminal."""


@cli.command()
@click.argument("prompt", nargs=-1, type=str, required=False)
def default(prompt: tuple[str, ...]):
    prompt = prompt or ("",)
    joined_prompt = " ".join(prompt)
    create_db_if_not_exists()
    file_config = load_or_create_config_file()
    app = Elia(LaunchConfig(**file_config), startup_prompt=joined_prompt)
    app.run()


@cli.command()
def reset() -> None:
    """
    Reset the database

    This command will delete the database file and recreate it.
    Previously saved conversations and data will be lost.
    """
    from rich.padding import Padding
    from rich.text import Text

    console.print(
        Padding(
            Text.from_markup(
                dedent(f"""\
[u b red]Warning![/]

[b red]This will delete all messages and chats.[/]

You may wish to create a backup of \
"[bold blue u]{str(sqlite_file_name.resolve().absolute())}[/]" before continuing.
            """)
            ),
            pad=(1, 2),
        )
    )
    if click.confirm("Delete all chats?", abort=True):
        sqlite_file_name.unlink(missing_ok=True)
        asyncio.run(create_database())
        console.print(f"♻️  Database reset @ {sqlite_file_name}")


@cli.command("import")
@click.argument(
    "file",
    type=click.Path(
        exists=True, dir_okay=False, path_type=pathlib.Path, resolve_path=True
    ),
)
def import_file_to_db(file: pathlib.Path) -> None:
    """
    Import ChatGPT Conversations

    This command will import the ChatGPT conversations from a local
    JSON file into the database.
    """
    asyncio.run(import_chatgpt_data(file=file))
    console.print(f"[green]ChatGPT data imported from {str(file)!r}")


@cli.command()
@click.argument("message", nargs=-1, type=str, required=True)
@click.option(
    "-m",
    "--model",
    type=str,
    default="gpt-3.5-turbo",
    help="The model to use for the chat",
)
def chat(message: Tuple[str, ...], model: str) -> None:
    """
    Start Elia with a chat message
    """
    quick_launch_args = QuickLaunchArgs(
        launch_prompt=" ".join(message),
        launch_prompt_model_name=model,
    )
    launch_config = LaunchConfig(
        default_model=quick_launch_args.launch_prompt_model_name,
    )
    app = Elia(launch_config, quick_launch_args.launch_prompt)
    app.run()


if __name__ == "__main__":
    cli()
