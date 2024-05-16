import typing
from pathlib import Path

import typer
from amsdal.cloud.enums import DeployType
from amsdal.cloud.enums import LakehouseOption
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.commands.cloud.deploy.app import deprecated_deploy_sub_app
from amsdal_cli.commands.cloud.environments.constants import DEFAULT_ENV
from amsdal_cli.utils.cli_config import CliConfig


@deploy_sub_app.command('new, n')
def deploy_command(
    ctx: typer.Context,
    deploy_type: DeployType = DeployType.include_state_db,
    lakehouse_type: LakehouseOption = LakehouseOption.postgres,
    env_name: str = Option(DEFAULT_ENV, '--env', help='Environment name.'),
    from_env: typing.Optional[str] = Option(None, '--from-env', help='Environment name to copy from.'),  # noqa: UP007
    *,
    no_input: bool = Option(False, '--no-input', help='Do not prompt for input.'),
    skip_checks: bool = Option(
        False,
        '--skip-checks',
        help='Skip checking secrets and dependencies before deploying.',
    ),
) -> None:
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    if not skip_checks:
        try:
            list_response_deps = manager.cloud_actions_manager.list_dependencies(
                env_name=env_name,
                application_uuid=cli_config.application_uuid,
                application_name=cli_config.application_name,
            )
        except AmsdalCloudError as e:
            print(f'[red]Failed to loading dependencies: {e}[/red]')
            raise typer.Exit(1) from e

        _deps_path: Path = cli_config.app_directory / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps = set(_deps_path.read_text().split('\n'))
        _diff_deps = list(filter(None, _deps - set(list_response_deps.dependencies)))

        if _diff_deps:
            print(f'[yellow]The following dependencies are missing: {", ".join(_diff_deps)}[/yellow]')

            if no_input:
                print('[blue]Installing missing dependencies...[/blue]')
                install_deps = True
            else:
                install_deps = typer.confirm('Do you want to install the missing dependencies?')

            if not install_deps:
                print('[blue]Use "amsdal cloud dependencies new NAME" to install the missing dependencies.[/blue]')
                raise typer.Exit(1)

            for dependency_name in _diff_deps:
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

        try:
            list_response_secrets = manager.cloud_actions_manager.list_secrets(
                with_values=False,
                env_name=env_name,
                application_uuid=cli_config.application_uuid,
                application_name=cli_config.application_name,
            )
        except AmsdalCloudError as e:
            print(f'[red]Failed to loading secrets: {e}[/red]')
            raise typer.Exit(1) from e

        _secrets_path: Path = cli_config.app_directory / '.secrets'
        _secrets_path.touch(exist_ok=True)
        _secrets = set(_secrets_path.read_text().split('\n'))
        _diff_secrets = list(filter(None, _secrets - set(list_response_secrets.secrets)))

        if _diff_secrets:
            print(f'[red]The following secrets are missing: {", ".join(_diff_secrets)}[/red]')
            raise typer.Exit(1)

    try:
        manager.cloud_actions_manager.create_deploy(
            deploy_type=deploy_type.value,
            lakehouse_type=lakehouse_type.value,
            env_name=env_name,
            from_env=from_env,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            no_input=no_input,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e


@deprecated_deploy_sub_app.callback(invoke_without_command=True)
def deploy_command_deprecated(
    ctx: typer.Context,
    deploy_type: DeployType = DeployType.include_state_db,
    lakehouse_type: LakehouseOption = LakehouseOption.postgres,
    *,
    no_input: bool = Option(False, '--no-input', help='Do not prompt for input.'),
    skip_checks: bool = Option(
        False,
        '--skip-checks',
        help='Skip checking secrets and dependencies before deploying.',
    ),
) -> None:
    """
    Deploy the app to the Cloud Server.
    """

    if ctx.invoked_subcommand is not None:
        return

    deploy_command(
        ctx=ctx,
        deploy_type=deploy_type,
        lakehouse_type=lakehouse_type,
        no_input=no_input,
        skip_checks=skip_checks,
    )
