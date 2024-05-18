from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.environments.app import environment_sub_app
from amsdal_cli.commands.cloud.environments.utils import set_current_environment
from amsdal_cli.utils.cli_config import CliConfig


@environment_sub_app.command(name='checkout, co')
def environments_checkout(ctx: typer.Context, env_name: str) -> None:
    """
    Change the current environment.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        list_response = manager.cloud_actions_manager.list_envs(
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e

    if not list_response:
        return

    if not list_response.details or not list_response.details.environments:
        print('[dark_orange]No environments found. Please create one first.[/dark_orange]')
        return

    if env_name not in list_response.details.environments:
        print(f'[dark_orange]Environment [dark_cyan]{env_name}[/dark_cyan] not found.[dark_orange]')
        return

    set_current_environment(ctx, env_name)
    print(f'[blue]Environment changed to [dark_cyan]{env_name}[/dark_cyan][blue]')
