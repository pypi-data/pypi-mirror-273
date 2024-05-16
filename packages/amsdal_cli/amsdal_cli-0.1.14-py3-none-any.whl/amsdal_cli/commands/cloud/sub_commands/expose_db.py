from pathlib import Path
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.utils.cli_config import CliConfig


@cloud_sub_app.command(name='expose-db, expose_db, edb')
def expose_db_command(
    ctx: typer.Context,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
    ip_address: Optional[str] = None,  # noqa: UP007
) -> None:
    """
    Add your IP to the allowlist of the database and return the connection configs.
    """

    cli_config: CliConfig = ctx.meta['config']
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
