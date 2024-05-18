import typing
from pathlib import Path
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig


@cloud_sub_app.command(name='expose-db, expose_db, edb')
def expose_db_command(
    ctx: typer.Context,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
    ip_address: Optional[str] = None,  # noqa: UP007
) -> None:
    """
    Add your IP to the allowlist of the database and return the connection configs.
    """

    env_name = env_name or get_current_env(ctx)
    cli_config: CliConfig = ctx.meta['config']

    if cli_config.verbose:
        print(f'[blue]Exposing database for environment: [dark_cyan]{env_name}[/dark_cyan][/blue]')

    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.expose_db(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            ip_address=ip_address,
        )
        print(response)
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return
