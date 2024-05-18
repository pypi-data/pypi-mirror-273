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


@dependency_sub_app.command(name='delete, del, d')
def dependency_delete_command(
    ctx: typer.Context,
    dependency_name: str,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
) -> None:
    """
    Deletes dependency from your Cloud Server app.
    """
    cli_config: CliConfig = ctx.meta['config']
    env_name = env_name or get_current_env(ctx)

    if cli_config.verbose:
        print(
            f'[blue]Deleting dependency [dark_cyan]{dependency_name}[/dark_cyan] from environment: '
            f'[dark_cyan]{env_name}[/dark_cyan][/blue]'
        )

    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.delete_dependency(
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

        if dependency_name in _deps:
            _deps.remove(dependency_name)
            _deps_path.write_text('\n'.join(_deps))

    print('[green]Dependency deleted successfully[/green]')


@deprecated_dependency_sub_app.command(name='delete', deprecated=True)
def deprecated_dependency_delete_command(
    ctx: typer.Context,
    dependency_name: str,
) -> None:
    """
    Delete dependency from your Cloud Server app.
    """

    dependency_delete_command(
        ctx=ctx,
        dependency_name=dependency_name,
    )
