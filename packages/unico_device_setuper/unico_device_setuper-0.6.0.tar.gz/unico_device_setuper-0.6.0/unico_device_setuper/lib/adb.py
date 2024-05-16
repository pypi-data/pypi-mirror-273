import contextlib
import dataclasses
import pathlib

import httpx
import pydantic_core

from unico_device_setuper.lib import datadir, dl, utils

ADB_DOWNLOAD_URL = pydantic_core.Url(
    'https://dl.google.com/android/repository/platform-tools-latest-darwin.zip'
)


@dataclasses.dataclass
class Adb:
    adb_exe: pathlib.Path

    @contextlib.asynccontextmanager
    @staticmethod
    async def make(http_client: httpx.AsyncClient, *, restart_server: bool):
        adb_path = datadir.get() / 'adb'

        if not utils.is_executable(adb_path):
            await dl.download_and_extract_zipped_executable(
                ADB_DOWNLOAD_URL, pathlib.Path('adb'), adb_path, http_client
            )

        ctx = Adb(adb_path)
        if restart_server:
            await ctx.kill_server()
        await ctx.start_server()
        yield ctx

    async def _exec(self, *args: str, ignore_error: bool = False):
        return await utils.exec_proc(self.adb_exe, *args, ignore_error=ignore_error)

    async def start_server(self):
        return await self._exec('start-server')

    async def kill_server(self):
        return await self._exec('kill-server')

    async def uninstall_uninav(self):
        return await self._exec('uninstall', 'com.unico.dev.appmobile')

    async def shell(self, cmd: str, *, ignore_error: bool = False):
        return await self._exec('shell', cmd, ignore_error=ignore_error)

    async def shell_uninstall(self, package_name: str):
        return await self.shell(f'pm uninstall -k --user 0 {package_name}')

    async def shell_disable(self, package_name: str):
        return await self.shell(f'pm disable-user --user 0 {package_name}')

    async def shell_install(self, apk_path: pathlib.Path):
        return await self.shell(f'pm install {apk_path}')

    async def push(self, local_path: pathlib.Path, remote_path: pathlib.Path):
        return await self._exec('push', str(local_path), str(remote_path))
