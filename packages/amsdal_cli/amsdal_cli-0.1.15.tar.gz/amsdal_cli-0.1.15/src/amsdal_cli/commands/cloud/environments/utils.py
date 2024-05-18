from pathlib import Path

import typer
from rich import print

from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.utils.cli_config import CliConfig


def _get_enviroments_path(ctx: typer.Context) -> Path:
    cli_config: CliConfig = ctx.meta['config']
    config_dir: Path = cli_config.app_directory / '.amsdal'
    config_dir.mkdir(exist_ok=True, parents=True)
    _env_path: Path = config_dir / '.environment'

    if not _env_path.exists():
        _env_path.touch(exist_ok=True)
        set_current_environment(ctx, DEFAULT_ENV)

    return _env_path


def get_current_env(ctx: typer.Context) -> str:
    _env_path = _get_enviroments_path(ctx)
    _envs = {env for env in _env_path.read_text().split('\n') if env}

    if len(_envs) == 1:
        return _envs.pop()

    print(
        '[dark_orange]Invalid environment config. Please checkout to a valid environment. '
        f'Using default [dark_cyan]{DEFAULT_ENV}[/dark_cyan] environment.[/dark_orange]'
    )
    return DEFAULT_ENV


def set_current_environment(ctx: typer.Context, env_name: str) -> None:
    _env_path = _get_enviroments_path(ctx)

    _env_path.write_text(env_name)
