import json
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table

from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.environments.app import environment_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig


@environment_sub_app.callback(invoke_without_command=True)
def environments_list_callback(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
) -> None:
    """
    List the environments of the Cloud Server app.
    """

    if ctx.invoked_subcommand is not None:
        return

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

    if output == OutputFormat.json:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.details or not list_response.details.environments:
        print('No environments found.')
        return

    data_table = Table()
    data_table.add_column('Environment', justify='center')
    data_table.add_column('Current', justify='center')
    current_env_name = get_current_env(ctx)

    for env in list_response.details.environments:
        data_table.add_row(env, '*' if current_env_name == env else '')

    print(data_table)
