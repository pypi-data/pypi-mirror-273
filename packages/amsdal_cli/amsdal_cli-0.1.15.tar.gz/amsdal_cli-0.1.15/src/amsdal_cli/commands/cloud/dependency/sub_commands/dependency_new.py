import typing
from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.commands.cloud.dependency.app import deprecated_dependency_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig


@dependency_sub_app.command(name='new, n')
def dependency_new_command(
    ctx: typer.Context,
    dependency_name: str,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
) -> None:
    """
    Creates a new dependency for your Cloud Server app.
    """

    env_name = env_name or get_current_env(ctx)
    cli_config: CliConfig = ctx.meta['config']

    if cli_config.verbose:
        print(
            f'[blue]Adding dependency [dark_cyan]{dependency_name}[/dark_cyan] to environment: '
            f'[dark_cyan]{env_name}[/dark_cyan][/blue]'
        )

    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.add_dependency(
            dependency_name=dependency_name,
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e
    else:
        config_dir: Path = cli_config.app_directory / '.amsdal'
        config_dir.mkdir(exist_ok=True, parents=True)
        _deps_path: Path = config_dir / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps = set(_deps_path.read_text().split('\n'))
        _deps.add(dependency_name)
        _deps_path.write_text('\n'.join(_deps))

    print('[green]Dependency added successfully[/green]')


@deprecated_dependency_sub_app.command(name='add', deprecated=True)
def dependency_add_command(
    ctx: typer.Context,
    dependency_name: str,
) -> None:
    """
    Add dependency to your Cloud Server app.
    """

    dependency_new_command(
        ctx=ctx,
        dependency_name=dependency_name,
    )
