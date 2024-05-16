import asyncio
import enum
import sys
import typing

import rich
import typer

import unico_device_setuper
from unico_device_setuper.cli import pkg, stp, unav
from unico_device_setuper.lib import auth, datadir

APP = typer.Typer(pretty_exceptions_enable=False)


@APP.callback(invoke_without_command=True)
def main(
    ctx: typer.Context, *, version: bool = False, data_dir: bool = False, logout: bool = False
):
    if version:
        rich.print(unico_device_setuper.__version__)
        sys.exit(0)

    if data_dir:
        rich.print(datadir.get())
        sys.exit(0)

    if logout:
        auth.clear_credentials()
        sys.exit(0)

    if len(sys.argv) == 1:
        typer.echo(ctx.get_help())


class PackageAction(enum.Enum):
    LIST = 'list'
    UNINSTALL = 'uninstall'


@APP.command()
def package(
    action: PackageAction,
    *,
    restart_adb: bool = False,
    unitech_client: typing.Optional[str] = None,  # noqa: UP007
    env: typing.Optional[stp.Env] = None,  # noqa: UP007
):
    asyncio.run(
        async_package(
            action, stp.Args(restart_adb=restart_adb, unitech_client=unitech_client, env=env)
        )
    )


async def async_package(action: PackageAction, args: stp.Args):
    async with stp.Setup.make(args) as setup:
        match action:
            case PackageAction.LIST:
                await pkg.list_packages(setup)
            case PackageAction.UNINSTALL:
                await pkg.uninstall_list_packages(setup)


class UninavAction(enum.Enum):
    INSTALL = 'install'


@APP.command()
def uninav(
    action: UninavAction,
    *,
    restart_adb: bool = False,
    unitech_client: typing.Optional[str] = None,  # noqa: UP007
    env: typing.Optional[stp.Env] = None,  # noqa: UP007
):
    asyncio.run(
        async_uninav(
            action, stp.Args(restart_adb=restart_adb, unitech_client=unitech_client, env=env)
        )
    )


async def async_uninav(action: UninavAction, args: stp.Args):
    async with stp.Setup.make(args) as setup:
        match action:
            case UninavAction.INSTALL:
                uninav_path = await unav.get_uninav_apk_url(setup)
                await unav.install_uninav(uninav_path, setup)
