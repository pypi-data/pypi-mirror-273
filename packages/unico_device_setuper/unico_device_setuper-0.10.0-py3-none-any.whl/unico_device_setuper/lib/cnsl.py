import contextlib
import typing

import rich


def _colored_print(s: str, color: str, end: str | None = None):
    return rich.print(f'[{color}]{s}[/{color}]', end=end if end is not None else '\n')


def print(s: str = '', end: str | None = None):
    _colored_print(s, 'white', end)


def print_gray(s: str = '', end: str | None = None):
    _colored_print(s, 'bright_black', end)


def print_red(s: str, end: str | None = None):
    _colored_print(s, 'red', end)


def print_blue(s: str, end: str | None = None):
    _colored_print(s, 'blue', end)


def print_cyan(s: str, end: str | None = None):
    _colored_print(s, 'cyan', end)


def print_greeen(s: str, end: str | None = None):
    _colored_print(s, 'green', end)


def choose[T](items: list[T], prompt: str | None = None) -> T:
    if len(items) == 0:
        raise RuntimeError('Cannot choose between 0 element')
    if len(items) == 1:
        return items[0]
    while True:
        with contextlib.suppress(Exception):
            rich.print('\n', prompt or 'choice : ', end='')
            user_input = input()
            if user_input == '':
                raise BaseException
            if 0 <= (choice := int(user_input)) < len(items):
                return items[choice]
        print_red('Choix invalide')


def print_choose[T](
    items: list[T],
    prompt: str | None = None,
    *,
    formater: typing.Callable[[T], str] | None = None,
    choice_formater: typing.Callable[[T], str] | None = None,
    headers: list[str] | None = None,
) -> T:
    if formater is None:
        formater = str
    if choice_formater is None:
        choice_formater = formater

    max_index = len(str(len(items) - 1))
    if headers is not None:
        for header in headers:
            rich.print(f" {'':>{max_index}}   {header}")
    console = rich.console.Console(highlight=False)
    for i, item in enumerate(items):
        console.print(f' [bold cyan]{i:>{max_index}}[/] - {formater(item)}')
    choice = choose(items, prompt)
    console.print(f'\nVous avez choisi {choice_formater(choice)}', style='green')
    return choice
