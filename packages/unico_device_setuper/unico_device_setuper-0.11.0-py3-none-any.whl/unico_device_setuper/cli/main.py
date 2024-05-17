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


async def _package(action: PackageAction, args: stp.Args):
    async with stp.Setup.make(args) as setup:
        match action:
            case PackageAction.LIST:
                await pkg.list_packages(setup)
            case PackageAction.UNINSTALL:
                await pkg.uninstall_packages(setup)


@APP.command()
def package(
    action: PackageAction,
    *,
    restart_adb: bool = False,
    unitech_client: typing.Optional[str] = None,  # noqa: UP007
    env: typing.Optional[stp.Env] = None,  # noqa: UP007
):
    asyncio.run(
        _package(action, stp.Args(restart_adb=restart_adb, unitech_client=unitech_client, env=env))
    )


class UninavAction(enum.Enum):
    INSTALL = 'install'
    REGISTER = 'register'


async def _uninav(action: UninavAction, args: stp.Args):
    async with stp.Setup.make(args) as setup:
        match action:
            case UninavAction.INSTALL:
                await unav.install_uninav(setup)
            case UninavAction.REGISTER:
                await unav.register_device(setup)


@APP.command()
def uninav(
    action: UninavAction,
    *,
    restart_adb: bool = False,
    unitech_client: typing.Optional[str] = None,  # noqa: UP007
    env: typing.Optional[stp.Env] = None,  # noqa: UP007
):
    asyncio.run(
        _uninav(action, stp.Args(restart_adb=restart_adb, unitech_client=unitech_client, env=env))
    )
