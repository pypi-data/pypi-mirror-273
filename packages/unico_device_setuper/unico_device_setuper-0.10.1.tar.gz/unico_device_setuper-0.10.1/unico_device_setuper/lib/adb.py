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

    def _exec_gen(self, *args: object):
        return utils.exec_proc(self.adb_exe, *map(str, args))

    async def _exec(self, *args: object):
        return [line async for line in utils.exec_proc(self.adb_exe, *map(str, args))]

    #

    def start_server(self):
        return self._exec('start-server')

    def kill_server(self):
        return self._exec('kill-server')

    #

    def logcat(self, *args: str):
        return self._exec('logcat', *args)

    def logcat_gen(self, *args: str):
        return self._exec_gen('logcat', *args)

    #

    def install(self, local_apk_path: pathlib.Path):
        return self._exec('install', local_apk_path)

    def uninstall(self, package_name: str):
        return self._exec('uninstall', package_name)

    #

    def shell_gen(self, cmd: str):
        return self._exec_gen('shell', cmd)

    def shell(self, cmd: str):
        return self._exec('shell', cmd)

    #

    async def push(self, local_path: pathlib.Path, remote_path: pathlib.Path):
        return await self._exec('push', local_path, remote_path)
