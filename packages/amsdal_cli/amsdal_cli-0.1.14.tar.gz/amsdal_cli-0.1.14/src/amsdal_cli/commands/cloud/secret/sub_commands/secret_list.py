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
from amsdal_cli.commands.cloud.secret.app import deprecated_secret_sub_app
from amsdal_cli.commands.cloud.secret.app import secret_sub_app
from amsdal_cli.commands.cloud.secret.constants import DEFAULT_SECRETS
from amsdal_cli.utils.cli_config import CliConfig


@deprecated_secret_sub_app.command(name='list', deprecated=True)
def secret_list_command(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
    *,
    values: Annotated[bool, typer.Option('--values', '-v', help='Show secret values')] = False,
    sync: bool = Option(
        False,
        '--sync',
        help='Sync the dependencies from the Cloud Server to ".secrets".',
    ),
) -> None:
    """
    List the app secrets on the Cloud Server.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        list_response = manager.cloud_actions_manager.list_secrets(
            with_values=values,
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e

    if not list_response:
        return

    if sync:
        _secrets_path: Path = cli_config.app_directory / '.secrets'
        _secrets_path.touch(exist_ok=True)
        _secrets_path.write_text(
            '\n'.join(
                [
                    _secret.split('=', 1)[0]
                    for _secret in list_response.secrets
                    if _secret.split('=', 1)[0] not in DEFAULT_SECRETS
                ],
            ),
        )

    if output == OutputFormat.json:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.secrets:
        print('No secrets found.')
        return

    data_table = Table()
    data_table.add_column('Secret Name', justify='center')

    if values:
        data_table.add_column('Secret Value', justify='center')

    for secret in list_response.secrets:
        if values:
            secret_name, secret_value = secret.split('=', 1)
            data_table.add_row(secret_name, secret_value)
        else:
            data_table.add_row(secret)

    print(data_table)


@secret_sub_app.callback(invoke_without_command=True)
def secret_list_callback(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    values: Annotated[bool, typer.Option('--values', '-v', help='Show secret values')] = False,
    sync: bool = Option(
        False,
        '--sync',
        help='Sync the dependencies from the Cloud Server to ".secrets".',
    ),
) -> None:
    """
    List the app secrets on the Cloud Server.
    """

    if ctx.invoked_subcommand is not None:
        return

    secret_list_command(
        ctx=ctx,
        output=output,
        values=values,
        sync=sync,
    )
