from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.commands.cloud.security.basic_auth.app import basic_auth_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@basic_auth_sub_app.command(name='delete, del, d')
def delete_basic_auth_command(
    ctx: typer.Context,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
) -> None:
    """
    Deletes the Basic Auth for the application API.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.delete_basic_auth(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    print(
        'Basic Auth credentials have been deleted from the application API. '
        'Please wait a few minutes for the changes to take effect.'
    )
