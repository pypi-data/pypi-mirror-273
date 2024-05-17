import contextlib
import dataclasses
import enum

import httpx
import pydantic_core

from unico_device_setuper.lib import aapt, adb, auth, unitech


class Env(enum.Enum):
    DEV = 'dev'
    PRE_PROD = 'pre-prod'
    PROD = 'prod'
    LOCAL = 'local'


@dataclasses.dataclass
class Args:
    restart_adb: bool
    unitech_client: str | None
    env: Env | None


def get_unitech_api_base_url(args: Args):
    if args.env == Env.LOCAL:
        return pydantic_core.Url('http://localhost:3000')
    return pydantic_core.Url(f'https://api.{(args.env or Env.PROD).value}.unicofrance.com')


@dataclasses.dataclass
class Setup:
    args: Args
    _unitech_client: unitech.Client
    http_client: httpx.AsyncClient
    adb: adb.Adb
    aapt: aapt.Aapt

    @contextlib.asynccontextmanager
    @staticmethod
    async def make(args: Args):
        async with (
            unitech.Client(base_url=str(get_unitech_api_base_url(args))) as unitech_client,
            httpx.AsyncClient() as http_client,
            adb.Adb.make(http_client, restart_server=args.restart_adb) as adb_,
            aapt.Aapt.make(adb_, http_client) as aapt_,
        ):
            yield Setup(args, unitech_client, http_client, adb_, aapt_)

    @property
    def unitech_api_base_url(self):
        return get_unitech_api_base_url(self.args)

    @property
    async def unitech_client(self):
        headers = self._unitech_client.get_async_httpx_client().headers
        auth_header_name = 'Authorization'
        if headers.get(auth_header_name) is None:
            headers[auth_header_name] = 'Bearer ' + await auth.get_auth_token(
                self.unitech_api_base_url, client_name=self.args.unitech_client
            )
        return self._unitech_client
