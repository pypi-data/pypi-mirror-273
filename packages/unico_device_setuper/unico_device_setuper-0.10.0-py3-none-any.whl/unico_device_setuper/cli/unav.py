import asyncio
import contextlib
import datetime
import typing

import pydantic_core

from unico_device_setuper.cli import stp
from unico_device_setuper.lib import cnsl, datadir, dl, unitech


async def download_uninav_apk(setup: stp.Setup):
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


async def install_uninav(setup: stp.Setup):
    apk_path = await download_uninav_apk(setup)
    with contextlib.suppress(RuntimeError):
        await setup.adb.uninstall('com.unico.dev.appmobile')
    await setup.adb.install(apk_path)


async def start_setuper_activity(setup: stp.Setup):
    await setup.adb.shell(
        'am start -n com.unico.dev.appmobile/.core.setuper.IdDeviceLoggerActivity'
    )


async def stop_uninav(setup: stp.Setup):
    await setup.adb.shell('am force-stop com.unico.dev.appmobile')


async def find_device_id_in_logs(logs: typing.AsyncIterable[str]):
    async for line in logs:
        line_parts = line.split('ID_DEVICE: ')
        if len(line_parts) > 1:
            return line_parts[-1]
    return None


SETUPER_ACTIVITY_TIMEOUT = datetime.timedelta(seconds=10)


async def get_id_device(setup: stp.Setup):
    await stop_uninav(setup)
    await setup.adb.logcat('-c')
    await start_setuper_activity(setup)
    try:
        return await asyncio.wait_for(
            find_device_id_in_logs(setup.adb.logcat_gen()),
            timeout=SETUPER_ACTIVITY_TIMEOUT.total_seconds(),
        )
    except TimeoutError:
        return None
    finally:
        await stop_uninav(setup)


async def register_device(setup: stp.Setup):
    device_id = await get_id_device(setup)
    if device_id is None:
        cnsl.print_red("Impossible de trouver l'id device")
    else:
        cnsl.print_cyan(f'Id Device: {device_id}')
        await unitech.post_auth_device_register_device.request(
            await setup.unitech_client, unitech.RegisterDevicePayload('test_register', device_id)
        )
