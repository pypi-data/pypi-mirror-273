from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.commands.cloud.secret.app import deprecated_secret_sub_app
from amsdal_cli.commands.cloud.secret.app import secret_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@secret_sub_app.command(name='new, n')
def secret_add_command(
    ctx: typer.Context,
    secret_name: str,
    secret_value: str,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
) -> None:
    """
    Adds a new secret to your Cloud Server app.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.add_secret(
            secret_name=secret_name,
            secret_value=secret_value,
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e
    else:
        _secrets_path: Path = cli_config.app_directory / '.secrets'
        _secrets_path.touch(exist_ok=True)
        _secrets = set(_secrets_path.read_text().split('\n'))
        _secrets.add(secret_name)
        _secrets_path.write_text('\n'.join(_secrets))

    print('[green]Secret added successfully.[/green]')


@deprecated_secret_sub_app.command(name='add', deprecated=True)
def secret_add_command_deprecated(
    ctx: typer.Context,
    secret_name: str,
    secret_value: str,
) -> None:
    """
    Add secrets to your Cloud Server app.
    """

    secret_add_command(
        ctx=ctx,
        secret_name=secret_name,
        secret_value=secret_value,
    )
