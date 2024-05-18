from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.environments.app import environment_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@environment_sub_app.command(name='new, n')
def env_add_command(ctx: typer.Context, env_name: str) -> None:
    """
    Adds a new environment to your Cloud Server app.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.create_env(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e

    print(f'[green]Environment [dark_cyan]{env_name}[/dark_cyan] created successfully[/green]')
