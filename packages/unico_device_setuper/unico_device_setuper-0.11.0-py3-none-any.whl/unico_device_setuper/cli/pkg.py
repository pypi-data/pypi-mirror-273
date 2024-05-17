import contextlib
import dataclasses
import pathlib

import slugify
import tqdm

from unico_device_setuper.cli import stp
from unico_device_setuper.lib import cnsl, utils


@dataclasses.dataclass
class Package:
    label: str
    name: str
    version: str | None = None


async def get_package_from_apk_path(apk_path: pathlib.Path, name: str, setup: stp.Setup):
    package_prefix = 'package:'
    launchable_activity_prefix = 'launchable-activity:'
    base_label_prefix = 'application-label:'
    label_fr_prefix = 'application-label-fr:'

    launchable_activity_label = None
    base_label = None
    label_fr = None
    version = None

    with contextlib.suppress(utils.SubprocessError):
        async for line in setup.aapt.dump_badging(apk_path):
            if line.startswith(launchable_activity_prefix):
                line_value = line.removeprefix(launchable_activity_prefix)
                _, _, label_and_after = line_value.partition('label=')
                label_value_and_space, _, _ = label_and_after.partition("='")
                launchable_activity_label = ' '.join(label_value_and_space.split()[:-1])[1:-1]
            if line.startswith(label_fr_prefix):
                label_fr = line.removeprefix(label_fr_prefix)[1:-1]
            if line.startswith(base_label_prefix):
                base_label = line.removeprefix(base_label_prefix)[1:-1]
            if line.startswith(package_prefix):
                line_value = line.removeprefix(package_prefix)
                _, _, version_and_after = line_value.partition('versionName=')
                version_and_space, _, _ = version_and_after.partition("='")
                version = ' '.join(version_and_space.split()[:-1])[1:-1]

    label = launchable_activity_label or label_fr or base_label
    if label is None:
        return None

    return Package(label=label, name=name, version=version)


def parse_package_list(output: list[str]):
    prefix = 'package:'
    for line in output:
        if line.startswith(prefix):
            yield line.removeprefix(prefix)


async def list_packages(setup: stp.Setup):
    package_apk_path_map: dict[str, pathlib.Path] = {}
    for line in parse_package_list(await setup.adb.shell('pm list package -f')):
        (path, _, name) = line.rpartition('=')
        package_apk_path_map[name] = pathlib.Path(path)

    packages = [
        package
        for name, path in tqdm.tqdm(package_apk_path_map.items())
        if (package := await get_package_from_apk_path(path, name, setup)) is not None
    ]

    max_label_length = max(len(p.label) for p in packages)
    for package in sorted(packages, key=lambda p: slugify.slugify(p.label)):
        cnsl.print_cyan(f' {package.label:<{max_label_length}}', end='')
        cnsl.print_blue(f' {package.name}', end='')
        cnsl.print_gray(f' ({package.version})' if package.version else '')


async def uninstall_packages(setup: stp.Setup):
    await uninstall_listed_packages(setup)
    await clear_launcher_app_storage(setup)


PACKAGE_TO_UNINSTALL: list[Package] = [
    Package('Chrome', name='com.android.chrome'),
    Package('Drive', name='com.google.android.apps.docs'),
    Package('Gmail', name='com.google.android.gm'),
    Package('Google', name='com.google.android.googlequicksearchbox'),
    Package('Google TV', name='com.google.android.videos'),
    Package('Maps', name='com.google.android.apps.maps'),
    Package('Galaxy Store', name='com.sec.android.app.samsungapps'),
    Package('Outlook', name='com.microsoft.office.outlook'),
    Package('Smart Switch', name='com.samsung.android.smartswitchassistant'),
    Package('Smart Switch', name='com.sec.android.easyMover'),
    Package('Meet', name='com.google.android.apps.tachyon'),
    Package('Photos', name='com.google.android.apps.photos'),
    Package('OneDrive', name='com.microsoft.skydrive'),
    Package('Microsoft 365 (Office)', name='com.microsoft.office.officehubrow'),
    Package('Google Play', name='com.android.vending'),
    Package('Samsung Notes', name='com.samsung.android.app.notes'),
    Package('Slack', name='com.Slack'),
    Package('Sure Protect', name='com.gears42.surelock'),
    Package('WPS Office', name='cn.wps.moffice_eng'),
    Package('YT Music', name='com.google.android.apps.youtube.music'),
    Package('YouTube', name='com.google.android.youtube'),
    Package('Samsung Free', name='com.samsung.android.app.spage'),
    Package('Game Launcher', name='com.samsung.android.game.gamehome'),
    Package('Samsung Flow', name='com.samsung.android.galaxycontinuity'),
    Package('AR Zone', name='com.samsung.android.arzone'),
    Package('Messages', name='com.google.android.apps.messaging'),
    Package('Mes fichiers', name='com.sec.android.app.myfiles'),
    Package('Calendrier', name='com.samsung.android.calendar'),
    Package('Clock', name='com.sec.android.app.clockpackage'),
    Package('Netflix', name='com.netflix.mediaclient'),
    Package('Mise à jour configuration', name='com.samsung.android.app.omcagent'),
    Package('Samsung Members', name='com.samsung.android.voc'),
]


async def get_installed_package_names(setup: stp.Setup):
    return set(parse_package_list(await setup.adb.shell('pm list package')))


async def uninstall_listed_packages(setup: stp.Setup):
    installed_package_names = await get_installed_package_names(setup)

    await utils.gather(
        uninstall_package(package.name, installed_package_names, setup)
        for package in PACKAGE_TO_UNINSTALL
    )


async def uninstall_package(package_name: str, installed_package_names: set[str], setup: stp.Setup):
    if package_name not in installed_package_names:
        cnsl.print_gray(f'{package_name} déjà désinstallé')
        return
    try:
        await setup.adb.shell(f'pm uninstall -k --user 0 {package_name}')
        cnsl.print_greeen(f'{package_name} désinstallé avec succès')
    except RuntimeError:
        cnsl.print_red(f'Erreur lors de la désinstallation de {package_name}')


LAUNCHER_APP_PACKAGE_NAMES = ['com.sec.android.app.launcher']


async def clear_launcher_app_storage(setup: stp.Setup):
    installed_package_names = await get_installed_package_names(setup)

    for laucher_app_package_name in LAUNCHER_APP_PACKAGE_NAMES:
        if laucher_app_package_name in installed_package_names:
            await setup.adb.shell(f'pm clear {laucher_app_package_name}')
