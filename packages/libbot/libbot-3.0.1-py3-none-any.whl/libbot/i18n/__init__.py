from os import listdir
from pathlib import Path
from typing import Any, Dict, Union

import libbot
from libbot.i18n import sync
from libbot.i18n.classes.bot_locale import BotLocale


async def _(
    key: str,
    *args: str,
    locale: Union[str, None] = "en",
    locales_root: Union[str, Path] = Path("locale"),
) -> Any:
    """Get value of locale string

    ### Args:
        * key (`str`): The last key of the locale's keys path.
        * *args (`list`): Path to key like: `dict[args][key]`.
        * locale (`Union[str, None]`): Locale to looked up in. Defaults to `"en"`.
        * locales_root (`Union[str, Path]`, *optional*): Folder where locales are located. Defaults to `Path("locale")`.

    ### Returns:
        * `Any`: Value of provided locale key. Is usually `str`, `dict` or `list`
    """
    locale = libbot.sync.config_get("locale") if locale is None else locale

    try:
        this_dict = await libbot.json_read(Path(f"{locales_root}/{locale}.json"))
    except FileNotFoundError:
        try:
            this_dict = await libbot.json_read(
                Path(f'{locales_root}/{await libbot.config_get("locale")}.json')
            )
        except FileNotFoundError:
            return f'⚠️ Locale in config is invalid: could not get "{key}" in {args} from locale "{locale}"'

    this_key = this_dict
    for dict_key in args:
        this_key = this_key[dict_key]

    try:
        return this_key[key]
    except KeyError:
        return f'⚠️ Locale in config is invalid: could not get "{key}" in {args} from locale "{locale}"'


async def in_all_locales(
    key: str, *args: str, locales_root: Union[str, Path] = Path("locale")
) -> list:
    """Get value of the provided key and path in all available locales

    ### Args:
        * key (`str`): The last key of the locale's keys path.
        * *args (`list`): Path to key like: `dict[args][key]`.
        * locales_root (`Union[str, Path]`, *optional*): Folder where locales are located. Defaults to `Path("locale")`.

    ### Returns:
        * `list`: List of values in all locales
    """

    output = []
    files_locales = listdir(locales_root)

    valid_locales = [".".join(entry.split(".")[:-1]) for entry in files_locales]
    for lc in valid_locales:
        try:
            this_dict = await libbot.json_read(Path(f"{locales_root}/{lc}.json"))
        except FileNotFoundError:
            continue

        this_key = this_dict
        for dict_key in args:
            this_key = this_key[dict_key]

        try:
            output.append(this_key[key])
        except KeyError:
            continue

    return output


async def in_every_locale(
    key: str, *args: str, locales_root: Union[str, Path] = Path("locale")
) -> Dict[str, Any]:
    """Get value of the provided key and path in every available locale with locale tag

    ### Args:
        * key (`str`): The last key of the locale's keys path.
        * *args (`list`): Path to key like: `dict[args][key]`.
        * locales_root (`Union[str, Path]`, *optional*): Folder where locales are located. Defaults to `Path("locale")`.

    ### Returns:
        * `Dict[str, Any]`: Locale is a key and it's value from locale file is a value
    """

    output = {}
    files_locales = listdir(locales_root)

    valid_locales = [".".join(entry.split(".")[:-1]) for entry in files_locales]
    for lc in valid_locales:
        try:
            this_dict = await libbot.json_read(Path(f"{locales_root}/{lc}.json"))
        except FileNotFoundError:
            continue

        this_key = this_dict
        for dict_key in args:
            this_key = this_key[dict_key]

        try:
            output[lc] = this_key[key]
        except KeyError:
            continue

    return output
