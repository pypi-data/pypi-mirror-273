import contextlib
import pathlib
import tomllib

import platformdirs

import unico_device_setuper
from unico_device_setuper.lib import utils


def is_release_version():
    pyproject_path = utils.module_path(unico_device_setuper).parent / 'pyproject.toml'
    with contextlib.suppress(FileNotFoundError):
        pyproject = tomllib.loads(pyproject_path.read_text())
        if pyproject.get('tool', {}).get('poetry', {}).get('name') == unico_device_setuper.__name__:
            return False
    return True


def get():
    if is_release_version():
        return pathlib.Path(platformdirs.user_data_dir(appname=utils.APP_NAME)).absolute()

    return utils.module_path(unico_device_setuper).parent / 'data'


@contextlib.contextmanager
def get_temporary():
    with utils.temporary_dir(get()) as dir:
        yield dir
