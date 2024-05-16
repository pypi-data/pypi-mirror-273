import contextlib
import pathlib

import pydantic_core

from unico_device_setuper.cli import stp
from unico_device_setuper.lib import datadir, dl, unitech


async def get_uninav_apk_url(setup: stp.Setup):
    change_log = await unitech.get_device_update_change_log.request(await setup.unitech_client)
    assert change_log
    assert change_log.release_url
    assert change_log.latest_version_name
    uninav_download_url = pydantic_core.Url(change_log.release_url)
    uninav_install_path = datadir.get() / f'uninav{change_log.latest_version_name}.apk'
    if not uninav_install_path.exists():
        await dl.download_url(
            uninav_download_url, uninav_install_path, setup.http_client, uninav_install_path.name
        )
    return uninav_install_path


async def install_uninav(uninav_path: pathlib.Path, setup: stp.Setup):
    uninav_remote_path = pathlib.Path('/') / 'data' / 'local' / 'tmp' / 'uninav'

    await setup.adb.push(uninav_path, uninav_remote_path)
    with contextlib.suppress(RuntimeError):
        await setup.adb.uninstall_uninav()
    await setup.adb.shell_install(uninav_remote_path)
