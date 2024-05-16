import asyncio
import collections
import contextlib
import os
import pathlib
import shutil
import subprocess
import types
import typing
import uuid

APP_NAME = 'com.unico.dev.device_setuper'

### Path stuff


def module_path(module: types.ModuleType):
    module_file = module.__file__
    assert module_file is not None
    return pathlib.Path(module_file).parent.absolute()


@contextlib.contextmanager
def temporary_dir(base: pathlib.Path):
    dir = base / str(uuid.uuid4())
    dir.mkdir(exist_ok=True, parents=True)
    try:
        yield dir
    finally:
        shutil.rmtree(dir)


### Subprocess stuff


async def _read_loop(stream: asyncio.StreamReader | None, storage: list[str]):
    if stream is None:
        return
    while True:
        line = await stream.readline()
        if len(line) == 0:
            break
        storage.append(line.decode())


async def exec_proc(exe: pathlib.Path, *args: str, ignore_error: bool = False):
    process = await asyncio.subprocess.create_subprocess_exec(
        exe, *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    stdout_reader = asyncio.get_event_loop().create_task(_read_loop(process.stdout, stdout_lines))
    stderr_reader = asyncio.get_event_loop().create_task(_read_loop(process.stderr, stderr_lines))
    (return_code, _, _) = await asyncio.gather(process.wait(), stdout_reader, stderr_reader)

    stdout = ''.join(stdout_lines)
    stderr = ''.join(stderr_lines)

    if not ignore_error and return_code != 0:
        raise RuntimeError(
            f'Command {exe.name} {' '.join(args)} returned {return_code}',
            f'stdout: {stdout}' f'stderr: {stderr}',
        )

    return stdout


def is_executable(path: pathlib.Path):
    return path.exists() and path.is_file() and os.access(path, os.X_OK)


### Other


async def gather[T](futures: typing.Iterable[typing.Awaitable[T]]) -> list[T]:
    return await asyncio.gather(*futures)


def groupby[T, K: typing.Hashable](
    values: typing.Iterable[T], key: typing.Callable[[T], K]
) -> typing.Mapping[K, typing.Sequence[T]]:
    key_values_map: dict[K, list[T]] = collections.defaultdict(list)
    for value in values:
        key_values_map[key(value)].append(value)
    return key_values_map
