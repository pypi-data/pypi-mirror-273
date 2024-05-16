import json
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table
from typer import Option

from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.commands.cloud.security.basic_auth.app import basic_auth_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@basic_auth_sub_app.command(name='retrieve')
def retrieve_basic_auth_command(
    ctx: typer.Context,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
    *,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
) -> None:
    """
    Retrieves the Basic Auth credentials for the application API.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.get_basic_auth_credentials(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    if not response.details:
        return

    if output == OutputFormat.json:
        print(json.dumps(response.details.model_dump(), indent=4))
        return

    data_table = Table()

    data_table.add_column('Username', justify='center')
    data_table.add_column('Password', justify='center')

    data_table.add_row(
        response.details.username,
        response.details.password,
    )

    print(data_table)
