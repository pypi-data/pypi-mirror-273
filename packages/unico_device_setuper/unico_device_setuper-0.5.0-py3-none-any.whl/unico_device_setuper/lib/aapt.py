import contextlib
import dataclasses
import pathlib

import httpx
import pydantic_core

from unico_device_setuper.lib import adb, datadir, dl, utils

APDE_DOWNLOAD_URL = pydantic_core.Url(
    'https://github.com/Calsign/APDE/archive/refs/tags/v0.5.1-alpha.zip'
)


@dataclasses.dataclass
class Aapt:
    adb_ctx: adb.Adb
    aapt_remote_path: pathlib.Path

    async def dump(self, *args: str, ignore_error: bool):
        return await self.adb_ctx.shell(
            f'{self.aapt_remote_path} dump {' '.join(f"'{arg}'" for arg in args)}',
            ignore_error=ignore_error,
        )

    @contextlib.asynccontextmanager
    @staticmethod
    async def make(adb_ctx: adb.Adb, http_client: httpx.AsyncClient):
        aapt_path = datadir.get() / 'aapt'
        if not utils.is_executable(aapt_path):
            await dl.download_and_extract_zipped_executable(
                APDE_DOWNLOAD_URL,
                pathlib.Path('APDE') / 'src' / 'main' / 'assets' / 'aapt-binaries' / 'aapt-arm-pie',
                aapt_path,
                http_client,
            )

        aapt_remote_path = pathlib.Path('/') / 'data' / 'local' / 'tmp' / 'aapt'
        try:
            await adb_ctx.push(aapt_path, aapt_remote_path)
            yield Aapt(adb_ctx, aapt_remote_path)
        finally:
            await adb_ctx.shell(f"rm '{aapt_remote_path}'")
