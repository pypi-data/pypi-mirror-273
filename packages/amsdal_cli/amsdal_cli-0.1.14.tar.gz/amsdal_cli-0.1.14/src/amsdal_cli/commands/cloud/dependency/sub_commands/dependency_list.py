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

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.commands.cloud.dependency.app import deprecated_dependency_sub_app
from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.utils.cli_config import CliConfig


@deprecated_dependency_sub_app.command(name='list', deprecated=True)
def dependency_list_command(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    all_deps: bool = Option(False, '--all', '-a', help='List all dependencies.'),
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
    sync: bool = Option(
        False,
        '--sync',
        help='Sync the dependencies from the Cloud Server to ".dependencies".',
    ),
) -> None:
    """
    List the app dependencies on the Cloud Server.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        list_response = manager.cloud_actions_manager.list_dependencies(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e

    if sync:
        _deps_path: Path = cli_config.app_directory / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps_path.write_text('\n'.join(list_response.dependencies))

    if not list_response:
        return

    if output == OutputFormat.json:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.dependencies:
        print('No dependencies found.')
        return

    data_table = Table()

    if all_deps:
        data_table.add_column('Dependency Name', justify='left')
        data_table.add_column('Status', justify='left')

        for dependency in list_response.all:
            is_installed = dependency in list_response.dependencies
            data_table.add_row(
                f'[green]{dependency}[/green]' if is_installed else f'[i]{dependency}[/i]',
                '[green]Installed[/green]' if is_installed else '[i]Not Installed[/i]',
            )

    else:
        data_table.add_column('Dependency Name', justify='center')

        for dependency in list_response.dependencies:
            data_table.add_row(dependency)

    print(data_table)


@dependency_sub_app.callback(invoke_without_command=True)
def dependency_list_callback(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    all_deps: bool = Option(False, '--all', '-a', help='List all dependencies.'),
    sync: bool = Option(
        False,
        '--sync',
        help='Sync the dependencies from the Cloud Server to ".dependencies".',
    ),
) -> None:
    """
    Lists the app dependencies on the Cloud Server.
    """

    if ctx.invoked_subcommand is not None:
        return

    dependency_list_command(
        ctx=ctx,
        output=output,
        all_deps=all_deps,
        sync=sync,
    )
