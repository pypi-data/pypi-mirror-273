import json
import typing
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table
from typer import Option

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig


@cloud_sub_app.command(name='get-monitoring-info, get_monitoring_info, gmi')
def get_monitoring_info(
    ctx: typer.Context,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
) -> None:
    """
    Get monitoring info.
    """

    env_name = env_name or get_current_env(ctx)
    cli_config: CliConfig = ctx.meta['config']

    if cli_config.verbose:
        print(f'[blue]Retrieving monitoring info for environment: [dark_cyan]{env_name}[/dark_cyan][/blue]')

    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.get_monitoring_info(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    if not response.details:
        print('No monitoring info found.')
        return

    if output == OutputFormat.json:
        print(json.dumps(response.details.model_dump(), indent=4))
        return

    data_table = Table()
    data_table.add_column('URL', justify='center')
    data_table.add_column('Username', justify='center')
    data_table.add_column('Password', justify='center')

    data_table.add_row(response.details.url, response.details.username, response.details.password)

    print(data_table)
