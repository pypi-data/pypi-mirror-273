import dataclasses

import slugify
import tqdm

from unico_device_setuper.cli import stp
from unico_device_setuper.lib import cnsl, utils


@dataclasses.dataclass
class Package:
    label: str
    name: str


async def get_package_from_apk_path(apk_path: str, name: str, setup: stp.Setup):
    output = await setup.aapt.dump('badging', apk_path, ignore_error=True)

    launchable_activity_prefix = 'launchable-activity:'
    base_label_prefix = 'application-label:'
    label_fr_prefix = 'application-label-fr:'

    launchable_activity_label = None
    base_label = None
    label_fr = None
    for line in output.splitlines():
        if line.startswith(launchable_activity_prefix):
            line_value = line.removeprefix(launchable_activity_prefix)
            _, _, label_and_after = line_value.partition('label=')
            label_value_and_space, _, _ = label_and_after.partition("='")
            launchable_activity_label = ' '.join(label_value_and_space.split()[:-1])[1:-1]
        if line.startswith(label_fr_prefix):
            label_fr = line.removeprefix(label_fr_prefix)[1:-1]
        if line.startswith(base_label_prefix):
            base_label = line.removeprefix(base_label_prefix)[1:-1]

    label = launchable_activity_label or label_fr or base_label
    if label is None:
        return None

    return Package(label=label, name=name)


def parse_package_list(output: str):
    prefix = 'package:'
    for line in output.splitlines():
        if line.startswith(prefix):
            yield line.removeprefix(prefix)


async def list_packages(setup: stp.Setup):
    package_apk_path_map: dict[str, str] = {}
    for line in parse_package_list(await setup.adb.shell('pm list package -f')):
        (path, _, name) = line.rpartition('=')
        package_apk_path_map[name] = path

    packages = [
        package
        for name, path in tqdm.tqdm(package_apk_path_map.items())
        if (package := await get_package_from_apk_path(path, name, setup)) is not None
    ]

    max_label_length = max(len(p.label) for p in packages)
    for package in sorted(packages, key=lambda p: slugify.slugify(p.label)):
        cnsl.print_blue(f' {package.label:<{max_label_length}}', end='')
        cnsl.print(f' {package.name}')


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
    Package('Messages', name='com.samsung.android.messaging'),
    Package('Mes fichiers', name='com.sec.android.app.myfiles'),
    Package('Calendrier', name='com.samsung.android.calendar'),
    Package('Clock', name='com.sec.android.app.clockpackage'),
]


async def uninstall_list_packages(setup: stp.Setup):
    installed_package_names = set(parse_package_list(await setup.adb.shell('pm list package')))

    await utils.gather(
        uninstall_package(package.name, installed_package_names, setup)
        for package in PACKAGE_TO_UNINSTALL
    )


async def uninstall_package(package_name: str, installed_package_names: set[str], setup: stp.Setup):
    if package_name not in installed_package_names:
        cnsl.print_gray(f'{package_name} déjà désinstallé')
        return
    try:
        await setup.adb.shell_uninstall(package_name)
        cnsl.print_greeen(f'{package_name} désinstallé avec succès')
    except RuntimeError:
        cnsl.print_red(f'Erreur lors de la désinstallation de {package_name}')
